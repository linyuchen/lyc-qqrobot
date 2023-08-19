import dataclasses
import logging
import threading
import time
import traceback
from pathlib import Path
from typing import Callable

import ifnude
import requests

from common.taskpool import TaskPool, Task
from common.utils.baidu_translator import is_chinese, trans
from common.utils.downloader import download2temp

logger = logging.getLogger(__name__)


class TusiError(Exception):
    pass


@dataclasses.dataclass()
class DrawModel:
    name: str
    model_id: str
    model_file_id: str
    cover: str = None


@dataclasses.dataclass()
class TusiTask(Task):
    task_id: str = ""
    callback: Callable[[list[Path]], None] = None
    # status: str = ""
    img_urls: list[str] = None
    prompt: str = ""
    # progress: int = 0


def download_img(img_url: str) -> Path | None:
    img_path = download2temp(img_url, ".png")
    # todo: 检查图片是否违规，违规的要打码
    if ifnude.detect(str(img_path)):
        return None
    return img_path


class TusiDraw(TaskPool[TusiTask]):
    # 最高并发
    max_concurrency = 1

    def __init__(self, token: str):
        super().__init__()
        self.base_prompt = ""
        self.query_interval = 5
        self.models = [
            DrawModel(name="sdxl1.0", model_id="619188908049212188", model_file_id="619188908048163613"),
            DrawModel(name="动漫风", model_id="603766951782701925", model_file_id="603766951781653350"),
            DrawModel(name="真人3D", model_id="603003048899406426", model_file_id="603003048898357851"),
        ]
        self.model = self.models[0]
        # token =
        self.base_url = "https://api.tusi.art"
        self.session = requests.Session()
        self.session.timeout = 30
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.106 Safari/537.36"}
        self.session.cookies.set("ta_token_prod", token)
        # 余额，生成一张图片扣除一次
        self.balance = 0
        # 多久(秒)检查一次余额
        self.balance_check_interval = 60 * 10
        # 首次启动时获取一次余额
        self.__get_balance()
        threading.Thread(target=self.__get_balance_thread).start()
        self.start()

    def _api_get(self, url_path: str, params: dict = None):
        url = self.base_url + url_path
        resp = self.session.get(url, params=params)
        return resp.json()

    def _api_post(self, url_path: str, data: dict = None):
        url = self.base_url + url_path
        resp = self.session.post(url, json=data)
        return resp.json()

    def _on_task_finished(self, task: TusiTask):
        img_paths = []
        for img_url in task.img_urls:
            img_paths.append(download_img(img_url))
        task.callback(img_paths)

    def run(self) -> None:
        while True:
            time.sleep(self.query_interval)
            self._lock.acquire()
            task_ids = [t.task_id for t in self.handling_tasks if t.task_id]
            if not task_ids:
                self._lock.release()
                continue
            try:
                res_tasks = self.__get_tasks(task_ids)
            except TusiError:
                traceback.print_exc()
                self._lock.release()
                continue
            # for task_id, task in res_tasks.items():
            for task in self.handling_tasks:
                status = res_tasks.get(task.task_id, {}).get("status")
                logger.info(
                    f"task {task.prompt} "
                    f"status: {status} progress: {res_tasks[task.task_id]['items'][0]['processPercent']}")
                if status == "FINISH":
                    task.finished = True
                    task.img_urls = [item["url"] for item in res_tasks[task.task_id]["items"]]
                # task.progress = res_tasks[task.task_id]["processPercent"]

            self._lock.release()

    def __get_balance(self):
        data = self._api_get("/user-web/v1/user/credits")
        data = data["data"]
        if not data:
            return
        with self._lock:
            self.balance = data.get("dailyAmount", 0)

    def __get_balance_thread(self):
        while True:
            time.sleep(self.balance_check_interval)
            try:
                self.__get_balance()
            except TusiError:
                traceback.print_exc()

    def txt2img(self, txt: str, callback: Callable[[list[Path]], None]):
        if is_chinese(txt):
            txt = trans(txt)
        task = TusiTask(prompt=txt, callback=callback)
        self._join_task(task)

    def get_models(self) -> str:
        return "模型列表：\n" + "\n".join([f"{'当前' if m == self.model else ''}模型名：{m.name}" for m in self.models])

    def set_model(self, model_name: str) -> str:
        model = list(filter(lambda m: model_name in m.name, self.models))
        if not model:
            return f"模型{model_name}不存在"
        self.model = model[0]
        return f"模型已切换为{self.model.name}"

    def _on_handling_putted(self, task: TusiTask):
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
                "negativePrompt": "",
                "height": 1024,
                "width": 1024,
                "imageCount": 1,
                "steps": 30,
                "samplerName": "Heun",
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
            self.balance -= 1
        else:
            raise Exception(res.get("message"))

    def __get_tasks(self, task_ids: list[str]) -> dict:
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

    @staticmethod
    def get_loras():
        return "暂无lora"


class MultipleCountPool:
    from config import TUSI_TOKENS
    tokens = TUSI_TOKENS

    def __init__(self):
        self.threads = [TusiDraw(token) for token in self.tokens]

    def txt2img(self, txt: str, callback: Callable[[list[Path]], None]) -> str:
        # threads进行排序，按照任务数从小到大排序
        def sort_task(t: TusiDraw):
            size = t.tasks.qsize()
            return size - t.balance

        self.threads.sort(key=sort_task)
        # 任务数最少的线程进行任务
        available_thread = None
        for thread in self.threads:
            if thread.balance == 0:
                continue
            available_thread = thread
        if not available_thread:
            return "画图余额不足，请明天再试"
        available_thread.txt2img(txt, callback)
