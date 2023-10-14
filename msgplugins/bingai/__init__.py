from config import get_config
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg

from .bingai_playwright import BinAITaskPool, BinAITask

bingai_task_pool = BinAITaskPool(proxy=get_config("GFW_PROXY"), headless=False)
bingai_task_pool.start()


@on_command("bing",
            desc="bing 问题，获取bing ai的回复,如: bing 上海的天气",
            param_len=1,
            cmd_group_name="bingai"
            )
def bing(msg: GeneralMsg, params: list[str]):
    msg.reply("正在思考中……")
    bingai_task_pool.put_question(BinAITask(params[0], msg.reply))
