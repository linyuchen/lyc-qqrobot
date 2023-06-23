from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, BaseMsg
from .chatgpt import gpt_35
from ..cmdaz import CMD


class ChatGPT(MsgHandler):
    is_async = True
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        cmd = CMD("#", sep="", param_len=1)
        context_id = msg.group.qq + "g" if isinstance(msg, GroupMsg) else msg.friend.qq + "f"
        if isinstance(msg, GroupMsg):
            if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
                res = gpt_35(context_id, cmd.get_original_param() or msg.msg)
                msg.reply(res)
        elif isinstance(msg, FriendMsg):
            res = gpt_35(context_id, msg.msg)
            msg.reply(res)
