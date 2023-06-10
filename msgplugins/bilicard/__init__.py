import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .bilicard import handle, get_bvid


class BiliCardPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        bvid = get_bvid(msg.msg)
        if bvid:
            img_path = handle(bvid)
            if img_path:
                reply_msg = MessageSegment.image_path(img_path)
                msg.reply(reply_msg)
                os.remove(img_path)
