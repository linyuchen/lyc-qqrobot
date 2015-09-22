#coding=UTF8
import basemsg
class TempMsg(basemsg.BaseMsg):
    """
    self.uin : int,发送者的uin
    self.qq : int,发送者的QQ
    self.ip : int, 发送者ip
    self.group: Group实例，如果是群里发起的则有，否则为None
    """

    def __init__(self):

        super(TempMsg, self).__init__()

        self.uin = 0
        self.qq = 0
        self.group = None
        self.fontStyle = None
        self.ip = 0
