from common.cmd_alias import CMD_ALIAS_DRAW
from common.utils.nsfw_detector import nsfw_words_filter
from config import get_config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, FriendMsg, MessageSegment

from .bingai_playwright import BinAITaskPool, BingAIChatTask, BingAIPlayWright, BingAIDrawTask, BingAIImageResponse

bingai_task_pool = BinAITaskPool(proxy=get_config("GFW_PROXY"), headless=False)
bingai_task_pool.start()


@on_command("bing",
            alias=("#",),
            desc="获取bing ai的回复,如: bing 上海的天气",
            example="bing 上海的天气",
            param_len=1,
            cmd_group_name="bingai"
            )
def bing(msg: GeneralMsg, params: list[str]):
    msg.reply("正在思考中……")
    if isinstance(msg, FriendMsg):
        user_id = msg.friend.qq + "f"
    else:
        user_id = msg.group.qq + "g"

    task = BingAIChatTask(user_id, params[0], msg.reply)
    bingai_task_pool.put_task(task)


@on_command(
    "DE3",
    alias=("bing画图", "de3", "微软画图") + CMD_ALIAS_DRAW,
    priority=5,
    param_len=1,
    desc="DALL·E 3画图,如: DE3 一只会飞的猫猫",
    cmd_group_name="bingai",
)
def bingai_draw(msg: GeneralMsg, params: list[str]):
    prompt = params[0]
    prompt = nsfw_words_filter(prompt)
    if not prompt:
        msg.reply("提示词中含有敏感词汇，请重新输入")
        return
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")

    def reply(resp: BingAIImageResponse):
        msg.reply(
            MessageSegment.image_path(resp.preview) +
            MessageSegment.text(f"提示词:{prompt}\n\n原图：" + '\n'.join(resp.img_urls))
        )

    bingai_task_pool.put_task(BingAIDrawTask(prompt, reply))
