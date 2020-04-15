#coding=UTF8
from dataclasses import dataclass
from typing import List
from qqsdk.entity.fontstyle import FontStyle
from qqsdk.entity.friend import Friend
from qqsdk.entity.group import Group


@dataclass
class QQUser:
    """
    self.fontStyle: entity.FontStyle,字体实例
    self.friends : dict, key为uin，value为entity.Friend实例
    self.groups : dict, key为uin，value为entity.Group实例
    self.qq: int, QQ号
    self.gtk: string,
    self.nick: string
    """
    frineds: List[Friend]
    groups: List[Group]
    fontstyle: FontStyle = None
    qq: str = ""
    nick: str = ""
    gtk: str = ""  # 用来直接打开腾讯相关网页的密钥
