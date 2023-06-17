from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from ..cmdaz import CMD
from .news import get_news


class ExamplePlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("每日新闻", param_len=0).az(msg.msg):
            msg.reply(get_news())
