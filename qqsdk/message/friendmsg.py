#coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg

class FriendMsg(BaseMsg):
    """
    self.friend : Friend实例
    """
    EVENT_NAME = "FriendMsg"

    def __init__(self, friend):

        super(FriendMsg, self).__init__()
        self.friend = friend
        self.fontStyle = None



