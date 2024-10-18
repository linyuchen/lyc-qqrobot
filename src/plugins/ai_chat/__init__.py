import time

import httpx
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, PrivateMessageEvent, MessageSegment

from config import get_config
from src.plugins.common.rules import is_at_me

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
        return

    if time.time() - chat_records.setdefault(sender_qq, 0) < 5:
        return
    chat_records[sender_qq] = time.time()

    _chat_text = event.get_plaintext()
    if event.reply:
        _chat_text = event.reply.message.extract_plain_text() + '\n' + _chat_text

    ai_server_host = get_config('AI_CHAT_SERVER')
    async with httpx.AsyncClient() as client:
        r = await client.post(f'{ai_server_host}/chat', json={
            "user_id": str(sender_qq),
            "question": _chat_text
        }, timeout=60)
        res = r.json()
        ai_res = res['result']
        await bot.send(event, MessageSegment.reply(event.message_id) + ai_res)
