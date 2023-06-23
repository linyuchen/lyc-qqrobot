# coding=UTF8

import threading
import time
import traceback
from queue import Queue
from typing import List

from qqsdk.message.friendmsg import BaseMsg
from qqsdk.message.msghandler import MsgHandler

Thread = threading.Thread


class EventListener(Thread):
    interval = 0.1
    running = True
    msg_handlers: List[MsgHandler]

    def __init__(self):
        self.msgs = Queue()
        super(EventListener, self).__init__()

    def add_msg(self, msg: BaseMsg):
        self.msgs.put(msg)

    def pause(self):
        self.running = False

    def restore(self):
        self.running = True

    def run(self):
        while self.running:
            msg: BaseMsg = self.msgs.get()
            for handler in self.msg_handlers:
                while msg.paused:
                    pass
                if msg.is_over:
                    break
                handler: MsgHandler
                if handler.check_type(msg):
                    try:
                        if handler.is_async:
                            threading.Thread(target=lambda: handler.handle(msg)).start()
                        else:
                            handler.handle(msg)
                    except Exception:
                        traceback.print_exc()

            time.sleep(self.interval)
