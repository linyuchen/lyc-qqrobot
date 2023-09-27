# coding=UTF8
from dataclasses import dataclass

from qqsdk.entity.friend import Friend
from qqsdk.entity.group import Group
from qqsdk.message.basemsg import BaseMsg
from qqsdk.message.types import MessageTypes


@dataclass
class FriendMsg(BaseMsg):
    """
    """
    friend: Friend = None
    msg_type = MessageTypes.FRIEND
    quote_msg: 'FriendMsg' = None  # 引用的消息

    @property
    def is_from_super_admin(self):
        return self.friend.is_super_admin


@dataclass
class FriendSignatureChangedMsg(FriendMsg):
    """
    好友签名修改消息
    """
    msg_type = MessageTypes.FRIEND_SIGNATURE


@dataclass
class FriendStatusChangeMsg(FriendMsg):
    """
    好友状态改变消息
    """
    msg_type = MessageTypes.FRIEND_STATUS


@dataclass
class FriendVoiceMsg(FriendMsg):
    msg_type = MessageTypes.FRIEND_VOICE
    url: str = ""  # 语音的url


@dataclass
class TempMsg(BaseMsg):
    """
    临时会话消息
    self.qq : int,发送者的QQ
    self.group: Group实例，如果是群里发起的则有，否则为None
    """
    msg_type = MessageTypes.TEMP

    qq: str = ""
    group: Group = None

    def __init__(self):
        super(TempMsg, self).__init__()


@dataclass
class AddedMeFriendMsg(FriendMsg):
    """
    对方已经添加了我为好友
    self.friend: Friend实例
    """
    msg_type = MessageTypes.ADDED_ME_FRIEND


@dataclass
class SendBuddyMsg(FriendMsg):
    """
    好像暂时用不到
    发送消息给好友
    """


@dataclass
class RequestAddMeFriend(BaseMsg):
    """
    对方请求添加我为好友
    """
    msg_type = MessageTypes.REQUEST_ADD_ME_FRIEND
    request_qq: str = ""

    def allow(self):
        """
        同意
        :return:
        """

    def reject(self, reason: str):
        """
        拒绝
        :param reason: 拒绝理由
        :return:
        """


@dataclass
class AddFriendResultMsg(BaseMsg):
    """
    加别人好友得到的结果
    self.qq: int, 对方QQ
    self.name: string, 对方昵称
    self.msg: string, 消息结果
    """
    msg_type = MessageTypes.ADD_ME_FRIEND_RESULT

    qq: str = ""
    name: str = ""
