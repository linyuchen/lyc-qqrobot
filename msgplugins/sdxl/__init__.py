from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sdxl_discord import SDDiscord
from ..chatgpt.chatgpt import trans2en

# sd_discord = SDDiscord()
# sd_discord.start()


class SDXLPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True

    def handle(self, msg: GroupMsg | FriendMsg):
        sep = " "
        if isinstance(msg, GroupMsg):
            if msg.is_at_me:
                sep = ""
        draw_cmd = CMD("画图", alias=["sd", "画画", "绘图", "画一个"], param_len=1, sep=sep)

        if draw_cmd.az(msg.msg):
            msg.destroy()

            msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
            draw_txt = draw_cmd.get_original_param()
            return
            img_paths = sd_discord.draw(draw_txt)
            res_msg = MessageSegment()
            for img_path in img_paths:
                res_msg += MessageSegment.image_path(img_path)
            msg.reply(res_msg)
