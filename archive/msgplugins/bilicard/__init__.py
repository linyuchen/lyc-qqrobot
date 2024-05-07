import os
import time

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from . import bilicard


class BiliCardPlugin(MsgHandler):
    name = "B站"
    desc = "自动解析B站视频链接\n获取视频简介和封面图及AI总结视频内容"
    example = "https://b23.tv/av12345678"
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True
    cached = {}

    def check_in_cache(self, bvid):
        if bvid in self.cached and time.time() - self.cached[bvid] < 60:
            return True
        self.cached[bvid] = time.time()
        return False

    def handle(self, msg: GroupMsg | FriendMsg):
        msg_text = msg.msg
        # 是否是QQ卡片分享，由于卡片附带了预览效果，如果没有简介或者字幕总结，没必要用机器人再发送一次
        is_from_card = "__from__card" in msg_text
        b32_url = bilicard.check_is_b23(msg_text)
        if b32_url:
            msg.pause()  # 因为b32链接有可能是不是视频链接，比如是专栏，用于被其他插件使用，所以这里先暂停
            msg_text = bilicard.b32_to_bv(b32_url[0])

        bvid = bilicard.get_bv_id(msg_text)
        avid = bilicard.get_av_id(msg_text)

        if bvid or avid:
            if bvid and len(bvid) < 6:
                return
            if avid and len(avid) < 6:
                return
            msg.destroy()
            msg.destroy()
            msg.resume()
            # text = gen_text(bvid)
            # if text:
            #     msg.reply(text)
            msg.destroy()
            if bvid and self.check_in_cache(bvid):
                return
            video_info = bilicard.get_video_info(bvid, avid)

            bvid = video_info.get("bvid", "")
            if self.check_in_cache(bvid + msg.group.qq if isinstance(msg, GroupMsg) else msg.friend.qq):
                return
            img_path = bilicard.gen_image(video_info)
            summary = bilicard.get_video_summary_by_ai(video_info["aid"], video_info["cid"])
            # 没有简介内容或者简介等于标题的，且是卡片分享的，而且AI无法总结的就不需要发送了
            if ((len(video_info["desc"]) < 4 or video_info["desc"] == video_info["title"])
                    and is_from_card and not summary):
                return
            summary = "AI总结：" + (summary if summary else "此视频不支持")
            url = f"https://bilibili.com/video/{bvid}" if bvid else f"https://bilibili.com/video/av{avid}"
            if img_path:
                reply_msg = MessageSegment.image_path(img_path) + \
                            MessageSegment.text("简介：" + video_info["desc"] + "\n\n" + summary +
                                                "\n\n" + url)
                if isinstance(msg, GroupMsg):
                    msg.reply(reply_msg, at=False, quote=False)
                else:
                    msg.reply(reply_msg)
                os.remove(img_path)

        else:
            # 不是视频链接，所以这里要去掉暂停状态，让其他插件可以使用
            msg.resume()
