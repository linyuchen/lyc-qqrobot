# coding=UTF8

import threading
import time
import traceback
from queue import Queue
from typing import List

from common.logger import logger
from qqsdk.message import GeneralMsg, GroupMsg, GroupNudgeMsg
from qqsdk.message.msghandler import MsgHandler

Thread = threading.Thread


class EventListener(Thread):
    interval = 0.1
    running = True
    msg_handlers: List[MsgHandler]

    def __init__(self):
        self.msgs = Queue()
        self.thread_lock = threading.Lock()
        super(EventListener, self).__init__(daemon=True)

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
            try:
                self.__run()
            except Exception as e:
                logger.error(f"EventListener出现异常 {e}：{traceback.format_exc()}")

    def __run(self):
        # logger.debug("等待消息")
        msg: GeneralMsg = self.msgs.get()
        # logger.debug(f"收到消息 {msg.msg}")
        for handler in self.msg_handlers:
            # logger.debug(f"检查消息处理器 {handler.name}")
            if not handler.check_enabled():
                # logger.debug(f"消息处理器未启用 {handler.name}")
                continue
            if hasattr(msg, "group"):
                if not handler.check_enabled(msg.group.qq):
                    # logger.debug(f"消息处理器未在群{msg.group.name}启用 {handler.name}")
                    continue
            paused_secs = 0
            while msg.is_paused:
                paused_secs += 1
                if paused_secs >= 30:
                    break
                time.sleep(1)
            if msg.is_over:
                # logger.debug(f"消息已经处理完毕 {msg.msg}")
                break
            if handler.check_type(msg):
                # logger.debug(f"消息处理器 {handler.name} 符合消息类型，开始处理消息 {msg.msg}")
                try:
                    if handler.is_async:
                        threading.Thread(target=lambda: handler.handle(msg), daemon=True).start()
                    else:
                        handler.handle(msg)
                except Exception as e:
                    # logger.error(f"处理消息时出现异常 {e}：{traceback.format_exc()}")
                    msg.resume()
            else:
                pass
                # logger.debug(f"消息处理器 {handler.name} 不符合消息类型 {msg.msg_type}")

        time.sleep(self.interval)
