# coding=UTF8

"""
运行时间
"""
import time

import psutil

from msgplugins.msgcmd.cmdaz import CMD
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from .runningtime import Time

mod = runningtime.Time()


class RunStatePlugin(MsgHandler):
    __doc__ = u"""
    运行时间查询
    命令：运行时间
    """
    name = "运行状态"
    desc = "发送 运行状态 查看机器人状态"
    bind_msg_types = (FriendMsg, GroupMsg)

    def __init__(self, **kwargs):
        super(RunStatePlugin, self).__init__(**kwargs)
        self.cmd = CMD("运行时间", alias=["运行状态"])
        self.start_time = time.time()

    def handle(self, msg: FriendMsg | GroupMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        if self.cmd.az(msg.msg):
            result = mod(self.start_time)
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            result += f"\nCPU使用率：{cpu_percent}%\n内存使用率：{memory.percent}%\n"
            msg.reply(result)
            msg.destroy()
