import abc
import dataclasses
import threading
import time
import traceback
from abc import abstractmethod
from typing import TypeVar, Generic


class Task:
    callback: callable
    finished: bool = False


TaskT = TypeVar('TaskT')


class TaskPool(threading.Thread, Generic[TaskT], metaclass=abc.ABCMeta):
    # 并发数
    concurrency: int = 1
    
    def __init__(self):
        super(threading.Thread, self).__init__()
        super().__init__()
        self._lock = threading.Lock()
        self.tasks: list[TaskT] = []
        self.handling_tasks: list[TaskT] = []
        threading.Thread(target=self.__put_task_thread).start()
        threading.Thread(target=self.__check_task_finished_thread).start()
    
    def _join_task(self, task: TaskT):
        self._lock.acquire()
        self.tasks.append(task)
        self._lock.release()
    
    @abstractmethod
    def run(self):
        # 监听task状态，将self.handling_tasks中的finished为True
        pass
    
    def __put_task_thread(self):
        # 控制并发数
        while True:
            time.sleep(0.1)
            self._lock.acquire()
            if len(self.tasks) == 0:
                self._lock.release()
                continue
            if len(self.handling_tasks) == self.concurrency:
                self._lock.release()
                continue
            if self.tasks:
                task = self.tasks.pop(0)
                try:
                    self.handling_tasks.append(task)
                    self._handle_put_task(task)
                except:
                    traceback.print_exc()
            self._lock.release()
    
    @abstractmethod
    def _handle_put_task(self, task: TaskT):
        # 处理进入self.handling_tasks的task
        pass
    
    def __check_task_finished_thread(self):
        while True:
            time.sleep(0.1)
            self._lock.acquire()
            if not self.handling_tasks:
                self._lock.release()
                continue
            for task in self.handling_tasks:
                if task.finished:
                    self.handling_tasks.remove(task)
                    threading.Thread(target=self._handle_finished_task, args=(task,)).start()
            self._lock.release()
    
    @abstractmethod
    def _handle_finished_task(self, task: TaskT):
        pass


if __name__ == '__main__':
    class MyTaskPool(TaskPool):
        def run(self):
            while True:
                time.sleep(2)
                if self.handling_tasks:
                    self.handling_tasks[0].finished = True
        
        def _handle_task(self, task):
            print("正在处理任务", task)
        
        def _handle_finished_task(self, task: TaskT):
            print("任务处理完成", task)
            task.callback()
    
    
    my_task_pool = MyTaskPool()
    my_task_pool.start()
    while True:
        task_name = input("输入任务名：")
        my_task_pool._join_task(TaskT(callback=lambda: print(task_name)))
