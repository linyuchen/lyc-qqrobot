# coding=UTF8

"""
运行时间
"""
import time
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, BaseMsg
from .runningtime import Time
from ..cmdaz import CMD

mod = runningtime.Time()


class MyEvent(MsgHandler):
    __doc__ = u"""
    运行时间查询
    命令：运行时间
    """

    bind_msg_types = (FriendMsg, GroupMsg)
    
    def __init__(self, qq_client):

        super(MyEvent, self).__init__(qq_client)
        self.name = "running_time"
        self.cmd = CMD("运行时间")
        self.start_time = time.time()

    def handle(self, msg: FriendMsg | GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        if self.cmd.az(msg.msg):
            result = mod(self.start_time)
            msg.reply(result)
            msg.destroy()

