# coding=UTF8

import os
from qqsdk.message.msghandler import MsgHandler
from qqsdk.message import GroupMsg, FriendMsg, BaseMsg
from msgplugins.cmdaz import CMD
from nonebot.message import MessageSegment
from ..superplugins import GroupPointAction
from .card import gacha


class GenShinCardMsgHandler(MsgHandler):
    __doc__ = """
    模拟原神常驻池十连抽
    """
    bind_msg_types = (FriendMsg, GroupMsg)

    def __init__(self, qq_client):
        super(GenShinCardMsgHandler, self).__init__(qq_client)
        self.cmd = CMD("原神十连")
        self.once_point = 2000  # 调用一次所需活跃度
        self.group_point_action = GroupPointAction()

    def handle(self, msg: BaseMsg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        msg: GroupMsg
        if self.cmd.az(msg.msg):
            if self.group_point_action.get_point(msg.group.qq, msg.group_member.qq) < self.once_point:
                return msg.reply(f"【{msg.group_member.get_name()}】的活跃度不足{self.once_point}")

            img_file_name = gacha()
            reply_msg = MessageSegment.image("file://" + img_file_name)
            r_msg = MessageSegment.text(f"【{msg.group_member.get_name()}】的抽奖结果：") + reply_msg
            msg.reply(r_msg)
            msg.destroy()
            self.group_point_action.add_point(msg.group.qq, msg.group_member.qq, -self.once_point)
