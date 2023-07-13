import os

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from ..cmdaz import CMD
from .sd import txt2img, get_models, set_model


class SDPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True
    desc = "发送 画图+空格+描述 进行AI画图\n发送" + \
        "\n发送 查看画图模型 获取模型列表\n发送 设置画图模型+空格+模型名 设置模型"

    def handle(self, msg: GroupMsg | FriendMsg):
        get_models_cmd = CMD("查看画图模型", param_len=0)
        set_model_cmd = CMD("设置画图模型", param_len=1, sep=" ")
        draw_cmd = CMD("画图", alias=["sd"], param_len=1, sep=" ")
        draw_txt = ""
        if get_models_cmd.az(msg.msg):
            msg.reply(get_models())
            msg.destroy()
            return
        elif set_model_cmd.az(msg.msg):
            model_name = set_model_cmd.get_original_param().strip()
            msg.reply(set_model(model_name))
            msg.destroy()
        elif draw_cmd.az(msg.msg):
            draw_txt = draw_cmd.get_original_param()
        if draw_txt:
            image_path = txt2img(draw_txt)
            reply_msg = MessageSegment.image_path(image_path)
            msg.reply(reply_msg)
            os.remove(image_path)
            msg.destroy()
            return



