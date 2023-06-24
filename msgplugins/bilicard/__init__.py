import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .bilicard import get_bv_id, gen_text, gen_image


class BiliCardPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        bvid = get_bv_id(msg.msg)
        if bvid:
            # text = gen_text(bvid)
            # if text:
            #     msg.reply(text)
            img_path, desc, summary = gen_image(bvid)
            if img_path:
                reply_msg = MessageSegment.image_path(img_path) + \
                            MessageSegment.text("简介：" + desc + "\n\n" + summary +
                                                "\n\n" + f"https://www.bilibili.com/video/BV{bvid}")
                msg.reply(reply_msg)
                os.remove(img_path)
                msg.destroy()
