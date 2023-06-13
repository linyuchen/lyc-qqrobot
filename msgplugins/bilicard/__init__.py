import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .bilicard import get_bv_id, gen_text


class BiliCardPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        bvid = get_bv_id(msg.msg)
        if bvid:
            text = gen_text(bvid)
            if text:
                msg.reply(text)

            # if img_path:
            #     reply_msg = MessageSegment.image_path(img_path)
            #     msg.reply(reply_msg)
            #     os.remove(img_path)
