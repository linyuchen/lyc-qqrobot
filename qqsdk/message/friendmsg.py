# coding=UTF8
from qqsdk.message.basemsg import BaseMsg
from qqsdk.entity.friend import Friend


class FriendMsg(BaseMsg):
    """
    self.friend : Friend实例
    """
    EVENT_NAME:str = "FriendMsg"

    def __init__(self, friend: Friend):

        super(FriendMsg, self).__init__()
        self.friend = friend
        self.fontStyle = None  # 已经弃用

class FriendSignatureChangedMsg(FriendMsg):
    """
    好友签名修改消息
    """
    EVENT_NAME = "FriendSignatureChanged"


class FriendStatusChangeMsg(FriendMsg):
    """
    好友状态改变消息
    """
    EVENT_NAME = "FriendStatusChanged"


class FriendVoiceMsg(FriendMsg):

    EVENT_NAME = "FriendVoiceMsg"

    def __init__(self, friend: Friend, url: str):
        """
        url: 语音的下载地址
        """
        super(FriendVoiceMsg, self).__init__(friend)
        self.url = url
