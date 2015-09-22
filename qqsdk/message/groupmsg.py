#coding=UTF8

import basemsg

class GroupMsg(basemsg.BaseMsg):
    """
    self.group: entity.group.Group实例,发送者所在的群
    self.groupMember : entity.groupmember.GroupMember实例,发送者
    self.msg: string, 消息内容
    """
    EVENT_NAME = "GroupMsg"

    def __init__(self, group, groupMember, msg):

        super(GroupMsg, self).__init__()

        self.group = group
        self.groupMember = groupMember
        self.msg = msg

