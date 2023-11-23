from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from msgplugins.msgcmd.cmdaz import CMD
from .news import get_news2


class DailyNewsPlugin(MsgHandler):
    name = "每日新闻"
    desc = "今日新闻"
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("每日新闻", param_len=0, alias=["今日新闻", "今天新闻", "早报", "晚报", "每天新闻"]).az(msg.msg):
            msg.destroy()
            img_path = get_news2()
            if img_path:
                msg.reply(MessageSegment.image_path(img_path))
