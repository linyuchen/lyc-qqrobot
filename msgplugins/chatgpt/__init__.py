import re
import time

import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .chatgpt import chat, summary_web, set_prompt, get_prompt, clear_prompt
from ..cmdaz import CMD, on_command


@on_command("百科", param_len=1, desc="发送 百科 + 词语 进行百科搜索,如:百科 猫娘")
def wiki(msg: GroupMsg | FriendMsg, params: list[str]):
    res = summary_web(f"https://zh.wikipedia.org/wiki/{params[0]}")
    msg.reply(res)


@on_command("萌娘百科", param_len=1, desc="发送 萌娘百科 + 词语 进行萌娘百科搜索,如:萌娘百科 猫娘")
def moe_wiki(msg: GroupMsg | FriendMsg, params: list[str]):
    res = summary_web(f"https://zh.moegirl.org.cn/{params[0]}")
    msg.reply(res)


def send_voice(msg: GroupMsg | FriendMsg, text):
    from ..tts.vits import tts
    text = text.replace("喵", "")
    if len(text) <= 80:
        try:
            base64_data = tts(text)
            msg.reply(MessageSegment.voice_base64(base64_data))
        except Exception as e:
            pass


class ChatGPT(MsgHandler):
    desc = "发送 #+消息 或者 @机器人+消息 进行AI对话\n\n" \
           "@机器人发送 网址(如:http://qq.com) 进行AI总结网页\n\n" \
           "发送 设置人格 + 空格 + 人格提示语 进行AI人格设置\n" \
           "发送 清除人格 进行AI人格清除\n" \
           "发送 查看人格 进行AI人格查看\n"
    is_async = True
    bind_msg_types = (GroupMsg, FriendMsg)
    records = {}

    def handle(self, msg: GroupMsg | FriendMsg):
        context_id = msg.group.qq + "g" if isinstance(msg, GroupMsg) else msg.friend.qq + "f"
        set_prompt_cmd = CMD("设置人格", param_len=1)
        clear_prompt_cmd = CMD("清除人格", alias=["恢复人格", "清空人格", "重置人格"])
        get_prompt_cmd = CMD("查看人格")
        if set_prompt_cmd.az(msg.msg):
            set_prompt(context_id, set_prompt_cmd.get_param_list()[0])
            msg.reply("人格设置成功")
            msg.destroy()
            return
        elif clear_prompt_cmd.az(msg.msg):
            clear_prompt(context_id)
            msg.destroy()
            msg.reply("人格已清除")
            return
        elif get_prompt_cmd.az(msg.msg):
            msg.reply("当前人格:\n\n" + get_prompt(context_id))
            msg.destroy()
            return

        pattern = re.compile("^https?://[A-Za-z0-9$\-_.+!*'(),%;:@&=/?#\[\]]+$")
        if re.match(pattern, msg.msg.strip()):
            if isinstance(msg, GroupMsg) and not msg.is_at_me:
                return
            url = msg.msg.strip()
            if res := summary_web(url):
                msg.reply(res + "\n\n" + url)
                msg.destroy()
                return
        if isinstance(msg, GroupMsg):
            robot_name = msg.group.get_member(str(config.QQ)).get_name()
            cmd = CMD("#", alias=[f"@{robot_name}"], sep="", param_len=1,
                      ignores=["#include", "#define", "#pragma", "#ifdef", "#ifndef"])
            if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
                if time.time() - self.records.setdefault(msg.group_member.qq, 0) < 5:
                    return
                self.records[msg.group_member.qq] = time.time()
                use_gpt_4 = msg.group_member.qq == str(config.ADMIN_QQ) and msg.msg.startswith("#")
                res = chat(context_id, cmd.original_cmd or msg.msg)
                send_voice(msg, res)
                msg.reply(res)
        elif isinstance(msg, FriendMsg):
            res = chat(context_id, msg.msg)
            send_voice(msg, res)
            msg.reply(res)
