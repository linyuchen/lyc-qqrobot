import base64
import json
import re
import sys
from pathlib import PurePath
from typing import List, Union

import requests
from flask import request

sys.path.append(str(PurePath(__file__).parent.parent.parent))
import config
from qqsdk import entity
from qqsdk.message import GroupMsg, FriendMsg, BaseMsg
from qqsdk.message.segment import MessageSegment
from qqsdk.qqclient import QQClientFlask


class MiraiQQClient(QQClientFlask):
    __api_url = config.MIRAI_HTTP_API
    __api_verify_key = config.MIRAI_HTTP_API_VERIFY_KEY
    __api_session_key = ""

    def __init__(self):
        super().__init__()
        self.qq_user.qq = config.QQ
        self.__verify()
        self.get_friends()

    def api_get(self, path: str, data: dict = None):
        if data is None:
            data = {}
        data.update({"sessionKey": self.__api_session_key})
        res = requests.get(self.__api_url + path, params=data)
        return res

    def api_post(self, path, data: dict):
        data.update({"sessionKey": self.__api_session_key})
        res = requests.post(self.__api_url + path, json=data)
        return res

    def __verify(self):
        r = requests.post(self.__api_url + "/verify", json={"verifyKey": self.__api_verify_key})
        self.__api_session_key = r.json().get("session")
        res = self.api_post("/bind", {"qq": self.qq_user.qq})
        return res

    def send2tim(self, qq_group_name: str, message_chain: list[dict]):
        for msg in message_chain:
            if msg["type"] in ["Image"]:
                with open(msg["path"], "rb") as f:
                    msg["data"] = base64.b64encode(f.read()).decode("utf8")
            elif msg["type"] == "Plain":
                msg["data"] = msg["text"]
            elif msg["type"] == "At":
                msg["data"] = "@" + str(msg["target"])
        post_data = {
            "qq_group_name": qq_group_name,
            "key": "linyuchen",
            "data": message_chain
        }
        res = requests.post(config.SEND2TIM_HTTP_API, json=post_data)
        
        return res

    def reply_group_msg(self, content: str | MessageSegment, msg: GroupMsg, at=True):
        if at:
            if not isinstance(content, MessageSegment):
                content = MessageSegment.text(content)
            content = MessageSegment.at(msg.group_member.qq) + content
        self.send_msg(msg.group.qq, content, is_group=True)

    def send_msg(self, qq: str, content: Union[str, MessageSegment], is_group=False):
        path = "/sendFriendMessage"
        if is_group:
            path = '/sendGroupMessage'

        message_chain = [{"type": "Plain", "text": content}]
        if isinstance(content, MessageSegment):
            message_chain = content.data

        send2tim = config.SEND2TIM
        if list(filter(lambda x: x["type"] == "Voice", message_chain)):
            send2tim = False
        if is_group and send2tim:
            res = self.send2tim(self.get_group(qq).name, message_chain)
        else:
            res = self.api_post(path,
                                {"target": int(qq),
                                 "messageChain": message_chain})
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
            my_info = self.api_get("/memberInfo", {"target": group.qq, "memberId": self.qq_user.qq}).json()
            group_member = entity.GroupMember(qq=str(self.qq_user.qq), nick=my_info["memberName"], card="")
            group.members.append(group_member)
            for member_data in member_list_data:
                group_member = entity.GroupMember(qq=str(member_data["id"]), nick=member_data["memberName"], card="")
                group.members.append(group_member)
            self.qq_user.groups.append(group)
        return self.qq_user.groups

    def get_msg(self):
        data = request.json
        message_type = data.get("type")
        msg = ""
        is_at_me = False
        for c in data.get("messageChain", []):
            msg += c.get("text", "")
            if c.get("type") == "At" and c.get("target") == self.qq_user.qq:
                is_at_me = True
            elif c.get("type") == "App":
                content = json.loads(c.get("content"))
                qq_doc_url = content["meta"]["detail_1"]["qqdocurl"]
                msg += qq_doc_url
            elif c.get("type") == "Xml":
                url = re.findall("url=\"(.*?)\"", c.get("xml"))
                if url:
                    msg += url[0]

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
                if not group_member:
                    group_member = entity.GroupMember(qq=group_member_qq, nick=group_member_qq, card="")
                    group.members.append(group_member)
            msg = GroupMsg(group=group, msg=msg, group_member=group_member, is_at_me=is_at_me)
            msg.reply = lambda _msg, at=True: self.reply_group_msg(_msg, msg, at)
            self.add_msg(msg)
        return {}


MiraiQQClient().start()
