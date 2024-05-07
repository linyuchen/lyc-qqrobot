import abc
import queue
import threading
import time
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic

from common.logger import logger


class TaskStatus(Enum):
    WAITING = 0
    HANDLING = 1
    FINISHED = 2
    TIMEOUT = 3


class Task:
    create_time: float = 0
    status: TaskStatus = TaskStatus.WAITING

    def finish(self):
        self.status = TaskStatus.FINISHED


TaskT = TypeVar('TaskT', bound=Task)


class TaskPool(Generic[TaskT], metaclass=abc.ABCMeta):

    def __init__(self, concurrency: int = 1, time_out: int = 60 * 3):
        self.concurrency = concurrency
        self.time_out = time_out
        super().__init__()
        self._lock = threading.Lock()
        self.tasks: queue.Queue[TaskT] = queue.Queue()
        self.handling_tasks: list[TaskT] = []
        threading.Thread(target=self.__put_task_thread, daemon=True).start()
        threading.Thread(target=self.__check_task_finished_thread, daemon=True).start()

    def __put_task_thread(self):
        # 控制并发数
        while True:
            time.sleep(0.1)
            if self.tasks.empty():
                continue
            if len(self.handling_tasks) == self.concurrency:
                continue
            task = self.tasks.get()
            try:
                with self._lock:
                    task.status = TaskStatus.HANDLING
                    self.handling_tasks.append(task)
                    threading.Thread(target=self.__on_task_handling, args=(task,), daemon=True).start()
            except Exception as e:
                logger.error(f"处理任务失败：{e}")

    def __check_task_finished_thread(self):
        while True:
            time.sleep(0.1)
            self._lock.acquire()
            if not self.handling_tasks:
                self._lock.release()
                continue
            for task in self.handling_tasks:
                if time.time() - task.create_time > self.time_out:
                    self.handling_tasks.remove(task)
                    task.status = TaskStatus.TIMEOUT
                    threading.Thread(target=self._on_task_timeout, args=(task,), daemon=True).start()
                    continue
                if task.status == TaskStatus.FINISHED:
                    self.handling_tasks.remove(task)
                    threading.Thread(target=self._on_task_finished, args=(task,), daemon=True).start()
            self._lock.release()

    def join_task(self, task: TaskT):
        task.create_time = time.time()
        task.status = TaskStatus.WAITING
        self.tasks.put(task)

    def __on_task_handling(self, task: TaskT):
        try:
            self._on_task_handling(task)
        except Exception as e:
            logger.error(f"处理任务失败：{e}")

    @abstractmethod
    def _on_task_handling(self, task: TaskT):
        # 处理进入self.handling_tasks的task, 处理完了记得调用task.finish()
        pass

    def _on_task_finished(self, task: TaskT):
        pass

    def _on_task_timeout(self, task: TaskT):
        pass


if __name__ == '__main__':

    @dataclass
    class MyTask(Task):
        name: str

    class MyTaskPool(TaskPool[MyTask]):
        def __init__(self):
            super().__init__(concurrency=2)

        def _on_task_handling(self, task: MyTask):
            print("正在处理任务", task.name)
            time.sleep(5)
            task.finish()
        
        def _on_task_finished(self, task: MyTask):
            print("任务处理完成", task.name)

    
    my_task_pool = MyTaskPool()
    while True:
        task_name = input("输入任务名：")
        my_task_pool.join_task(MyTask(name=task_name))
