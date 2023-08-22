from functools import reduce
from pathlib import Path

import ifnude

from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .tusi import TusiMultipleCountPool

tusi = TusiMultipleCountPool()


@on_command("画图",
            alias=("画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"),
            param_len=1,
            auto_destroy=False,
            priority=2,
            cmd_group_name="吐司画图")
def ts_draw(msg: GroupMsg | FriendMsg, args: list[str]):
    # msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    def cb(img_paths: list[Path]):
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

    tusi.txt2img(args[0], cb)
