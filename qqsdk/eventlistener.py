# coding=UTF8

import threading
import time
from typing import List
from qqsdk.message.msghandler import MsgHandler
from queue import Queue
from qqsdk.message.friendmsg import BaseMsg

Thread = threading.Thread


class EventListener(Thread):
    interval = 0.5
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
                    handler.handle(msg)
            time.sleep(self.interval)
