# -*- coding: UTF8 -*-
import math
import os
import sys
import requests
from flask import Flask, request, Response, json
from typing import List, Union, Sequence

from qqsdk.message.segment import MessageSegment

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from qqsdk.qqclient import QQClientBase
from qqsdk import entity
from qqsdk.message import FriendMsg, GroupMsg


class QQClient(QQClientBase):
    api_url = "http://localhost:5700"

    def __init__(self):
        super(QQClient, self).__init__()
        while True:
            try:
                self.get_friends()
                self.get_groups()
                break
            except:
                continue
    
    def send_msg(self, qq: str, content: Union[str, MessageSegment], is_group=False):
        post_data = {"message": str(content)}
        if is_group:
            post_data["group_id"] = qq
        else:
            post_data["user_id"] = qq

        if isinstance(content, str):
            max_length = 1500
            num = math.ceil(len(content) / float(max_length))
            for i in range(int(num)):
                msg = content[i * max_length: (i + 1) * max_length]
                post_data["message"] = msg

                requests.post(self.api_url + "/send_msg", post_data)
        else:
            requests.post(self.api_url + "/send_msg", post_data)

    def get_friends(self) -> List[entity.Friend]:
        friends = requests.get(self.api_url + "/get_friend_list").json().get("data", [])
        for f in friends:
            friend = entity.Friend(qq=str(f["user_id"]), nick=f["nickname"], mark_name=f["remark"])
            self.qq_user.friends.append(friend)
        return self.qq_user.friends

    def get_groups(self) -> List[entity.Group]:
        self.qq_user.groups = []
        groups = requests.get(self.api_url + "/get_group_list").json().get("data", [])
        for g in groups:
            group = entity.Group(qq=str(g["group_id"]), name=g["group_name"], members=[])
            member_list_data = requests.get(self.api_url + "/get_group_member_list?group_id=" + group.qq).json().get(
                "data", [])
            for member_data in member_list_data:
                group_member = entity.GroupMember(qq=str(member_data["user_id"]), nick=member_data["nickname"],
                                                  card=member_data["card"])
                group.members.append(group_member)
            self.qq_user.groups.append(group)
        return self.qq_user.groups

    def get_msg(self):
        data = request.get_data()
        data = json.loads(data)
        # print(data)
        message_type = data.get("message_type")
        msg = data.get("message")
        if message_type == "private":
            friend = qq_client.get_friend(str(data["sender"]["user_id"]))
            msg = FriendMsg(friend=friend, msg=msg)
            msg.reply = lambda _msg: qq_client.send_msg(friend.qq, _msg)
            qq_client.add_msg(msg)
        elif message_type == "group":
            group = qq_client.get_group(str(data.get("group_id")))
            group_member = group.get_member(str(data["sender"]["user_id"]))
            if not group_member or not group:
                qq_client.get_groups()
                group = qq_client.get_group(str(data.get("group_id")))
                group_member = group.get_member(str(data["sender"]["user_id"]))
            msg = GroupMsg(group=group, msg=msg, group_member=group_member)
            msg.reply = lambda _msg: qq_client.send_msg(group.qq, _msg, is_group=True)
            qq_client.add_msg(msg)
        return {}


qq_client = QQClient()
qq_client.start()
