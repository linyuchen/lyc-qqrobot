# coding=UTF8

import os
import nonebot
from client.nonebot import config
from qqsdk.qqclient import QQClientBase


class QQClient(QQClientBase):
    def __init__(self):
        super(QQClient, self).__init__()
        self.bot = nonebot.get_bot()

    def send_msg(self, qq: str, content: str, is_group=False):
        if is_group:
            self.bot.send_group_msg(qq, content)
        else:
            self.bot.send_private_msg(qq, content)


if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(os.path.join(os.path.dirname(__file__), "plugins"), "client.nonebot.plugins")
    nonebot.run(host='127.0.0.1', port=9080)


