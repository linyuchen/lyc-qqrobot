#coding=UTF8
import basemsg
class SendBuddyMsg(basemsg.BaseMsg):
    """
    发送给好友或者陌生人的消息
    self.qq : int,对方QQ
    self.time : int, 发送时间戳
    self.fontStyle : FontStyle实例发送的字体
    self.content : str,发送的内容

    """

    def __init__(self):

        super(SendBuddyMsg, self).__init__()

        self.qq = 0
        self.fontStyle = None
        self.time = 0
        self.content = ""
