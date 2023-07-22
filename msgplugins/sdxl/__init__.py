from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sdxl_discord import SDDiscord

sd_discord = SDDiscord()
sd_discord.start()


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
            sd_discord.draw(draw_txt, lambda img_paths: self.send_img(msg, img_paths))
            # msg.reply(res_msg)

    @staticmethod
    def send_img(msg, img_paths):
        reply_msg = MessageSegment()
        for i in img_paths:
            reply_msg += MessageSegment.image_path(str(i))
        msg.reply(reply_msg)
        