import dataclasses
import threading
import time
import traceback
from abc import abstractmethod
from typing import Callable

import ifnude

from common.utils.downloader import download2temp
from .base import AIDrawBase


@dataclasses.dataclass()
class DrawModel:
    name: str
    model_id: str
    model_file_id: str
    cover: str = None


@dataclasses.dataclass()
class Task:
    task_id: str
    callback: Callable[[list[str]], None]
    finished: bool = False
    # status: str = ""
    img_urls: list[str] = None
    # prompt: str = ""
    # progress: int = 0


class TaskStatusListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.task_list: list[Task] = []  # [task_id, ...]
        self.query_interval = 3

    def _join_task(self, task_id: str, callback: callable):
        self.lock.acquire()
        self.task_list.append(Task(task_id, callback))
        self.lock.release()

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
            task_ids = [t.task_id for t in self.task_list]
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
            for task in self.task_list:
                status = res_tasks.get(task.task_id, {}).get("status")
                if status == "FINISH":
                    task.finished = True
                    task.img_urls = [item["url"] for item in res_tasks[task.task_id]["items"]]
                # task.progress = res_tasks[task.task_id]["processPercent"]
            finished_tasks = filter(lambda t: t.finished, self.task_list)
            for task in finished_tasks:
                threading.Thread(target=lambda: self.__handle_finished_task(task)).start()
                self.task_list.remove(task)

            self.lock.release()


class TusiDraw(AIDrawBase, TaskStatusListener):
    def __init__(self):
        super().__init__()
        TaskStatusListener.__init__(self)
        self.models = [
            DrawModel(name="真人3D", model_id="603003048899406426", model_file_id="603003048898357851"),
            DrawModel(name="动漫风", model_id="601420727112962175", model_file_id="601420727111913600"),
        ]
        self.model = self.models[0]
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjYxNTg2OTMwMjA1ODM1OTMzOCwiZGV2aWNlSWQiOiIyMDI1NTUiLCJyZWZyZXNoVG9rZW4iOiJOV1UzTWpNME9EUXpPVE15T0RReFlYbXNMU3R4NnM0Vy9qZmJVVnV1NEgzUzgzU1M1bVR6c1cxSFVUd3plYmQwSGwxZVZ3PT0iLCJleHBpcmVUaW1lIjoyNTkyMDAwLCJleHAiOjE2OTIyNTcyNDZ9.Mhw0LH1vNY4yKVa2vcCqdY1wksrSsuhmjChrtHwgDEQ"
        self.base_url = "https://api.tusi.art"
        self.session.cookies.set("ta_token_prod", token)
        self.start()

    def txt2img(self, txt: str, callback: Callable[[list[str]], None]):
        task_id = self.__post_task(txt, callback)
        # img_url = self.__get_image(task_id)
        # return img_url

    def get_models(self) -> str:
        return "模型列表：" + "\n".join([f"{'当前' if m == self.model else ''}模型名：{m.name}" for m in self.models])

    def set_model(self, model_name: str) -> str:
        model = list(filter(lambda m: model_name in m.name, self.models))
        if not model:
            return f"模型{model_name}不存在"
        self.model = model[0]
        return f"模型已切换为{self.model.name}"

    def __post_task(self, txt: str, callback: Callable[[list[str]], None]):
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
                "prompt": self.base_prompt + txt,
                "negativePrompt": self.negative_prompt,
                "height": 768,
                "width": 512,
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
            self._join_task(task_id, callback=callback)
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

    def __get_image(self, task_id: str) -> str:
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
                return task["items"][0]["url"]
            else:
                time.sleep(self.query_interval)
                return self.__get_image(task_id)
        raise Exception(res.get("message"))

    def get_loras(self):
        return "暂无lora"
