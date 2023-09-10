import threading
from functools import reduce

from common.utils.nsfw_detector import nsfw_detect
from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .sd import SDDraw, raw_b64_img

sd = SDDraw()


def txt2img(msg: GroupMsg | FriendMsg, args: list[str]):
    try:
        img_paths = sd.txt2img(args[0], width=768, height=768)
    except Exception as e:
        return
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
    base64_data = raw_b64_img(sd.img2img(url, args[0]))
    msg.reply(MessageSegment.image_b64(base64_data))


@on_command("sd",
            param_len=-1,
            priority=3,
            cmd_group_name="SD画图")
def sd_draw(msg: GroupMsg | FriendMsg, args: list[str]):
    if isinstance(msg, GroupMsg):
        if not msg.is_at_me:
            return
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    url = msg.msg_chain.get_image_urls() or msg.quote_msg and msg.quote_msg.msg_chain.get_image_urls()
    if url:
        if not args:
            args = ["masterpiece"]
        threading.Thread(target=img2img, args=(msg, args, url[0]), daemon=True).start()
    else:
        threading.Thread(target=txt2img, args=(msg, args), daemon=True).start()


