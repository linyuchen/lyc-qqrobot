# -*- encoding:UTF8 -*-
from dataclasses import dataclass

from qqsdk.entity.group import Group, GroupMember
from qqsdk.message.segment import MessageSegment
from qqsdk.message.basemsg import BaseMsg
from qqsdk.message.types import MessageTypes


@dataclass
class GroupMsg(BaseMsg):
    """
    """
    msg_id: int | str = None
    msg_type = MessageTypes.GROUP
    group: Group = None
    group_member: GroupMember = None
    is_at_me: bool = False
    is_at_other: bool = False
    quote_msg: 'GroupMsg' = None

    def recall(self):
        """
        撤回消息
        """

    @property
    def is_from_admin(self):
        """
        是否是管理员发的消息
        """
        return self.group_member.is_admin or self.group_member.is_creator or self.group_member.is_super_admin

    @property
    def is_from_super_admin(self):
        """
        是否是超级管理员发的消息
        """
        return self.group_member.is_super_admin


@dataclass
class GroupNudgeMsg(BaseMsg):
    """
    群戳一戳
    """
    action: str = ""
    group: Group = None
    from_member: GroupMember = None
    target_member: GroupMember = None
    msg_type = MessageTypes.GROUP_NUDGE


@dataclass
class GroupAdminChangeMsg(GroupMsg):
    """
    self.group : Group实例
    self.groupMember : GroupMember实例
    """

    msg_type = MessageTypes.GROUP_ADMIN_CHANGE


@dataclass
class GroupMemberCardChangedMsg(BaseMsg):
    """
    """
    old_name: str = ""  # 群成员之前的群名片
    msg_type = MessageTypes.GROUP_MEMBER_CARD_CHANGE


@dataclass
class RequestJoinGroupMsg(BaseMsg):
    """
    有人申请加群，只有管理员才能收到此消息
    msg: 验证消息
    """
    msg_type = MessageTypes.GROUP_REQUEST_JOIN
    group: Group = None
    request_qq: str = ""
    request_name: str = ""

    def allow(self):
        """
        同意入群
        """

    def reject(self, reason: str):
        """
        拒绝入群
        reason: string, 拒绝理由
        """


@dataclass
class NewGroupMemberMsg(GroupMsg):
    """
    新成员入群
    """
    msg_type = MessageTypes.GROUP_NEW_MEMBER


@dataclass
class MeJoinedGroupMsg(GroupMsg):
    """
    我成功加入一个群
    group_member: 同意我进群的管理员
    """
    msg_type = MessageTypes.GROUP_JOINED


@dataclass
class GroupInviteMsg(BaseMsg):
    """
    """

    # 邀请者相关信息
    group_qq: str = ""
    group_name: str = ""
    group_member_qq: str = ""
    group_member_name: str = ""

    def allow(self):
        """
        同意加群
        :return:
        """

    def reject(self, reason: str):
        """
        拒绝加群
        :reason: 拒绝的理由
        :return:
        """


@dataclass
class GroupRemoveMeMsg(BaseMsg):
    """
    我被踢出群的消息
    self.groupQQ： 群号
    self.adminUin：踢我的管理员uin
    self.adminName：踢我的管理员昵称
    """
    group_qq: str = ""
    admin_qq: str = ""
    admin_name: str = ""


@dataclass
class GroupRemoveMemberMsg(GroupMsg):
    """
    group_member: 踢人的管理员
    """

    member_name: str = ""
    member_qq: str = ""


@dataclass
class GroupMemberExitMsg(BaseMsg):
    """
    """
    group: Group = None
    member_name: str = ""
    member_qq: str = ""


@dataclass
class DiscussionGroupMsg(BaseMsg):
    """
    讨论组消息
    """
    qq: str = ""  # 发送者qq
    name: str = ""  # 发送者名字
    discussion_id: str = ""


@dataclass
class GroupSendMsg(GroupMsg):
    """
    发送给群的消息
    """
    msg_type = MessageTypes.GROUP_SEND
