from config import get_config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, FriendMsg, MessageSegment

from .bingai_playwright import BinAITaskPool, BinAITask, BingAIPlayWright

bingai_playwright = BingAIPlayWright(proxy=get_config("GFW_PROXY"), headless=False)
bingai_task_pool = BinAITaskPool(proxy=get_config("GFW_PROXY"), headless=False)
bingai_task_pool.start()


@on_command("bing",
            alias=("#", ),
            desc="bing 问题，获取bing ai的回复,如: bing 上海的天气",
            param_len=1,
            cmd_group_name="bingai"
            )
def bing(msg: GeneralMsg, params: list[str]):
    msg.reply("正在思考中……")
    if isinstance(msg, FriendMsg):
        user_id = msg.friend.qq + "f"
    else:
        user_id = msg.group.qq + "g"

    task = BinAITask(user_id, params[0], msg.reply)
    bingai_task_pool.put_question(task)


@on_command(
    "DE3",
    alias=("bing画图", "de3", "微软画图"),
    desc="DALL·E 3画图,如: DE3 一只会飞的猫猫",
)
def bingai_draw(msg: GeneralMsg, params: list[str]):
    msg.reply("正在努力画画中（吭哧吭哧~），请稍等...")
    prompt = params[0]
    res = bingai_playwright.draw(prompt)
    msg.reply(
        MessageSegment.image_path(res.image_path) +
        MessageSegment.text(f"提示词:{prompt}\n\n原图："+'\n'.join(res.image_urls))
    )
