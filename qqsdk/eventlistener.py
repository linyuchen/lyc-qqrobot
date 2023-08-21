# coding=UTF8

import threading
import time
import traceback
from queue import Queue
from typing import List

from common.logger import logger
from qqsdk.message import GeneralMsg, GroupMsg
from qqsdk.message.msghandler import MsgHandler

Thread = threading.Thread


class EventListener(Thread):
    interval = 0.1
    running = True
    msg_handlers: List[MsgHandler]

    def __init__(self):
        self.msgs = Queue()
        self.thread_lock = threading.Lock()
        super(EventListener, self).__init__()

    def add_msg(self, msg: GeneralMsg):
        msg.qq_client = self
        self.msgs.put(msg)

    def pause(self):
        with self.thread_lock:
            self.running = False

    def restore(self):
        with self.thread_lock:
            self.running = True

    def run(self):
        while self.running:
            msg: GeneralMsg = self.msgs.get()
            for handler in self.msg_handlers:
                if not handler.check_enabled():
                    continue
                if isinstance(msg, GroupMsg):
                    if not handler.check_enabled(msg.group.qq):
                        continue
                paused_secs = 0
                while msg.is_paused:
                    paused_secs += 1
                    if paused_secs >= 30:
                        break
                    time.sleep(1)
                if msg.is_over:
                    break
                if handler.check_type(msg):
                    try:
                        if handler.is_async:
                            threading.Thread(target=lambda: handler.handle(msg)).start()
                        else:
                            handler.handle(msg)
                    except Exception as e:
                        logger.error(f"处理消息时出现异常 {e}：{traceback.format_exc()}")
                        msg.resume()

            time.sleep(self.interval)
