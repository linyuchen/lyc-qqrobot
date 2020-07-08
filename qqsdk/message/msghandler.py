# coding=utf8
from typing import Tuple
from qqsdk.message.basemsg import BaseMsg
from qqsdk.归档.qqclient import QQClient


class MsgHandler:

    qq_client: QQClient
    bind_msg_types: Tuple[BaseMsg] = ()

    def __init__(self, qq_client: QQClient=None):
        self.qq_client = qq_client

    def check_type(self, msg: BaseMsg):
        return isinstance(msg, self.bind_msg_types)

    def handle(self, msg: BaseMsg):
        pass
