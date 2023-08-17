import config
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .midjourney_client import MidjourneyClient, TaskCallbackParam, TaskCallback

from ..cmdaz import on_command

mj_client = MidjourneyClient(url=config.MJ_DISCORD_CHANNEL_URL, token=config.MJ_DISCORD_TOKEN,
                             http_proxy=config.GFW_PROXY)


@on_command("画图", alias=("sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"), param_len=1,
            desc="发送 画图+空格+描述 进行AI画图,如 画图 一只猫在天上飞")
def mj_draw(msg: GroupMsg | FriendMsg, msg_param: str):
    def callback(param: TaskCallbackParam):
        if param.error:
            msg.reply(param.error)
        elif param.image_path:
            msg.reply(
                MessageSegment.image_path(param.image_path[0]) +
                MessageSegment.text(f"提示词:{param.prompt}\n\n原图(需魔法):{param.image_urls[0]}")
            )
            param.image_path[0].unlink(missing_ok=True)

    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    mj_client.draw(msg_param[0], callback)
