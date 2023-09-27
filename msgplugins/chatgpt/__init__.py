import re
import threading
import time
from pathlib import Path

import config
from common.logger import logger
from msgplugins.msgcmd.cmdaz import CMD, on_command
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .chatgpt import chat, summary_web, set_prompt, get_prompt, clear_prompt


@on_command("百科", param_len=1, desc="百科搜索,如:百科 猫娘")
def wiki(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("正在为您搜索百科...")

    def reply():
        res = summary_web(f"https://zh.wikipedia.org/wiki/{params[0]}")
        msg.reply(res)

    threading.Thread(target=reply, daemon=True).start()


def send_voice(msg: GroupMsg | FriendMsg, text):
    if not config.TTS_ENABLED:
        return
    from ..tts.genshinvoice_top import tts
    # text = text.replace("喵", "")
    if len(text) <= 60:
        try:
            base64_data = tts(text)
            msg.reply(MessageSegment.voice_base64(base64_data))
        except Exception as e:
            logger.error(e)


def get_url(text: str) -> str:
    pattern = re.compile(r"(https?://[A-Za-z0-9$\-_.+!*'(),%;:@&=/?#\[\]]+)")
    url = re.findall(pattern, text)
    return url[0] if url else ""


def summary_url(url: str) -> str:
    if url := get_url(url):
        result = summary_web(url)
        return result


@on_command("总结",
            alias=("总结一下", "总结网页"),
            param_len=-1, desc="总结网页,如:总结 https://www.qq.com")
def summary_web_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    text = msg.quote_msg.msg if msg.quote_msg else ""
    text += "\n" + msg.msg
    if url := get_url(text):
        msg.reply("正在为您总结网页...")
        result = summary_web(url)
        msg.reply(result + "\n\n" + url)
        return


class ChatGPT(MsgHandler):
    name = "ChatGPT"
    desc = "#+消息 或者 @机器人+消息 进行AI对话\n\n" \
           "@机器人发送 http开头的网址进行AI总结网页\n\n" \
           "设置人格，如：设置人格 你现在是一只狗娘\n" \
           "清除人格\n" \
           "查看人格\n"
    is_async = True
    priority = -1
    bind_msg_types = (GroupMsg, FriendMsg)
    records = {}
    ignore_username = ["Q群管家"]

    def handle(self, msg: GroupMsg | FriendMsg):
        if isinstance(msg, GroupMsg) and msg.group_member.get_name() in self.ignore_username:
            return
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

        if url := get_url(msg.msg):
            if isinstance(msg, GroupMsg) and not msg.is_at_me:
                return
            if res := summary_web(url):
                msg.reply(res + "\n\n" + url)
                msg.destroy()
                return
        if isinstance(msg, GroupMsg):
            cmd = CMD("#",
                      alias=["＃"],
                      sep="", param_len=1,
                      ignores=["#include", "#define", "#pragma", "#ifdef", "#ifndef", "#ph"])
            if cmd.az(msg.msg) or getattr(msg, "is_at_me", False):
                if time.time() - self.records.setdefault(msg.group_member.qq, 0) < 5:
                    return
                self.records[msg.group_member.qq] = time.time()

                # use_gpt_4 = msg.group_member.qq == str(config.ADMIN_QQ) and msg.msg.startswith("#")
                def reply():
                    _chat_text = cmd.input_text or msg.msg
                    if msg.quote_msg:
                        _chat_text = msg.quote_msg.msg + '\n' + _chat_text
                    _res = chat(context_id, _chat_text)
                    msg.reply(_res)
                    send_voice(msg, _res)

                threading.Thread(target=reply, daemon=True).start()
        elif isinstance(msg, FriendMsg):
            if time.time() - self.records.setdefault(msg.friend.qq, 0) < 5:
                return
            self.records[msg.friend.qq] = time.time()
            chat_text = msg.msg
            if msg.quote_msg:
                chat_text = msg.quote_msg.msg + '\n' + chat_text
            res = chat(context_id, chat_text)
            send_voice(msg, res)
            msg.reply(res)
