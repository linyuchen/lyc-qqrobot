# coding=UTF8

import math
import time
import os
import nonebot
import asyncio
from typing import List
from qqsdk import entity
from client.nonebot import config
from qqsdk.qqclient import QQClientBase


class QQClient(QQClientBase):
    def __init__(self):
        super(QQClient, self).__init__()
        self.bot = nonebot.get_bot()

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.get_friends())
        self.loop.run_until_complete(self.get_groups())

    async def send_msg(self, qq: str, content: str, is_group=False):

        max_length = 150
        num = math.ceil(len(content) / float(max_length))
        for i in range(int(num)):
            msg = content[i * max_length: (i + 1) * max_length]
            if is_group:
                await self.bot.send_group_msg(group_id=qq, message=msg)
            else:
                await self.bot.send_private_msg(user_id=qq, message=msg)
            time.sleep(0.3)

    async def get_friends(self) -> List[entity.Friend]:
        self.qq_user.friends = []
        friends = await self.bot.get_friend_list()
        for f in friends:
            friend = entity.Friend(qq=str(f["user_id"]), nick=f["nickname"], mark_name=f["remark"])
            self.qq_user.friends.append(friend)

    async def get_groups(self) -> List[entity.Group]:
        self.qq_user.groups = []
        groups = await self.bot.get_group_list()
        for g in groups:
            group = entity.Group(qq=str(g["group_id"]), name=g["group_name"], members=[])
            member_list_data = await self.bot.get_group_member_list(group_id=group.qq)
            for member_data in member_list_data:
                group_member = entity.GroupMember(qq=str(member_data["user_id"]), nick=member_data["nickname"],
                                                  card=member_data["card"])
                group.members.append(group_member)
            self.qq_user.groups.append(group)


if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(os.path.join(os.path.dirname(__file__), "plugins"), "client.nonebot.plugins")
    nonebot.run()
