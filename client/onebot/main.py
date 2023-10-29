from abc import ABC

import requests
from flask import request, Flask

from client.onebot.msgtype import OnebotNewMessage
from config import get_config
from qqsdk.message import MessageSegment
from qqsdk.qqclient import QQClientBase


class OnebotQQClient(QQClientBase, ABC):
    def __init__(self, qq: str):
        self.qq_user.qq = qq
        super().__init__()
        self.host = get_config("SATORI_HOST")

    def __post(self, url, data: dict = None) -> dict | list[dict]:
        resp = requests.post(self.host + url, json=data).json()
        return resp

    # def get_friends(self) -> list[entity.Friend]:
    #     resp: list[dict] = self.__post("/friend.list")
    #     users = [SatoriUser(**i) for i in resp]
    #     friends = [entity.Friend(qq=i.id, nick=i.name, mark_name=i.name) for i in users]
    #     return friends

    # def get_groups(self) -> list[entity.Group]:
    #     resp: list[dict] = self.__post("/guild.list")
    #     guilds = [SatoriGuild(**i) for i in resp]
    #     groups = []
    #     for guild in guilds:
    #         resp = self.__post("/guild.member.list", {"guild_id": guild.id})
    #         satori_members = [SatoriGuildMember(**i) for i in resp]
    #         members = []
    #         for satori_member in satori_members:
    #             member = entity.GroupMember(qq=satori_member.user.id, nick=satori_member.name)
    #             members.append(member)
    #
    #         group = entity.Group(qq=guild.id, name=guild.name, members=members)
    #         groups.append(group)
    #
    #     return groups
    def get_group_members(self, group_qq: str):
        resp = self.__post("/", {
            "action": "get_group_member_list",
            "params": {"group_id": group_qq}
        })


    def get_msg(self, data: OnebotNewMessage):
        if data["detail_type"] == "group":
            group = self.get_group(data["group_id"])
            group_member = group.get_member(data["user_id"])
            if not group_member:
                group.get_members()
                group_member = group.get_member(data["user_id"])

    def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        pass


class QQClientFlask:
    _flask_app = Flask(__name__)

    def __init__(self):
        self._flask_app.add_url_rule("/", view_func=self.get_msg, methods=["POST"])
        self.qq_clients: [str, OnebotQQClient] = {}

    def get_msg(self):
        json_data: OnebotNewMessage = request.json
        qq = json_data["self"]["self_id"]
        client: OnebotQQClient = self.qq_clients[qq]
        client.get_msg(json_data)

        return {}

    def start(self) -> None:
        for qq in get_config("QQ"):
            client = OnebotQQClient(str(qq))
            self.qq_clients[str(qq)] = client
            client.start()
        self._flask_app.run(host="0.0.0.0", port=get_config("LISTEN_PORT"))


QQClientFlask().start()
