import random
import tempfile
import time
from pathlib import Path

import httpx

from nonebot import on_message, Bot
from nonebot.internal.adapter import Event
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg, Reply
from nonebot_plugin_uninfo import get_session

__plugin_meta__ = PluginMetadata(
    name="动图加速",
    description="有一定概率对用户GIF动图进行加速",
    usage="可以对GIF引用回复 加速 来手动加速"
)

from src.common.utils.gif_speed import re_speed, is_gif
from src.plugins.common.message import get_message_image_urls

history: dict[str, float] = {}


@on_message().handle()
async def random_speed_up_gif(bot: Bot, event: Event, msg: UniMsg):
    session = await get_session(bot, event)
    msg_text = event.message.extract_plain_text().strip()
    reply_msg = msg.get(Reply)
    if reply_msg:
        reply_msg: Reply = reply_msg[0]
        reply_msg = await UniMsg.generate(message=reply_msg.msg)
        reply_img_urls = get_message_image_urls(reply_msg)
    else:
        reply_img_urls = []
    img_urls = get_message_image_urls(msg)
    img_urls = reply_img_urls + img_urls
    r_int = random.randint(0, 10)
    is_manual = msg_text == '加速'
    if r_int != 0 and not is_manual:
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
        qq = session.group.id if session.scene.is_group else session.user.id
        last_time = history.get(qq, 0)
        if (time.time() - last_time) < 5 * 60 and not is_manual:
            return
        history[qq] = time.time()
        re_path = re_speed(img_path, random.choice([30, 40, 50]))
        await bot.send(event, await UniMsg.image(raw=re_path.read_bytes()).export())
        img_path.unlink()
        re_path.unlink()
