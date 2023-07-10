import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sd import txt2img


class SDPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        c = CMD("画图", param_len=1, sep="")
        if c.az(msg.msg):
            image_path = txt2img(c.get_param_list()[0])
            reply_msg = MessageSegment.image_path(image_path)
            msg.reply(reply_msg)
            os.remove(image_path)
            msg.destroy()
