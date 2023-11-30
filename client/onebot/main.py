import base64
import sys
import tempfile
from abc import ABC
from functools import reduce
from pathlib import PurePath, Path
from typing import Type, Union

import requests
from flask import request, Flask

sys.path.append(str(PurePath(__file__).parent.parent.parent))

from client.onebot.onebot_typing import OnebotRespNewMessage, OnebotRespGroupMember, OnebotRespFriend, OnebotRespGroup, \
    MessageItemType
from config import get_config
from qqsdk.entity import GroupMember, Friend, Group
from qqsdk.message import MessageSegment, GroupMsg, GroupSendMsg, GeneralMsg
from qqsdk.qqclient import QQClientBase


# MessageSegment.to_data = MessageSegment.to_onebot_data


class Onebot11QQClient(ABC, QQClientBase):
    def __init__(self, qq: str):
        super().__init__()
        self.qq_user.qq = qq
        self.host = get_config("ONEBOT_HTTP_API")

    def __post(self, url, data: dict = None) -> dict | list[dict]:
        resp = requests.post(self.host + url, json=data).json()
        return resp

    def recall_msg(self, msg_id: str):
        resp = self.__post("/delete_msg", {
            "message_id": msg_id
        })

    def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        if isinstance(content, str):
            content = MessageSegment.text(content)
        message = content.onebot11_data
        post_data = {
            "group_id": qq if is_group else None,
            "user_id": qq,
            "message": message
        }
        if is_group:
            path = "/send_group_msg"
        else:
            path = "/send_private_msg"
        resp = self.__post(path, post_data)

    def get_friends(self) -> list[Friend]:
        resp = self.__post("/", {
            "action": "get_friend_list",
        })
        friends: list[OnebotRespFriend] = resp["data"]
        self.qq_user.friends = [Friend(qq=i["user_id"], nick=i["user_name"]) for i in friends]
        return self.qq_user.friends

    def get_groups(self) -> list[Group]:
        resp = self.__post("/", {
            "action": "get_group_list",
        })
        groups: list[OnebotRespGroup] = resp["data"]
        self.qq_user.groups = [Group(qq=i["group_id"], name=i["group_name"], members=[]) for i in groups]
        return self.qq_user.groups

    def get_group_members(self, group_qq: str):
        resp = self.__post("/", {
            "action": "get_group_member_list",
            "params": {"group_id": group_qq}
        })
        members: list[OnebotRespGroupMember] = resp["data"]
        group = self.get_group(group_qq)
        group.members = [GroupMember(
            qq=i["user_id"],
            nick=i["user_name"],
            card=i["user_display_name"]
        ) for i in members]

    def get_msg(self, data: OnebotRespNewMessage):
        if data["detail_type"] == "group":
            group = self.get_group(data["group_id"])
            group_member = group.get_member(data["user_id"])
            if not group_member:
                self.get_group_members(data["group_id"])
                group_member = group.get_member(data["user_id"])
                if not group_member:
                    return

            is_at_me = False
            is_at_other = False
            at_member = None
            message_segments = []
            msg_text = ""
            quote_msg: GeneralMsg | None = None
            for resp_message in data["message"]:
                match resp_message["type"]:
                    case MessageItemType.text:
                        msg_text += resp_message["data"]["text"]
                        message_segments.append(MessageSegment.text(resp_message["data"]["text"]))
                    case MessageItemType.at:
                        at_qq = resp_message["data"].get("qq") or resp_message["data"].get("mention")
                        is_at_me = at_qq == self.qq_user.qq
                        is_at_other = not is_at_me
                        at_member = group.get_member(at_qq)
                        message_segments.append(MessageSegment.at(at_qq, is_at_me, is_at_other))
                    case MessageItemType.image:
                        image_uri = resp_message["data"]["file"]
                        if image_uri.startswith("base64://,"):
                            image_data = image_uri.split("base64://,")[1]
                            image_path = Path(tempfile.mktemp(suffix=".png"))
                            image_path.write_bytes(base64.b64decode(image_data))
                            message_segments.append(MessageSegment.image_path(image_path))
                        elif image_uri.startswith("file://"):
                            image_path = image_uri.split("file://")[1]
                            message_segments.append(MessageSegment.image_path(image_path))
                    case MessageItemType.reply:
                        reply_msg_id = resp_message["data"].get("id")
                        quote_msg = self.get_history_msg(reply_msg_id)
                        message_segments.append(MessageSegment.reply(reply_msg_id))
            msg_chain = reduce(lambda a, b: a + b, message_segments) if message_segments else None
            if group_member.qq == self.qq_user.qq:
                group_msg_class = GroupSendMsg
            else:
                group_msg_class = GroupMsg
            group_msg = group_msg_class(
                group=group,
                group_member=group_member,
                msg=msg_text,
                quote_msg=quote_msg,
                msg_chain=msg_chain,
                is_at_me=is_at_me,
                is_at_other=is_at_other,
                at_member=at_member,
                msg_id=data["message_id"])

            def reply(content, at=True, quote=True):
                if isinstance(content, str):
                    content = MessageSegment.text(content)
                if not list(filter(lambda ms: ms["type"] == "voice", content.onebot11_data)):
                    if quote:
                        content = MessageSegment.reply(group_msg.msg_id) + content
                # if at:
                #     content = MessageSegment.at(group_member.qq) + MessageSegment.text("\n") + content
                self.send_msg(group.qq, content, is_group=True)

            group_msg.reply = reply
            group_msg.recall = lambda: self.recall_msg(group_msg.msg_id)
            self.add_msg(group_msg)


class QQClientFlask:
    _flask_app = Flask(__name__)

    def __init__(self):
        self._flask_app.add_url_rule("/", view_func=self.get_msg, methods=["POST"])
        self.qq_clients: [str, Onebot11QQClient] = {}

    def get_msg(self):
        json_data: OnebotRespNewMessage = request.json
        qq = json_data["self"]["user_id"]
        client: Onebot11QQClient = self.qq_clients[qq]
        client.get_msg(json_data)

        return {}

    def start(self) -> None:
        for qq in get_config("QQ"):
            client = Onebot11QQClient(str(qq))
            self.qq_clients[str(qq)] = client
            client.start()
        self._flask_app.run(host="0.0.0.0", port=get_config("LISTEN_PORT"))


QQClientFlask().start()
