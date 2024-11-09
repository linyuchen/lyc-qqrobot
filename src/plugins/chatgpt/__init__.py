import asyncio
import re
import threading
import time

from nonebot import on_command, on_message, on_fullmatch
from nonebot.adapters.onebot.v11 import Message, MessageEvent, GroupMessageEvent, PrivateMessageEvent, Bot, \
    MessageSegment
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="AI聊天",
    description="让bot支持AI回复",
    usage="@机器人+聊天内容，或者#聊天内容",
)


import config
from src.common.chatgpt.chatgpt import chat, summary_web, set_prompt, get_prompt, clear_prompt
from ..common.rules import is_at_me, rule_args_num

wiki_cmd = on_command("百科", force_whitespace=True, permission=SUPERUSER, rule=rule_args_num(min_num=1))


@wiki_cmd.handle()
def wiki(args: Message = CommandArg()):
    wiki_cmd.send("正在为您搜索百科...")
    params = args.extract_plain_text()

    def reply():
        res = summary_web(f"https://zh.wikipedia.org/wiki/{params[0]}")
        wiki_cmd.finish(res)

    threading.Thread(target=reply, daemon=True).start()


def gen_voice(text) -> bytes | None:
    if not config.TTS_ENABLED:
        return
    from ..tts.genshinvoice_top import tts
    # text = text.replace("喵", "")
    if len(text) <= 60:
        try:
            voice_bytes = tts(text)
            return voice_bytes
        except Exception as e:
            pass


def get_url(text: str) -> str:
    pattern = re.compile(r"(https?://[A-Za-z0-9$\-_.+!*'(),%;:@&=/?#\[\]]+)")
    url = re.findall(pattern, text)
    return url[0] if url else ""


def summary_url(url: str) -> str:
    if url := get_url(url):
        result = summary_web(url)
        return result


summary_web_cmd = on_command("总结网页", force_whitespace=True, rule=rule_args_num(min_num=1))


@summary_web_cmd.handle()
def _(event: MessageEvent, args: Message = CommandArg()):
    text = ""
    if event.reply:
        text = event.reply.message.extract_plain_text()
    text += "\n" + args.extract_plain_text()
    if url := get_url(text):
        summary_web_cmd.send("正在为您总结网页...")
        result = summary_web(url)
        summary_web_cmd.finish(result + "\n\n" + url)


def get_context_id(msg: GroupMessageEvent | PrivateMessageEvent) -> str:
    context_id = str(msg.group_id) + "g" if isinstance(msg, GroupMessageEvent) else str(msg.user_id) + "f"
    return context_id


set_prompt_cmd = on_command("设置人格", force_whitespace=True)


@set_prompt_cmd.handle()
async def _(event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    set_prompt(get_context_id(event), args.extract_plain_text())
    await set_prompt_cmd.finish("人格设置成功")


clear_prompt_cmd = on_fullmatch(("清除人格", "恢复人格", "清空人格", "重置人格"))


@clear_prompt_cmd.handle()
async def _(event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    clear_prompt(get_context_id(event))
    clear_prompt_cmd.finish("人格清除成功")


get_prompt_cmd = on_fullmatch("查看人格")


@get_prompt_cmd.handle()
async def _(msg: GroupMessageEvent | PrivateMessageEvent):
    clear_prompt(get_context_id(msg))
    await get_prompt_cmd.finish("当前人格:\n\n" + get_prompt(get_context_id(msg)))


chat_records = {}

chatgpt_cmd = on_message()


@chatgpt_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent | PrivateMessageEvent):
    if isinstance(event, GroupMessageEvent):
        sender_qq = event.group_id
        if not is_at_me(event):
            if not event.get_plaintext().strip().startswith('#'):
                return
    else:
        sender_qq = event.user_id

    if time.time() - chat_records.setdefault(sender_qq, 0) < 5:
        return
    chat_records[sender_qq] = time.time()

    _chat_text = event.get_plaintext()
    if event.reply:
        _chat_text = event.reply.message.extract_plain_text() + '\n' + _chat_text

    async def gptchat():
        _res = chat(get_context_id(event), _chat_text)
        await bot.send(event, MessageSegment.reply(event.message_id) + _res)
        # voice_bytes = gen_voice(_res)
        # if voice_bytes:
        #     await bot.send(event, MessageSegment.record(voice_bytes))
    threading.Thread(target=lambda: asyncio.run(gptchat()), daemon=True).start()
