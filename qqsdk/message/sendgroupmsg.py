#coding=UTF8
import basemsg
class SendGroupMsg(basemsg.BaseMsg):
    """
    发送给群的消息
    self.group : Group实例
    self.time : int, 发送时间戳
    self.fontStyle : 发送的字体
    self.content : str,发送的内容

    """

    def __init__(self):

        super(SendGroupMsg, self).__init__()

        self.group = None
        self.fontStyle = None
        self.time = 0
        self.content = ""
