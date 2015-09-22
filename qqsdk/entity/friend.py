# coding=UTF8


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
    def __init__(self):

        self.uin = 0
        self.nick = ""
        self.markName = ""
        self.ip = 0
        self.status = None
        self.groupId = 0
        self.groupName = ""
        self.clientType = None
        self.gender = ""

    def __getattr__(self, name):

        if "qq" == name:
            return self.getQQ(self.uin)

    def getQQ(self, uin):
        """
        返回QQ号(int)
        """
        return self.qq

    def getName(self):
        """
        有备注则返回备注，无则返回昵称
        """

        return self.markName or self.nick
