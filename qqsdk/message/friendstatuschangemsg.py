#coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg

class FriendStatusChangeMsg(BaseMsg):
    """
    好友状态改变消息
    self.friend: Friend实例
    """
    EVENT_NAME = "FriendStatusChanged"

    def __init__(self, friend):

        super(FriendStatusChangeMsg, self).__init__()

        self.friend = friend
