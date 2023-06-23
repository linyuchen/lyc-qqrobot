# coding=utf8
from typing import Tuple, Type
from qqsdk.message.basemsg import BaseMsg


class MsgHandler:

    name = "base handler"  # 唯一性
    qq_client: None
    is_async = False
    bind_msg_types: Tuple[Type[BaseMsg]] = ()

    def __init__(self, qq_client=None):
        self.qq_client = qq_client

    def check_type(self, msg: BaseMsg):
        return isinstance(msg, self.bind_msg_types)

    def handle(self, msg: BaseMsg):
        pass
