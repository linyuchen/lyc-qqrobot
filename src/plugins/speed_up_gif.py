import random
import tempfile
import time
from pathlib import Path

import httpx

from nonebot import on_message, Bot
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

from src.common.utils.gif_speed import re_speed, is_gif
from src.plugins.common import get_message_image_urls

history: dict[str, float] = {}


@on_message().handle()
async def random_speed_up_gif(bot: Bot, event: MessageEvent):
    msg_text = event.message.extract_plain_text().strip()
    reply_img_urls = get_message_image_urls(event.reply.message) if event.reply else []
    img_urls = get_message_image_urls(event.message)
    img_urls = reply_img_urls + img_urls
    r_int = random.randint(0, 10)
    if r_int != 0 and msg_text != '加速':
        return
    if img_urls:
        img_url = img_urls[0]
        img_path = Path(tempfile.mktemp(suffix=".gif"))
        async with httpx.AsyncClient() as http:
            img_data = (await http.get(img_url)).content
            with open(img_path, "wb") as f:
                f.write(img_data)
            if not is_gif(img_path):
                return
        qq = event.group_id if hasattr(event, 'group_id') else event.user_id
        last_time = history.get(qq, 0)
        if (time.time() - last_time) < 5 * 60:
            return
        history[qq] = time.time()
        re_path = re_speed(img_path, random.choice([30, 40, 50]))
        await bot.send(event, MessageSegment.image(re_path))
        img_path.unlink()
        re_path.unlink()
