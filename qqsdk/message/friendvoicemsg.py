# -*- coding: UTF8 -*-
__author__ = 'neverlike'
import basemsg
BaseMsg = basemsg.BaseMsg
class FriendVoiceMsg(BaseMsg):
    """
    self.friend: friend实例
    self.url: 语音的下载地址
    """
    def __init__(self, friend, url):
        super(FriendVoiceMsg, self).__init__()
        self.friend = friend
        self.url = url