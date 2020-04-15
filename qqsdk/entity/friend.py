# coding=UTF8
from dataclasses import dataclass


@dataclass
class Friend(object):
    """
        self.uin: int, 好友临时号码
        self.qq: int, 好友QQ号
        self.nick: string
        self.markName: string，备注
        self.ip: int, 登录IP，只有此好友发送了消息才能获取
        self.status: 登录状态
        self.groupId: int, 所在分组id
        self.groupName: string, 所在分组名
        self.clientType: int,客户端类型
        self.gender: string, 性别
    """
    uin: str  # 已弃用
    qq: str
    nick: str
    markName: str
    ip: int  # 已弃用
    status: any  # 登录状态，类型未知
    groupId: int  # 所在分组id
    groupName: str  # 所在分组名
    clinetType: int  # 客户端类型，有哪些值暂时未知
    gender: int  # 性别

    def get_name(self):
        """
        有备注则返回备注，无则返回昵称
        """

        return self.markName or self.nick
