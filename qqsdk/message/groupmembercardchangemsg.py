#coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg


class GroupMemberCardChangedMsg(BaseMsg):
    """
    self.group : Group实例
    self.groupMember : GroupMember实例
    self.oldName: 更改群名片之前的昵称
    """
    def __init__(self, group, groupMember, oldName):

        super(GroupMemberCardChangedMsg, self).__init__()
        self.group = group
        self.groupMember = groupMember
        self.oldName = oldName

