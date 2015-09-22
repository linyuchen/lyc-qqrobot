# coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg


class RequestJoinGroupMsg(BaseMsg):
    """
    有人申请加群，只有管理员才能收到此消息
    要在两分钟内处理此消息，否则将被销毁
    self.group : Group实例
    self.requestQQ: int 申请者QQ
    self.uin : int，同requestQQ
    self.requestName: 申请者名字
    self.msg: 验证消息
    """
    EVENT_NAME = "RequestJoinGroup"

    def __init__(self, group, requestQQ, msg):

        super(RequestJoinGroupMsg, self).__init__()

        self.group = group
        self.requestQQ = requestQQ
        self.uin = requestQQ
        self.requestName = ""
        self.msg = msg

    def allow(self):
        """
        同意入群
        """

    def reject(self, reason):
        """
        拒绝入群
        reason: string, 拒绝理由
        """


class NewGroupMemberMsg(BaseMsg):

    """
    新成员入群
    self.group: Group实例
    self.groupMmber: GroupMember实例
    """

    def __init__(self, group, groupMember):

        super(NewGroupMemberMsg, self).__init__()

        self.group = group
        self.groupMember = groupMember


class MeJoinedGroupMsg(BaseMsg):
    """
    我成功加入一个群
    self.group: 群实例
    self.groupAdmin: 同意我进群的管理员
    """

    def __init__(self, group, groupAdmin):

        super(MeJoinedGroupMsg, self).__init__()
        self.group = group
        self.groupAdmin = groupAdmin

class InviteMeToGroupMsg(BaseMsg):
    """
    有人邀请我入群
    要在两分钟内处理此消息，否则将被销毁
    self.groupQQ: 群号
    self.groupName: 群名
    self.groupMemberQQ: 邀请者的QQ
    self.groupMemberName: 邀请者昵称
    """

    def __init__(self, groupQQ, groupName, groupMemberQQ, groupMemberName):

        super(InviteMeToGroupMsg, self).__init__()
        self.groupQQ = groupQQ
        self.groupName = groupName
        self.groupMemberQQ = groupMemberQQ
        self.groupMemberName = groupMemberName

    def allow(self):
        """
        同意加群
        :return:
        """

    def reject(self, reason):
        """
        拒绝加群
        :reason: 拒绝的理由
        :return:
        """
