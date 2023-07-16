# coding=utf8
from typing import Tuple, Type
from qqsdk.message.basemsg import BaseMsg


class MsgHandler:
    name = "base handler"
    desc = ""  # 描述
    qq_client: "qqsdk.qqclient.QQClientBase"
    is_async = False
    bind_msg_types: Tuple[Type[BaseMsg]] = ()

    def __init__(self, qq_client: "qqsdk.qqclient.QQClientBase" = None):
        self.qq_client = qq_client

    def check_type(self, msg: BaseMsg):
        return isinstance(msg, self.bind_msg_types)

    def handle(self, msg: BaseMsg):
        pass

    def get_module_name(self):
        return self.__module__.split(".")[1]