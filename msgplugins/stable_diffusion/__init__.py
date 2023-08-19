from functools import reduce

import ifnude

from qqsdk.message import GroupMsg, FriendMsg
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


@on_command("画图", alias=("sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"), param_len=1, auto_destroy=False)
def sd_draw(msg: GroupMsg | FriendMsg, args: list[str]):
    # msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    try:
        img_paths = sd.txt2img(args[0], width=512, height=512)
    except Exception as e:
        return
    for img_path in img_paths[:]:
        if ifnude.detect(str(img_path)):
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
