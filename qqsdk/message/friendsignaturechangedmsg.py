# -*- coding:UTF8 -*-
__author__ = 'neverlike'

import basemsg


class FriendSignatureChangedMsg(basemsg.BaseMsg):
    """
    self.friend: Friend实例
    """
    def __init__(self, friend):

        super(FriendSignatureChangedMsg, self).__init__()

        self.friend = friend
