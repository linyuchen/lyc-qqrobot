# coding=UTF8

import threading
import time
from dataclasses import dataclass
from typing import List
from qqsdk.message.msghandler import MsgHandler
from queue import Queue
from qqsdk.message.friendmsg import FriendMsg, BaseMsg
from qqsdk.message.groupmsg import GroupMsg
from qqsdk.qqclient import QQClientBase

Thread = threading.Thread


class EventListener(Thread):
    MESSAGE_CLASSES = (FriendMsg, GroupMsg)
    interval = 0.5
    msgs = Queue()
    running = True

    def __init__(self, qq_client: QQClientBase, msg_handlers: List[MsgHandler]):
        self.qq_client = qq_client
        self.msg_handlers = msg_handlers
        super(EventListener, self).__init__()

    def add_msg(self, msg: BaseMsg):
        self.msgs.put(msg)

    def pause(self):
        self.running = False

    def restore(self):
        self.running = True
    
    def run(self):
        while True:
            msg: BaseMsg = self.msgs.get()
            while msg.paused:
                pass
            for handler in self.msg_handlers:
                if msg.is_over:
                    break
                handler: MsgHandler
                if handler.check_type(msg):
                    handler.handle(msg)
            time.sleep(self.interval)
