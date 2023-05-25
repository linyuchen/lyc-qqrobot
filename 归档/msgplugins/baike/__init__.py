# coding=UTF8

from qqsdk.message.msghandler import MsgHandler
from qqsdk.message import GroupMsg, FriendMsg, BaseMsg
from msgplugins.baike.baidubaike import Baike
from msgplugins.cmdaz import CMD

baike = Baike()


class BaikeMsgHandler(MsgHandler):
    __doc__ = """
    百度百科查询
    命令：百科 + 空格 + 关键字
    """
    bind_msg_types = (FriendMsg, GroupMsg)

    def __init__(self, qq_client):
        super(BaikeMsgHandler, self).__init__(qq_client)
        self.name = "baike"
        self.cmd = CMD("百科", param_len=1, handle_func=baike)

    def handle(self, msg: BaseMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = self.cmd.handle(msg.msg)
        if result:
            msg.reply(result)
            msg.destroy()

