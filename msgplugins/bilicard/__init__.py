import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .bilicard import get_bv_id, gen_text, gen_image, get_av_id, transform_b23, check_is_b23


class BiliCardPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        msg_text = msg.msg
        b32_url = check_is_b23(msg_text)
        if b32_url:
            msg.destroy()
            msg_text = transform_b23(b32_url[0])

        bvid = get_bv_id(msg_text)
        avid = get_av_id(msg_text)
        if bvid or avid:
            # text = gen_text(bvid)
            # if text:
            #     msg.reply(text)
            msg.destroy()
            img_path, desc, summary = gen_image(bvid, avid)
            url = f"https://www.bilibili.com/video/BV{bvid}" if bvid else f"https://www.bilibili.com/video/av{avid}"
            if img_path:
                reply_msg = MessageSegment.image_path(img_path) + \
                            MessageSegment.text("简介：" + desc + "\n\n" + summary +
                                                "\n\n" + url)
                msg.reply(reply_msg)
                os.remove(img_path)
