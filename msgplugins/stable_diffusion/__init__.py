from pathlib import Path

from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .sd import SDDraw
from .tusi import TusiDraw, MultipleCountPool
from ..cmdaz import CMD
from ..midjourney import TaskCallbackParam

sd = TusiDraw("")
# txt2img = MultipleCountPool().txt2img
get_models = sd.get_models
set_model = sd.set_model
get_loras = sd.get_loras
use_online = isinstance(sd, TusiDraw)


class SDPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    is_async = True
    desc = "发送 画图+空格+描述 进行AI画图\n"

    # "发送 查看画图模型 获取模型列表\n发送 设置画图模型+空格+模型名 设置模型\n" + \
    # "发送 查看lora 获取lora关键字列表, 画图时加上lora关键字可形成特定风格\n"

    def send_img(self, msg: GroupMsg | FriendMsg, img_paths: list[Path]):
        if isinstance(img_paths, Path):
            img_paths = [img_paths]
        for img_path in img_paths:
            if img_path:
                msg.reply(MessageSegment.image_path(str(img_path)))
                img_path.unlink(missing_ok=True)
            else:
                msg.reply("图片违规，已被删除")

    def handle(self, msg: GroupMsg | FriendMsg):
        sep = " "
        if isinstance(msg, GroupMsg):
            if msg.is_at_me:
                sep = ""
        get_models_cmd = CMD("查看画图模型", alias=["画图模型", "查看模型", "切换模型", "设置模型"], param_len=0)
        get_loras_cmd = CMD("查看lora", param_len=0)
        set_model_cmd = CMD("设置画图模型", alias=["画图模型", "设置模型", "切换模型", "切换画图模型"], param_len=1,
                            sep=sep)
        draw_cmd = CMD("画图", alias=["sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"], param_len=1,
                       sep=sep)
        draw_hd_cmd = CMD("画图hd", param_len=1, sep=sep)
        draw_txt = ""
        if get_models_cmd.az(msg.msg):
            msg.destroy()
            msg.reply(get_models())
            return
        elif get_loras_cmd.az(msg.msg):
            msg.destroy()
            msg.reply(get_loras())
            return
        elif set_model_cmd.az(msg.msg):
            msg.destroy()
            model_name = set_model_cmd.get_original_param().strip()
            # msg.reply("正在设置模型，请稍等...")
            msg.reply(set_model(model_name))
        elif draw_cmd.az(msg.msg) or draw_hd_cmd.az(msg.msg):
            draw_txt = draw_cmd.get_original_param()
        if draw_txt:
            msg.destroy()
            if draw_hd_cmd.az(msg.msg):
                width = 1024
                height = 768
            else:
                width = 600
                height = 800
            # msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
            if use_online:
                # error = txt2img(draw_txt, callback=lambda img_paths: self.send_img(msg, img_paths))
                def callback(param: TaskCallbackParam):
                    if param.error:
                        msg.reply(param.error)
                    else:
                        msg.reply(
                            MessageSegment.image_path(param.image_path[0]) +
                            MessageSegment.text(f"提示词:{param.prompt}\n\n原图(需魔法):{param.image_urls[0]}")
                        )
                # mj_client.draw(draw_txt, callback)
                # error = draw(draw_txt, callback=lambda img_paths, other_info: self.send_img(msg, img_paths) or msg.reply("原图：" + other_info))
                # if error:
                #     msg.reply(error)
            else:
                pass
                # image_path = txt2img(draw_txt, width=1024, height=1024)
                # if ifnude.detect(image_path):
                #     msg.reply("图片违规，已被删除")
                #     os.remove(str(image_path))
                #     return
                # reply_msg = MessageSegment.image_path(str(image_path))
                # msg.reply(reply_msg)
                # os.remove(str(image_path))
            return
