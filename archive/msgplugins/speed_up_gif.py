import random
import tempfile
import time
from pathlib import Path

import requests

from common.utils.gif_speed import re_speed, is_gif
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment

history: dict[str, float] = {}


@on_command("", cmd_group_name="随机加速gif")
def random_speed_up_gif(msg: GeneralMsg, params: list[str]):
    r_int = random.randint(0, 10)
    if r_int != 0:
        return
    img_urls = msg.msg_chain.get_image_urls()
    if img_urls:
        img_url = img_urls[0]
        img_path = Path(tempfile.mktemp(suffix=".gif"))
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as f:
            f.write(img_data)
        if not is_gif(img_path):
            return
        qq = msg.group.qq if msg.group else msg.friend.qq
        last_time = history.get(qq, 0)
        if (time.time() - last_time) < 5 * 60:
            return
        history[qq] = time.time()
        re_path = re_speed(img_path, random.choice([30, 40, 50]))
        msg.reply(MessageSegment.image_path(re_path), at=False, quote=False)
        img_path.unlink()
        re_path.unlink()
