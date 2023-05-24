import sys
import os
from typing import List

import requests
from flask import Flask, request, Response, json

from qqsdk import entity
from qqsdk.message import GroupMsg, FriendMsg

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from qqsdk.qqclient import QQClientBase


class MiraiQQClient(QQClientBase):
    api_url = "http://localhost:8080"
    api_session_key = ""

    def __init__(self, qq: int):
        super().__init__()
        self.qq_user.qq = qq
        self.__verify()
        self.get_friends()

    def api_get(self, path: str, data: dict = {}):
        data.update({"sessionKey": self.api_session_key})
        res = requests.get(self.api_url + path, params=data)
        return res

    def api_post(self, path, data: dict):
        data.update({"sessionKey": self.api_session_key})
        res = requests.post(self.api_url + path, json=data)
        return res

    def __verify(self):
        r = requests.post(self.api_url + "/verify", json={"verifyKey": "1234567890"})
        self.api_session_key = r.json().get("session")
        res = self.api_post("/bind", {"qq": self.qq_user.qq})
        return res

    def send_msg(self, qq: str, content: str, is_group=False):
        path = "/sendFriendMessage"
        if is_group:
            path = '/sendGroupMessage'
        res = self.api_post(path,
                            {"target": int(qq),
                             "messageChain": [{"type": "Plain",
                                              "text": content}]})
        return res

    def get_friends(self) -> List[entity.Friend]:
        res = self.api_get("/friendList")
        data = res.json().get("data")
        for f in data:
            friend = entity.Friend(qq=str(f["id"]), nick=f["nickname"], mark_name=f["remark"])
            self.qq_user.friends.append(friend)
        return self.qq_user.friends

    def get_groups(self) -> List[entity.Group]:
        res = self.api_get("/groupList")
        data = res.json().get("data")
        for g in data:
            group = entity.Group(qq=str(g["id"]), name=g["name"], members=[])
            member_list_data = self.api_get("/memberList", {"target": group.qq}).json().get("data")
            for member_data in member_list_data:
                group_member = entity.GroupMember(qq=str(member_data["id"]), nick=member_data["memberName"],
                                                  card="")
                group.members.append(group_member)
            self.qq_user.groups.append(group)
        return self.qq_user.groups

    def get_msg(self):
        data = request.json
        message_type = data.get("type")
        msg = data.get("messageChain")[1].get("text", "")
        if message_type == "FriendMessage":
            friend = self.get_friend(str(data["sender"]["id"]))
            msg = FriendMsg(friend=friend, msg=msg)
            msg.reply = lambda _msg: self.send_msg(friend.qq, _msg)
            self.add_msg(msg)
        elif message_type == "GroupMessage":
            group_qq = str(data["sender"]["group"]["id"])
            group_member_qq = str(data["sender"]["id"])
            group = self.get_group(group_qq)
            group_member = group and group.get_member(group_member_qq) or None
            if not group_member or not group:
                self.get_groups()
                group = self.get_group(group_qq)
                group_member = group.get_member(group_member_qq)
            msg = GroupMsg(group=group, msg=msg, group_member=group_member)
            msg.reply = lambda _msg: self.send_msg(group.qq, _msg, is_group=True)
            self.add_msg(msg)
        return {}


MiraiQQClient(qq=int(sys.argv[1])).start()
