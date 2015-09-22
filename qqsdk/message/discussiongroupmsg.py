# -*- coding:UTF8 -*-
__author__ = 'neverlike'
import basemsg


class DiscussionGroupMsg(basemsg.BaseMsg):
    """
    self.senderQQ : int,发送者的QQ
    self.senderName: string, 发送者名字
    self.groupId: int, 讨论组ID
    """

    def __init__(self, senderQQ, senderName, groupId):

        super(DiscussionGroupMsg, self).__init__()
        self.senderQQ = senderQQ
        self.senderName = senderName
        self.groupId = groupId