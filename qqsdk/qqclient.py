# coding=UTF8
import importlib
import os
import pathlib
import sys
from abc import ABCMeta, abstractmethod, ABC
from flask import Flask

import config
from qqsdk import entity
from qqsdk.eventlistener import EventListener
from qqsdk.message import MsgHandler
from qqsdk.message.segment import MessageSegment


class QQClientBase(EventListener, metaclass=ABCMeta):

    def __init__(self):
        super(QQClientBase, self).__init__()
        self.qq_user = entity.QQUser(friends=[], groups=[])
        self.online = True
        self.msg_handlers = self.get_plugins()

    def get_plugins(self) -> list[MsgHandler]:
        handlers_class = []
        plugins_path = pathlib.PurePath(__file__).parent.parent / "msgplugins"
        sys.path.append(str(plugins_path))
        for module_name in os.listdir(plugins_path):
            if module_name.endswith(".py"):
                module_name = module_name[:-3]
            b = importlib.import_module(f".{module_name}", "msgplugins")
            for v in dir(b):
                if v == "MsgHandler":
                    continue
                class_ = getattr(b, v)
                if type(class_) == type(type) and issubclass(class_, MsgHandler):
                    handlers_class.append(class_(self))

        return handlers_class

    def start(self) -> None:
        super().start()

    @abstractmethod
    def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        pass

    def get_friends(self) -> list[entity.Friend]:
        """
        获取好友，结果将放在self.qq_user.friends里面
        """

    def get_groups(self) -> list[entity.Group]:
        """
        结果保存在 self.qq_user.groups
        """

    @abstractmethod
    def get_msg(self):
        raise NotImplementedError

    def get_group(self, group_qq: str) -> entity.Group:
        result = list(filter(lambda g: g.qq == group_qq, self.qq_user.groups))
        return result and result[0] or None

    def __get_friend(self, qq: str) -> entity.Friend | None:
        result = list(filter(lambda f: f.qq == qq, self.qq_user.friends))
        return result and result[0] or None

    def get_friend(self, qq: str) -> entity.Friend:
        friend = self.__get_friend(qq)
        if not friend:
            self.get_friends()
            friend = self.__get_friend(qq)
        return friend


class QQClientFlask(QQClientBase, ABC):
    _flask_app = Flask(__name__)

    def __init__(self):
        super().__init__()
        self._flask_app.add_url_rule("/", view_func=self.get_msg, methods=["POST"])

    def start(self) -> None:
        super().start()
        self._flask_app.run(host="0.0.0.0", port=config.LISTEN_PORT)
