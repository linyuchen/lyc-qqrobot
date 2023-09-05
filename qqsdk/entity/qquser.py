# coding=UTF8
from dataclasses import dataclass
from typing import List


from qqsdk.entity.friend import Friend
from qqsdk.entity.group import Group


@dataclass
class QQUser:
    """
    """
    friends: List[Friend]
    groups: List[Group]
    qq: str = ""
    nick: str = ""
    gtk: str = ""  # 用来直接打开腾讯相关网页的密钥
