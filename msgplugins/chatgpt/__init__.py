from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, BaseMsg
from .chatgpt import gpt_35, summary_web
from ..cmdaz import CMD


class ChatGPT(MsgHandler):
    is_async = True
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        cmd = CMD("总结", alias=["摘要"], param_len=1)
        cmd2 = CMD("总结", alias=["摘要"], param_len=1, sep="")
        if cmd.az(msg.msg) or cmd2.az(msg.msg):
            url = (cmd.paramList and cmd.paramList[0]) or (cmd2.paramList and cmd2.paramList[0])
            res = summary_web(url)
            if res:
                msg.reply(res)
                msg.destroy()
                return
        cmd = CMD("#", sep="", param_len=1)
        context_id = msg.group.qq + "g" if isinstance(msg, GroupMsg) else msg.friend.qq + "f"
        if isinstance(msg, GroupMsg):
            if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
                res = gpt_35(context_id, cmd.original_cmd or msg.msg)
                msg.reply(res)
        elif isinstance(msg, FriendMsg):
            res = gpt_35(context_id, msg.msg)
            msg.reply(res)
