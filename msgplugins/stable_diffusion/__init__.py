import threading
from functools import reduce

import requests
from requests.exceptions import ConnectionError

from common.logger import logger
from common.utils.nsfw_detector import nsfw_detect
from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .sd import SDDraw, raw_b64_img

sd = SDDraw()


def txt2img(msg: GroupMsg | FriendMsg, args: list[str]):
    try:
        img_paths = sd.txt2img(args[0], width=768, height=768)
    except ConnectionError as e:
        logger.error(e)
        return msg.reply(f"画图失败，可能主人把SD给关掉了，等主人回来后开启吧")
    except Exception as e:
        logger.error(e)
        return msg.reply(f"画图失败，请检查图片或者提示词")
    for img_path in img_paths[:]:
        if nsfw_detect(img_path):
            img_path.unlink()
            img_paths.remove(img_path)
    if img_paths:
        msgs = [MessageSegment.image_path(img_path) for img_path in img_paths]
        reply_msg = reduce(lambda a, b: a + b, msgs)
        msg.reply(reply_msg)
        for i in img_paths:
            i.unlink(missing_ok=True)
    else:
        msg.reply("图片违规，已被删除")


def img2img(msg: GroupMsg | FriendMsg, args: list[str], url):
    try:
        base64_data = raw_b64_img(sd.img2img(url, args[0]))
    except ConnectionError as e:
        logger.error(e)
        return msg.reply(f"画图失败，可能主人把SD给关掉了，等主人回来后开启吧")
    except Exception as e:
        logger.error(e)
        return msg.reply(f"画图失败，请检查图片或者提示词")

    msg.reply(MessageSegment.image_b64(base64_data))


@on_command("sd",
            alias=("SD", ),
            desc="sd画图，支持图生图，示例：sd 猫耳女孩",
            param_len=-1,
            priority=3,
            cmd_group_name="SD画图")
def sd_draw(msg: GroupMsg | FriendMsg, args: list[str]):
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    url = msg.msg_chain.get_image_urls() or msg.quote_msg and msg.quote_msg.msg_chain.get_image_urls()
    if not url and not args:
        return
    if url:
        if not args:
            args = ["masterpiece"]
        threading.Thread(target=img2img, args=(msg, args, url[0]), daemon=True).start()
    else:
        threading.Thread(target=txt2img, args=(msg, args), daemon=True).start()
