import re
import threading
import time

import config
from common.logger import logger
from msgplugins.msgcmd.cmdaz import CMD, on_command
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg, GeneralMsg
from qqsdk.message.segment import MessageSegment
from .chatgpt import chat, summary_web, set_prompt, get_prompt, clear_prompt


@on_command("百科", param_len=1, desc="百科搜索",
            example="如:百科 猫娘", is_async=True)
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
            voice_path = tts(text)
            msg.reply(MessageSegment.voice_path(voice_path))
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


@on_command("总结网页",
            alias=("总结一下",),
            param_len=-1,
            desc="AI总结网页", example="总结网页 https://www.qq.com", is_async=True)
def summary_web_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    text = msg.quote_msg.msg if msg.quote_msg else ""
    text += "\n" + msg.msg
    if url := get_url(text):
        msg.reply("正在为您总结网页...")
        result = summary_web(url)
        msg.reply(result + "\n\n" + url)
        return


def get_context_id(msg: GeneralMsg) -> str:
    context_id = msg.group.qq + "g" if isinstance(msg, GroupMsg) else msg.friend.qq + "f"
    return context_id


@on_command("设置人格", param_len=1,
            cmd_group_name="ChatGPT",
            desc="设置AI人格",
            example="设置人格 你现在是一只狗娘")
def set_prompt_cmd(msg: GeneralMsg, params: list[str]):
    set_prompt(get_context_id(msg), params[0])
    msg.reply("人格设置成功")


@on_command("清除人格", alias=("恢复人格", "清空人格", "重置人格"),
            cmd_group_name="ChatGPT",
            desc="清除AI人格")
def clear_prompt_cmd(msg: GeneralMsg, params: list[str]):
    clear_prompt(get_context_id(msg))
    msg.reply("人格清除成功")


@on_command("查看人格",
            cmd_group_name="ChatGPT",
            desc="查看AI人格")
def clear_prompt_cmd(msg: GeneralMsg, params: list[str]):
    clear_prompt(get_context_id(msg))
    msg.reply("当前人格:\n\n" + get_prompt(get_context_id(msg)))


chat_records = {}


@on_command("",
            cmd_group_name="ChatGPT",
            desc="@机器人进行AI对话",
            example="@喵了个咪 你好",
            is_async=True, priority=-1)
def chat_cmd(msg: GeneralMsg, params: list[str]):
    if isinstance(msg, GroupMsg):
        sender_qq = msg.group_member.qq
        if not msg.is_at_me:
            return
        if msg.group_member.nick in ["Q群管家"]:
            return
    else:
        sender_qq = msg.friend.qq

    if time.time() - chat_records.setdefault(sender_qq, 0) < 5:
        return
    chat_records[sender_qq] = time.time()

    _chat_text = msg.msg
    if msg.quote_msg:
        _chat_text = msg.quote_msg.msg + '\n' + _chat_text
    _res = chat(get_context_id(msg), _chat_text)
    msg.reply(_res)
    send_voice(msg, _res)
