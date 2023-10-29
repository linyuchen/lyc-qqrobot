import requests
from pydantic import BaseModel

from qqsdk import entity
from qqsdk.message import MessageSegment
from qqsdk.qqclient import QQClientBase
from config import get_config


class SatoriUser(BaseModel):
    id: str
    name: str = ""
    avatar: str = ""
    is_bot: bool = False


class SatoriGuild(BaseModel):
    id: str
    name: str = ""
    avatar: str = ""

class SatoriGuildMember(BaseModel):
    user: SatoriUser = None
    name: str = ""
    avatar: str = ""
    join_at: int = None

class SatoriQQClient(QQClientBase):
    def __init__(self, qq: str):
        self.qq_user.qq = qq
        super().__init__()
        self.host = get_config("SATORI_HOST")

    def __post(self, url, data: dict = None) -> dict | list[dict]
        resp = requests.post(self.host + url, json=data).json()
        return resp

    def get_friends(self) -> list[entity.Friend]:
        resp: list[dict] = self.__post("/friend.list")
        users = [SatoriUser(**i) for i in resp]
        friends = [entity.Friend(qq=i.id, nick=i.name, mark_name=i.name) for i in users]
        return friends


    def get_groups(self) -> list[entity.Group]:
        resp: list[dict] = self.__post("/guild.list")
        guilds = [SatoriGuild(**i) for i in resp]
        groups = []
        for guild in guilds:
            resp = self.__post("/guild.member.list", {"guild_id": guild.id})
            satori_members = [SatoriGuildMember(**i) for i in resp]
            members = []
            for satori_member in satori_members:
                member = entity.GroupMember(qq=satori_member.user.id, nick=satori_member.name)
                members.append(member)

            group = entity.Group(qq=guild.id, name=guild.name, members=members)
            groups.append(group)

        return groups

    def get_msg(self, data: dict):
        pass

    def send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        pass
