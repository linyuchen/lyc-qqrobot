import re
import dataclasses
import queue
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, NewType

import pytz

from common.discord_client import DiscordClient, Message
from common.utils.baidu_translator import is_chinese, trans


@dataclasses.dataclass
class TaskCallbackParam:
    prompt: str
    image_path: list[Path] | None
    error: str
    image_urls: list[str] = None


TaskCallback = NewType("TackCallback", Callable[[TaskCallbackParam], None])


@dataclasses.dataclass
class Task:
    prompt: str
    datetime: datetime
    callback: TaskCallback
    username: str = ""


class MidjourneyClient(DiscordClient):
    BOT_NAME = "Midjourney Bot"
    ERROR_WORDS = [
        "Banned prompt",
        "Invalid parameter",
        "Action needed to continue",
        "You have been blocked"
    ]

    def __init__(self, url: str, token: str = "", debug_address: str = None, http_proxy: str = ""):
        super().__init__(url, token, debug_address, http_proxy)
        self.__putted_tasks: queue.Queue[Task] = queue.Queue()
        self.tasks: list[Task] = []
        self.__lock = threading.Lock()
        threading.Thread(target=self.__listen_msg).start()
        threading.Thread(target=self.__listen_cmd).start()

    def __listen_cmd(self):
        while True:
            task = self.__putted_tasks.get()
            self.send_cmd("/imagine", task.prompt)
            now = datetime.now(pytz.timezone('Asia/Shanghai'))
            task.datetime = now
            with self.__lock:
                self.tasks.append(task)

    def draw(self, prompt: str, callback: TaskCallback):
        prompt = prompt.replace("\n", "")
        prompt = prompt.split("--", 1)
        params = ""
        if len(prompt) > 1:
            prompt, params = prompt
            params = " --" + params

        else:
            prompt = prompt[0]

        prompt = prompt.replace("-", " ")
        # 特殊符号转成空格
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', ' ', prompt)
        # 多个空格转成一个空格
        prompt = " ".join(prompt.split())

        # 自动加上版本
        if "--v" not in params and "--niji" not in params:
            params += " --v 5.2"
        if is_chinese(prompt):
            prompt = trans(prompt)
        prompt = prompt + params
        task = Task(prompt=prompt, callback=callback, datetime=datetime.now())
        self.__putted_tasks.put(task)

    def __filter_msg(self, msg: Message, task: Task) -> bool:
        if msg.datetime < task.datetime:
            return False
        if task.prompt.replace(" ", "") not in msg.content.replace(" ", ""):
            return False
        if msg.sender_name != self.BOT_NAME:
            return False

        return True

    def __handle_callback(self, task: Task, param: TaskCallbackParam):
        if param.image_urls:
            try:
                param.image_path = self.download_imgs(param.image_urls)
            except Exception as e:
                param.error = str(e)
        task.callback(param)

    def __listen_msg(self):
        while True:
            if not self.tasks:
                time.sleep(1)
                continue
            # print("开始获取消息")
            msgs = self.get_msgs()
            for task in self.tasks[:]:
                reply_msgs = list(filter(lambda msg: self.__filter_msg(msg, task), msgs))
                if reply_msgs:
                    reply_msg = reply_msgs[0]
                    if not reply_msg.attachment_urls and \
                            (list(filter(lambda word: word in reply_msg.content, self.ERROR_WORDS))):
                        callback_param = TaskCallbackParam(prompt=task.prompt, error=reply_msg.content, image_path=None)
                    else:
                        # 有在画图，需要判断一下进度
                        if "%)" in reply_msg.content:
                            continue
                        callback_param = TaskCallbackParam(prompt=task.prompt,
                                                           error="", image_urls=reply_msg.attachment_urls,
                                                           image_path=[])
                    with self.__lock:
                        self.tasks.remove(task)
                    threading.Thread(target=lambda: self.__handle_callback(task, callback_param)).start()
                # 参数错误

            time.sleep(1)
