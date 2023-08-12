import random

import ifnude

from common.utils.ai_replicate import AIReplicateClient
from common.utils.downloader import download2temp
from config import REPLICATE_TOKEN
from msgplugins.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment

replicate_client = AIReplicateClient(REPLICATE_TOKEN)


@on_command("二维码",
            desc="发送 二维码 +链接或内容+ 风格，生成艺术风格二维码，如 二维码 https://bilibili.com 雪地",
            param_len=1, bind_msg_type=(GroupMsg, FriendMsg))
def gen_qrcode_cmd(msg: GroupMsg | FriendMsg, params: list[str]):
    if len(params) == 1:
        random_prompt = ["snow", "flowers", "forest", "cloud"]
        params.append("".join(random.choices(random_prompt, k=2)))
    reply_img = MessageSegment.image(replicate_client.gen_qrcode(*params))
    reply_text = MessageSegment.text(f"二维码内容： {params[0]}，如果不能识别请查看原图后重试")
    msg.reply(reply_img + reply_text)


@on_command("画图",
            desc="发送 画图+空格+描述 进行AI画图,如 画图 一只猫在天上飞",
            alias=("sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"),
            param_len=1, bind_msg_type=(GroupMsg, FriendMsg))
def gen_sdxl(msg: GroupMsg | FriendMsg, params: list[str]):
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    res = replicate_client.gen_sdxl(params[0])
    reply_paths = []
    for img_url in res:
        local_path = download2temp(img_url)
        if not ifnude.detect(str(local_path)):
            reply_paths.append(local_path)
    if reply_paths:
        # reply_msg = reduce(MessageSegment.image_path, reply_paths)
        reply_msg = MessageSegment.image_path(reply_paths[0])
        msg.reply(reply_msg + MessageSegment.text(params[0]))
    else:
        msg.reply("图片违规，已删除~")
