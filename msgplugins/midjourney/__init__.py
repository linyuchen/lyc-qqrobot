import config
from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .midjourney_client import TaskCallbackResponse, TaskCallback, TaskType
from .midjourney_websocket_client import MidjourneyClient

from msgplugins.msgcmd.cmdaz import on_command

mj_client = MidjourneyClient(token=config.MJ_DISCORD_TOKEN,
                             channel_id=config.MJ_DISCORD_CHANNEL_ID,
                             guild_id=config.MJ_DISCORD_GUILD_ID,
                             proxy=config.GFW_PROXY)

CMD_GROUP_NAME = "MJ画图"

class LastDrawRes:
    def __init__(self, res: TaskCallbackResponse):
        self.res = res
        self.already_upscale_index = []


last_task_res = {}  # key: userid, value: TaskCallbackResponse


def get_user_id(msg: GroupMsg | FriendMsg):
    if isinstance(msg, GroupMsg):
        user_id = f"{msg.group.qq}-{msg.group_member.qq}"
    else:
        user_id = msg.friend.qq
    return user_id


@on_command("画图", alias=("sd", "画画", "绘图", "画一", "画个", "给我画", "帮我画", "画张"), param_len=1,
            desc="发送 画图+空格+描述 进行AI画图,如 画图 一只猫在天上飞",
            cmd_group_name=CMD_GROUP_NAME)
def mj_draw(msg: GroupMsg | FriendMsg, msg_param: str):
    def callback(res: TaskCallbackResponse):
        if res.error:
            msg.reply(res.error)
        elif res.image_path:
            if res.task.task_type == TaskType.DRAW:
                last_task_res[get_user_id(msg)] = LastDrawRes(res)
            msg.reply(
                MessageSegment.image_path(res.image_path[0]) +
                MessageSegment.text(f"提示词:{res.task.prompt}\n\n原图(需魔法):{res.image_urls[0]}\n"
                                    f"回复u+数字取图,如u1,上面两张为1、2，下面为3、4")
            )
            res.image_path[0].unlink(missing_ok=True)

    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    mj_client.draw(msg_param[0], callback)


@on_command("取图", alias=("U", "u"), param_len=1, int_param_index=[0], sep="", cmd_group_name=CMD_GROUP_NAME)
def mj_upscale(msg: GroupMsg | FriendMsg, msg_param: list[str]):
    last_res: LastDrawRes = last_task_res.get(get_user_id(msg))
    if not msg_param[0].isnumeric():
        return
    upscale_index = int(msg_param[0])
    if not last_res:
        msg.reply("你还没有画图哦")
        return
    if upscale_index in last_res.already_upscale_index:
        msg.reply(f"你已经取过图{upscale_index}啦")
        return
    if upscale_index < 1 or upscale_index > 4:
        msg.reply("取图序号必须在1-4之间")
        return
    last_res.already_upscale_index.append(upscale_index)
    msg.reply("正在取图中，请稍等...")
    mj_client.upscale(last_res.res, upscale_index)
