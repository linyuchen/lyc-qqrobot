import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, BaseMsg
from .chatgpt import chat, summary_web
from ..cmdaz import CMD


class ChatGPT(MsgHandler):
    desc = "发送 #+消息 或者 @机器人+消息 进行AI对话\n\n发送 总结+网址 进行AI总结网页"
    is_async = True
    bind_msg_types = (GroupMsg, FriendMsg)

    def handle(self, msg: GroupMsg | FriendMsg):
        cmd = CMD("总结", alias=["摘要"], param_len=1)
        cmd2 = CMD("总结", alias=["摘要"], param_len=1, sep="")
        if cmd.az(msg.msg) or cmd2.az(msg.msg):
            url = (cmd.paramList and cmd.paramList[0]) or (cmd2.paramList and cmd2.paramList[0])
            res = summary_web(url)
            if res:
                msg.reply(res + "\n\n" + url)
                msg.destroy()
                return
        cmd = CMD("#", sep="", param_len=1)
        context_id = msg.group.qq + "g" if isinstance(msg, GroupMsg) else msg.friend.qq + "f"
        if isinstance(msg, GroupMsg):
            if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
                # use_gpt_4 = msg.group_member.qq == config.ADMIN_QQ
                use_gpt_4 = False
                res = chat(context_id, cmd.original_cmd or msg.msg, use_gpt4=use_gpt_4)
                msg.reply(res)
        elif isinstance(msg, FriendMsg):
            res = chat(context_id, msg.msg)
            msg.reply(res)
