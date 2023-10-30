# coding=UTF8
from dataclasses import dataclass

from config import get_config
from qqsdk.entity.avatar import Avatar


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
    qq: str
    nick: str
    mark_name: str = ""
    status: any = None  # 登录状态，类型未知
    group_id: int = 0  # 所在分组id
    group_name: str = ""  # 所在分组名
    gender: int = 0  # 性别
    __avatar: Avatar = None

    def get_name(self):
        """
        有备注则返回备注，无则返回昵称
        """

        return self.mark_name or self.nick

    @property
    def avatar(self):
        if not self.__avatar:
            self.__avatar = Avatar(self.qq)
        return self.__avatar

    @property
    def is_super_admin(self) -> bool:
        return self.qq in get_config("ADMIN_QQ", [])

