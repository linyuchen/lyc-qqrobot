from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .cmdaz import CMD


class ExamplePlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("b").az(msg.msg):
            reply_msg = MessageSegment.image_path("")
            msg.reply(reply_msg)
