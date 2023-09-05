# -*- coding: UTF8 -*-
from dataclasses import dataclass
from typing import List

from qqsdk.entity.avatar import Avatar


@dataclass
class GroupMember(object):
    """
    """

    qq: str
    nick: str
    card: str = ""  # 名片
    is_admin: bool = False
    is_creator: bool = False  # 是否是群主
    status = None  # 登录状态，具体有哪些类型目前不明
    last_speak_time: int = 0  # 上一次发言的时间戳
    age: int = 0
    gender: int = 0  # 0是未知，1是男，2是女？
    __avatar: Avatar = None
    # 以下字段已弃用
    ip: str = ""  # 已弃用
    uin: str = ""  # 群成员临时号码，已经弃用

    def get_name(self):
        """
        有群名片则返回群名片，
        无则返回昵称
        """
        return self.card or self.nick

    @property
    def avatar(self):
        if not self.__avatar:
            self.__avatar = Avatar(self.qq)
        return self.__avatar


@dataclass
class Group(object):
    """
    群
    """
    qq: str
    name: str  # 群名
    members: List[GroupMember]
    creator: GroupMember = None  # 群主
    create_time: int = 0  # 群创建时间戳
    mask: int = 0  # 群消息设置 0 接收并提醒，1 接收不提醒，2 不接受
    member_count: int = 0  # 群员人数
    level: int = 0  # 群等级
    description: str = ""  # 群简介
    notice: str = ""  # 当前显示的群公告
    mark_name: str = ""  # 群备注
    # 以下字段已弃用
    uin: str = ""
    code: str = ""

    def get_member(self, qq: str):
        for member in self.members:
            if member.qq == qq:
                return member
