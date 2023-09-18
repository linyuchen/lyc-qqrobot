import random
import tempfile
from pathlib import Path

import requests

from common.utils.gif_speed import re_speed, is_gif
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("", cmd_group_name="随机加速gif")
def random_speed_up_gif(msg: GeneralMsg, params: list[str]):
    r_int = random.randint(0, 10)
    if r_int > 1:
        return
    img_urls = msg.msg_chain.get_image_urls()
    if img_urls:
        img_url = img_urls[0]
        # 判断是否是gif
        img_path = Path(tempfile.mktemp(suffix=".gif"))
        img_data = requests.get(img_url).content
        with open(img_path, "wb") as f:
            f.write(img_data)
        if not is_gif(img_path):
            return
        re_path = re_speed(img_path, random.choice([30, 40, 50]))
        msg.reply(MessageSegment.image_path(re_path), at=False)
        img_path.unlink()
        re_path.unlink()
