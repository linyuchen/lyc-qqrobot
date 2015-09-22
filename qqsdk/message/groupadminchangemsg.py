# coding=UTF8
import basemsg

BaseMsg = basemsg.BaseMsg


class GroupAdminChangeMsg(BaseMsg):
    """
    self.group : Group实例
    self.groupMember : GroupMember实例
    """
    EVENT_NAME = "GroupAdminChanged"

    def __init__(self,group, groupMember):
        super(GroupAdminChangeMsg, self).__init__()
        self.group = group
        self.groupMember = groupMember
