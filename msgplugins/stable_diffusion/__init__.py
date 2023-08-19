from functools import reduce
from pathlib import Path

import ifnude

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .sd import SDDraw
from ..cmdaz import on_command

# get_models_cmd = CMD("查看画图模型", alias=["画图模型", "查看模型", "切换模型", "设置模型"], param_len=0)
# get_loras_cmd = CMD("查看lora", param_len=0)
# set_model_cmd = CMD("设置画图模型", alias=["画图模型", "设置模型", "切换模型", "切换画图模型"], param_len=1,
#                     sep=sep)
# draw_cmd = CMD("画图", alias=["sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"], param_len=1,
#                sep=sep)
# draw_hd_cmd = CMD("画图hd", param_len=1, sep=sep)

sd = SDDraw()


@on_command("画图", alias=("sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"), param_len=1)
def sd_draw(msg: GroupMsg | FriendMsg, args: list[str]):
    img_paths = sd.txt2img(args[0])
    for img_path in img_paths[:]:
        if ifnude.detect(str(img_path)):
            img_path.unlink()
            img_paths.remove(img_path)
    if img_paths:
        reply_msg = reduce(lambda x, y: MessageSegment.image_path(x) + MessageSegment.image_path(y),
                           img_paths,
                           MessageSegment.image_path(img_paths[0]))
        msg.reply(reply_msg)
        for i in img_paths:
            i.unlink(missing_ok=True)
    else:
        msg.reply("图片违规，已被删除")

