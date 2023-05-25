# coding=UTF8
import sys
import os
import math
import time
import importlib
from typing import List, Type, Union
from flask import Flask
from qqsdk import entity
from qqsdk.message import MsgHandler
from qqsdk.eventlistener import EventListener
from qqsdk.message.segment import MessageSegment


class QQClientBase(EventListener):
    _flask_app = Flask(__name__)
    listen_port = 5000

    def __init__(self):
        super(QQClientBase, self).__init__()
        self.qq_user = entity.QQUser(friends=[], groups=[])
        self.online = True
        self.msg_handlers = self.get_plugins()
        self._flask_app.add_url_rule("/", view_func=self.get_msg, methods=["POST"])

    def get_plugins(self) -> List[MsgHandler]:
        handlers_class = []
        plugins_path = os.path.dirname(os.path.dirname(__file__))
        plugins_path = os.path.join(plugins_path, "msgplugins")
        # sys.path.append(plugins_path)
        # b = importlib.import_module(os.path.join(plugins_path, "baike"))
        for m_name in ["baike", "superplugins", "bull_fight", "visual_menu", "running_time", "randomimg", "game24",
                       "game21", "genshincard"]:
            b = importlib.import_module(f".{m_name}", "msgplugins")
            for v in dir(b):
                if v == "MsgHandler":
                    continue
                class_ = getattr(b, v)
                if type(class_) == type(type) and issubclass(class_, MsgHandler):
                    handlers_class.append(class_(self))

        return handlers_class

    def start(self) -> None:
        super().start()
        self._flask_app.run(port=self.listen_port)

    def send_msg(self, qq: str, content: Union[str, MessageSegment], is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        raise NotImplementedError

    def get_friends(self) -> List[entity.Friend]:
        """
        获取好友，结果将放在self.qq_user.friends里面
        """
        # raise NotImplementedError

    def get_groups(self) -> List[entity.Group]:
        """
        结果保存在 self.qq_user.groups
        """
        # raise NotImplementedError

    def get_msg(self):
        raise NotImplementedError

    def get_group(self, group_qq: str) -> entity.Group:
        result = list(filter(lambda g: g.qq == group_qq, self.qq_user.groups))
        return result and result[0] or None

    def get_friend(self, qq: str) -> entity.Friend:
        result = list(filter(lambda f: f.qq == qq, self.qq_user.friends))
        return result and result[0] or None
