import dataclasses
import logging
import threading
import time
import traceback
from abc import abstractmethod
from typing import Callable

import ifnude

from common.utils.baidu_translator import is_chinese, trans
from common.utils.downloader import download2temp
from .base import AIDrawBase

logger = logging.getLogger(__name__)


@dataclasses.dataclass()
class DrawModel:
    name: str
    model_id: str
    model_file_id: str
    cover: str = None


@dataclasses.dataclass()
class Task:
    task_id: str = ""
    callback: Callable[[list[str]], None] = None
    finished: bool = False
    # status: str = ""
    img_urls: list[str] = None
    prompt: str = ""
    # progress: int = 0


class TaskStatusListener(threading.Thread):
    # 最高并发
    max_concurrency = 2

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.tasks: list[Task] = []  # [task_id, ...]
        self.handling_tasks: list[Task] = []
        self.query_interval = 3
        threading.Thread(target=self.__put_task_thread).start()

    def _join_task(self, prompt: str, callback: callable):
        self.lock.acquire()
        self.tasks.append(Task(callback=callback, prompt=prompt))
        self.lock.release()

    def __put_task_thread(self):
        while True:
            time.sleep(0.1)
            self.lock.acquire()
            if len(self.tasks) == 0:
                self.lock.release()
                continue
            if len(self.handling_tasks) == self.max_concurrency:
                self.lock.release()
                continue
            if self.tasks:
                task = self.tasks.pop(0)
                try:
                    self._post_task(task)
                    self.handling_tasks.append(task)
                except:
                    traceback.print_exc()
            self.lock.release()
            # self._post_task(task)

    @abstractmethod
    def _get_tasks(self, task_ids: list[str]) -> dict:
        pass

    def __handle_finished_task(self, task: Task):
        img_paths = []
        for img_url in task.img_urls:
            img_paths.append(self._handle_img(img_url))
        task.callback(img_paths)

    def _handle_img(self, img_url: str) -> str:
        img_path = download2temp(img_url, ".png")
        # todo: 检查图片是否违规，违规的要打码
        if ifnude.detect(img_path):
            return ""
        return img_path

    def run(self) -> None:
        while True:
            time.sleep(self.query_interval)
            self.lock.acquire()
            task_ids = [t.task_id for t in self.handling_tasks]
            if not task_ids:
                self.lock.release()
                continue
            try:
                res_tasks = self._get_tasks(task_ids)
            except:
                traceback.print_exc()
                self.lock.release()
                continue
            # for task_id, task in res_tasks.items():
            for task in self.handling_tasks:
                status = res_tasks.get(task.task_id, {}).get("status")
                logger.info(
                    f"task {task.prompt} status: {status} progress: {res_tasks[task.task_id]['items'][0]['processPercent']}")
                if status == "FINISH":
                    task.finished = True
                    task.img_urls = [item["url"] for item in res_tasks[task.task_id]["items"]]
                # task.progress = res_tasks[task.task_id]["processPercent"]
            finished_tasks = filter(lambda t: t.finished, self.handling_tasks)
            for task in finished_tasks:
                threading.Thread(target=lambda: self.__handle_finished_task(task)).start()
                self.handling_tasks.remove(task)

            self.lock.release()

    @abstractmethod
    def _post_task(self, task: Task):
        pass


class TusiDraw(AIDrawBase, TaskStatusListener):
    def __init__(self, token: str):
        super().__init__()
        self.base_prompt = ""
        TaskStatusListener.__init__(self)
        self.models = [
            DrawModel(name="sdxl0.9", model_id="611736766128336332", model_file_id="611736766127287757"),
            DrawModel(name="动漫风", model_id="603766951782701925", model_file_id="603766951781653350"),
            DrawModel(name="真人3D", model_id="603003048899406426", model_file_id="603003048898357851"),
        ]
        self.model = self.models[0]
        # token =
        self.base_url = "https://api.tusi.art"
        self.session.cookies.set("ta_token_prod", token)
        self.start()

    def txt2img(self, txt: str, callback: Callable[[list[str]], None]):
        if is_chinese(txt):
            txt = trans(txt)
        self._join_task(txt, callback)
        # img_url = self.__get_image(task_id)
        # return img_url

    def get_models(self) -> str:
        return "模型列表：\n" + "\n".join([f"{'当前' if m == self.model else ''}模型名：{m.name}" for m in self.models])

    def set_model(self, model_name: str) -> str:
        model = list(filter(lambda m: model_name in m.name, self.models))
        if not model:
            return f"模型{model_name}不存在"
        self.model = model[0]
        return f"模型已切换为{self.model.name}"

    def _post_task(self, task: Task):
        res = self._api_post("/works/v1/works/task", {
            "params": {
                "baseModel": {
                    "modelId": self.model.model_id,
                    "modelFileId": self.model.model_file_id,
                },
                "sdxl": {
                    "refiner": False
                },
                "models": [],
                "sdVae": "Automatic",
                "prompt": self.base_prompt + task.prompt,
                "negativePrompt": self.negative_prompt,
                "height": 1024,
                "width": 1024,
                "imageCount": 1,
                "steps": 20,
                "samplerName": "DPM++ 2M Karras",
                "images": [],
                "cfgScale": 7,
                "seed": "-1",
                "clipSkip": 2,
                "etaNoiseSeedDelta": 31337
            },
            "credits": 1,
            "taskType": "TXT2IMG"
        })
        if res.get("code") == '0':
            task_id = res["data"]["task"]["taskId"]
            task.task_id = task_id
        else:
            raise Exception(res.get("message"))

    def _get_tasks(self, task_ids: list[str]) -> dict:
        res = self._api_post(f"/works/v1/works/mget_task",
                             {"ids": task_ids})
        if res.get("code") == "0":
            tasks = res["data"]["tasks"]
            if not tasks:
                raise Exception("task not found")
            return tasks
            # status = task.get("status")
            # if status == "FINISH":
            #     return task["items"][0]["url"]
            # else:
            #     time.sleep(2)
            #     return self.__get_image(task_id)
        raise Exception(res.get("message"))

    def __get_image(self, task_id: str) -> list[str]:
        """
        阻塞方式检查任务状态
        :param task_id: 任务id
        :return: 图片的url
        """
        res = self._api_post(f"/works/v1/works/mget_task",
                             {"ids": [task_id]})
        if res.get("code") == "0":
            task = res["data"]["tasks"].get(task_id, {})
            if not task:
                raise Exception("task not found")
            status = task.get("status")
            if status == "FINISH":
                return [item["url"] for item in task["items"]]
            else:
                time.sleep(self.query_interval)
                return self.__get_image(task_id)
        raise Exception(res.get("message"))

    def get_loras(self):
        return "暂无lora"


class MultipleCountPool:
    tokens = [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjYxNTg2OTMwMjA1ODM1OTMzOCwiZGV2aWNlSWQiOiIyMDI1NTUiLCJyZWZyZXNoVG9rZW4iOiJOV1UzTWpNME9EUXpPVE15T0RReFlYbXNMU3R4NnM0Vy9qZmJVVnV1NEgzUzgzU1M1bVR6c1cxSFVUd3plYmQwSGwxZVZ3PT0iLCJleHBpcmVUaW1lIjoyNTkyMDAwLCJleHAiOjE2OTIyNTcyNDZ9.Mhw0LH1vNY4yKVa2vcCqdY1wksrSsuhmjChrtHwgDEQ",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjYxODE0NjQ1MDc2ODk3NzM3MSwiZGV2aWNlSWQiOiIyMDYwNDgiLCJyZWZyZXNoVG9rZW4iOiJOV1UzTWpNME9EUXpPVE15T0RReFlYbXNJQ0p6NWNrVC9ERFlVVkdzN24zVytuU1M1bUQyc0dCSFVUd3plTHgzSGx0WlZ3PT0iLCJleHBpcmVUaW1lIjoyNTkyMDAwLCJleHAiOjE2OTI3ODc0MzZ9.UPHYfUDE1F8jPNGf0ePFgZiDSJRiMK0i7IbVHS4sS3Q"
    ]

    def __init__(self):
        self.threads = [TusiDraw(token) for token in self.tokens]

    def txt2img(self, txt: str, callback: Callable[[list[str]], None]):
        # threads进行排序，按照任务数从小到大排序
        self.threads.sort(key=lambda x: len(x.tasks))
        # 任务数最少的线程进行任务
        self.threads[0].txt2img(txt, callback)
