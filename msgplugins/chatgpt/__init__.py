from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, BaseMsg
from .chatgpt import gpt_35
from ..cmdaz import CMD


class ChatGPT(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: BaseMsg):
        cmd = CMD("#", sep="", param_len=1)
        if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
            res = gpt_35(cmd.get_original_param() or msg.msg)
            msg.reply(res)
