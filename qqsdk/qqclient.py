# coding=UTF8
import sys
import os
import math
import time
import importlib
from typing import List, Type
from qqsdk import entity
from qqsdk.message import MsgHandler
from qqsdk.eventlistener import EventListener


class QQClientBase(EventListener):
    def __init__(self):
        super(QQClientBase, self).__init__()
        self.qq_user = entity.QQUser(friends=[], groups=[])
        self.online = True
        self.msg_handlers = self.get_plugins()

    def get_plugins(self) -> List[Type[MsgHandler]]:
        handlers_class = []
        plugins_path = os.path.dirname(os.path.dirname(__file__))
        plugins_path = os.path.join(plugins_path, "msgplugins")
        # sys.path.append(plugins_path)
        # b = importlib.import_module(os.path.join(plugins_path, "baike"))
        b = importlib.import_module(".baike", "msgplugins")
        b = importlib.import_module(".superplugins", "msgplugins")
        for v in dir(b):
            if v == "MsgHandler":
                continue
            class_ = getattr(b, v)
            if type(class_) == type(type) and issubclass(class_, MsgHandler):
                handlers_class.append(class_(self))

        return handlers_class

    def send_msg(self, qq: str, content: str, is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        raise NotImplementedError

    def get_friends(self) -> List[entity.Friend]:
        """
        获取好友，结果将放在self.qq_user.friends里面
        """

    def get_groups(self) -> List[entity.Group]:
        """
        结果保存在 self.qq_user.groups
        """

    def get_group(self, group_qq: str) -> entity.Group:
        for g in self.qq_user.groups:
            if g.qq == group_qq:
                return g

    def get_friend(self, qq: str) -> entity.Friend:

        for f in self.qq_user.friends:
            if f.qq == qq:
                return f

