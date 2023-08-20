# coding=UTF8

import threading
import time
import traceback
from queue import Queue
from typing import List

import config
from qqsdk.message import GroupMsg
from qqsdk.message.friendmsg import BaseMsg
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

    def add_msg(self, msg: BaseMsg):
        self.msgs.put(msg)

    def pause(self):
        with self.thread_lock:
            self.running = False

    def restore(self):
        with self.thread_lock:
            self.running = True

    def run(self):
        while self.running:
            msg: BaseMsg = self.msgs.get()
            for handler in self.msg_handlers:
                paused_secs = 0
                while msg.is_paused:
                    paused_secs += 1
                    if paused_secs >= 30:
                        break
                    time.sleep(1)
                if msg.is_over:
                    break
                handler: MsgHandler
                handler_plugin_name = handler.get_module_name()
                enabled = config.plugins[handler_plugin_name].get("enabled", True)
                if not enabled:
                    continue
                if isinstance(msg, GroupMsg):
                    exclude_groups = config.plugins[handler_plugin_name].get("exclude_groups", [])
                    exclude_groups = map(str, exclude_groups)
                    if msg.group.qq in exclude_groups:
                        continue
                if handler.check_type(msg):
                    try:
                        if handler.is_async:
                            threading.Thread(target=lambda: handler.handle(msg)).start()
                        else:
                            handler.handle(msg)
                    except Exception:
                        msg.resume()
                        traceback.print_exc()

            time.sleep(self.interval)
