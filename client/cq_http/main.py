# -*- coding: UTF8 -*-
import requests
from flask import Flask, request, Response, json
from qqsdk.qqclient import QQClientBase
from qqsdk import entity
from qqsdk.message import FriendMsg, GroupMsg
from typing import List, Union, Sequence
from aiocqhttp.message import MessageSegment


class QQClient(QQClientBase):
    api_url = "http://localhost:5700"

    def __init__(self):
        super(QQClient, self).__init__()
        self.get_friends()
        self.get_groups()

    def send_msg(self, qq: str, content: Union[str, MessageSegment], is_group=False):
        post_data = {"message": str(content)}
        if is_group:
            post_data["group_id"] = qq
        else:
            post_data["user_id"] = qq

        requests.post(self.api_url + "/send_msg", post_data)

    def get_friends(self) -> List[entity.Friend]:
        friends = requests.get(self.api_url + "/get_friend_list").json().get("data", [])
        for f in friends:
            friend = entity.Friend(qq=str(f["user_id"]), nick=f["nickname"], mark_name=f["remark"])
            self.qq_user.friends.append(friend)
        return self.qq_user.friends

    def get_groups(self) -> List[entity.Group]:
        groups = requests.get(self.api_url + "/get_group_list").json().get("data", [])
        for g in groups:
            group = entity.Group(qq=str(g["group_id"]), name=g["group_name"], members=[])
            member_list_data = requests.get(self.api_url + "/get_group_member_list?group_id=" + group.qq).json().get("data", [])
            for member_data in member_list_data:
                group_member = entity.GroupMember(qq=str(member_data["user_id"]), nick=member_data["nickname"],
                                                  card=member_data["card"])
                group.members.append(group_member)
            self.qq_user.groups.append(group)
        return self.qq_user.groups


qq_client = QQClient()
app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_msg():
    data = request.get_data()
    data = json.loads(data)
    print(data)
    message_type = data.get("message_type")
    msg = data.get("message")
    if message_type == "private":
        friend = qq_client.get_friend(str(data["sender"]["user_id"]))
        msg = FriendMsg(friend=friend, msg=msg)
        msg.reply = lambda _msg: qq_client.send_msg(friend.qq, _msg)
        qq_client.add_msg(msg)
    elif message_type == "group":
        group = qq_client.get_group(str(data.get("group_id")))
        msg = GroupMsg(group=group, msg=msg, group_member=group.get_member(str(data["sender"]["user_id"])))
        msg.reply = lambda _msg: qq_client.send_msg(group.qq, _msg, is_group=True)
        qq_client.add_msg(msg)
    return {}


qq_client.start()
app.run(port="5000")
