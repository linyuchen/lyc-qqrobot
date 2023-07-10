import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sd import txt2img


class SDPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True
    desc = "发送 画图+描述 进行AI画图\n\n发送 sd+空格+英文描述词 进行精准的AI画图"

    def handle(self, msg: GroupMsg | FriendMsg):
        c = CMD("画图", param_len=1, sep="")
        c2 = CMD("sd", param_len=1, sep=" ")
        trans = True
        draw_txt = ""
        if c.az(msg.msg):
            draw_txt = c.get_original_param()
        elif c2.az(msg.msg):
            draw_txt = c2.get_original_param()
            trans = False
        if draw_txt:
            image_path = txt2img(draw_txt, trans)
            reply_msg = MessageSegment.image_path(image_path)
            msg.reply(reply_msg)
            os.remove(image_path)
            msg.destroy()
