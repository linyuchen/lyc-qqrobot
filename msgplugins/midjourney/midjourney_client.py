import dataclasses
import json
import queue
import re
import threading
import time
from abc import abstractmethod, ABCMeta
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Callable, NewType

import pytz

from common.discord_client import DiscordSeleniumClient, Message, download_images
from common.utils.translator import is_chinese, trans

BANNED_WORDS = json.load(open(Path(__file__).parent / "banned_words.json"))
BANNED_WORDS = [word["words"].strip().lower() for word in BANNED_WORDS]

TaskCallback = NewType("TackCallback", Callable[['TaskCallbackParam'], None])


class TaskType(StrEnum):
    DRAW = "draw"
    UPSCALE = "upscale"


@dataclasses.dataclass
class Task:
    prompt: str
    datetime: datetime
    callback: TaskCallback
    username: str = ""
    reply_msg: Message = None
    task_type: TaskType = TaskType.DRAW
    upscale_index: int | None = None


@dataclasses.dataclass
class TaskCallbackResponse:
    task: Task
    error: str = ""
    reply_msg: Message = None
    image_path: list[Path] | None = None
    image_urls: list[str] = None


class MidjourneyClientBase(metaclass=ABCMeta):
    BOT_NAME = "Midjourney Bot"
    ERROR_WORDS = {
        "Banned prompt": "有违禁词",
        "Empty prompt": "提示词不能为空",
        "Invalid parameter": "参数错误",
        "Action needed to continue": "提示词可能有不良内容",
        "You have been blocked": "你已被封禁",
    }

    def __init__(self, http_proxy: str):
        self.http_proxy = http_proxy
        self._putted_tasks: queue.Queue[Task] = queue.Queue()
        self.tasks: list[Task] = []
        self._lock = threading.Lock()
        threading.Thread(target=self.__listen_cmd).start()

    @abstractmethod
    def _handle_new_task(self, task: Task):
        pass

    @abstractmethod
    def _listen_msg(self):
        pass

    def __listen_cmd(self):
        while True:
            task = self._putted_tasks.get()
            now = datetime.now(pytz.timezone('Asia/Shanghai'))
            task.datetime = now
            with self._lock:
                self.tasks.append(task)
                self._handle_new_task(task)

    def draw(self, prompt: str, callback: TaskCallback):
        prompt = prompt.lower()

        prompt = prompt.replace("\n", "")
        prompt = prompt.split("--", 1)
        params = ""
        if len(prompt) > 1:
            prompt, params = prompt
            params = " --" + params

        else:
            prompt = prompt[0]

        prompt = prompt.replace("-", " ")

        # 多个空格转成一个空格
        prompt = " ".join(prompt.split())

        # 自动加上版本
        if "--v" not in params and "--niji" not in params:
            params += " --v 5.2"
        if is_chinese(prompt):
            prompt = trans(prompt).lower()

        have_banned_words: list[str] = []
        for banned_word in BANNED_WORDS:
            if banned_word in prompt:
                have_banned_words.append(banned_word)
                prompt = prompt.replace(banned_word, "")
        task = Task(prompt=prompt, callback=callback, datetime=datetime.now())
        if not prompt:
            error = "提示词不能为空"
            if have_banned_words:
                error = " 有违禁词" + " ".join(have_banned_words)
            return callback(TaskCallbackResponse(error=error, image_path=None, task=task, reply_msg=None))
        # 特殊符号转成空格
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', ' ', prompt)
        prompt = prompt + params
        task.prompt = prompt
        self._putted_tasks.put(task)

    def __check_new_msg(self, msg: Message, task: Task) -> bool:
        """
        判断是否是新消息是否是mj的有用消息
        """
        if msg.read:
            return False
        if msg.datetime < task.datetime:
            return False
        if task.prompt.replace(" ", "") not in msg.content.replace(" ", ""):
            return False
        if msg.sender_name != self.BOT_NAME:
            return False

        return True

    def _handle_new_msg(self, reply_msg: Message):
        for task in self.tasks[:]:
            if not self.__check_new_msg(reply_msg, task):
                continue
            if reply_msg.attachment_urls:
                if "%)" in reply_msg.content:
                    continue
                reply_msg.read = True
                callback_param = TaskCallbackResponse(task=task,
                                                      reply_msg=reply_msg,
                                                      error="", image_urls=reply_msg.attachment_urls,
                                                      image_path=[])
            elif error := list(filter(lambda word: word in reply_msg.content, self.ERROR_WORDS)):
                error_msg = self.ERROR_WORDS[error[0]] + reply_msg.content
                reply_msg.read = True
                callback_param = TaskCallbackResponse(task=task, error=error_msg, image_path=None, reply_msg=reply_msg)
            else:
                continue

            with self._lock:
                self.tasks.remove(task)
            threading.Thread(target=lambda: self.__handle_callback(task, callback_param)).start()

    def __handle_callback(self, task: Task, param: TaskCallbackResponse):
        if param.image_urls:
            try:
                param.image_path = download_images(param.image_urls, self.http_proxy)
            except Exception as e:
                param.error = str(e)
        task.callback(param)


class MJSeleniumClient(MidjourneyClientBase, DiscordSeleniumClient):
    def __init__(self, url: str, token: str = "", debug_address: str = None, http_proxy: str = ""):
        MidjourneyClientBase.__init__(self, http_proxy)
        DiscordSeleniumClient.__init__(self, url, token, debug_address, http_proxy)
        threading.Thread(target=self._listen_msg).start()

    def _handle_new_task(self, task: Task):
        self.send_cmd("/imagine", task.prompt)

    def _listen_msg(self):
        while True:
            if not self.tasks:
                time.sleep(1)
                continue
            msgs = self.get_msgs()
            for msg in msgs:
                self._handle_new_msg(msg)

            time.sleep(1)