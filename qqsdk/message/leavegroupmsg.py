#coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg


class GroupRemoveMeMsg(BaseMsg):
    """
    我被踢出群的消息
    self.groupQQ： 群号
    self.adminUin：踢我的管理员uin
    self.adminName：踢我的管理员昵称
    """

    def __init__(self, groupQQ, adminQQ, adminName):

        super(GroupRemoveMeMsg, self).__init__()

        self.groupQQ = groupQQ
        self.adminUin = adminQQ
        self.adminName = adminName


class GroupRemoveMemberMsg(BaseMsg):

    def __init__(self, group, groupAdmin, memberQQ, memberName):

        super(GroupRemoveMemberMsg, self).__init__()

        self.group = group
        self.memberName = memberName
        self.memberQQ = memberQQ
        self.groupAdmin = groupAdmin


class GroupMemberExitMsg(basemsg.BaseMsg):
    """
    self.group: entity.group.Group实例,发送者所在的群
    self.memberName: 退群者昵称
    self.memberQQ: 退群者QQ
    """

    def __init__(self, group, memberName, memberQQ):

        super(GroupMemberExitMsg, self).__init__()

        self.group = group
        self.memberName = memberName
        self.memberQQ = memberQQ
