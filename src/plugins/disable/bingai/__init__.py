import asyncio

from nonebot import on_command, Bot
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg

from config import get_config
from src.common import PLAYWRIGHT_DATA_DIR
from src.common.bingai.bingai_playwright import BinAITaskPool, BingAIChatTask, BingAIImageResponse, BingAIDrawTask
from src.common.utils.nsfw_detector import nsfw_words_filter

bingai = BinAITaskPool(get_config('GFW_PROXY'), headless=False, data_path=PLAYWRIGHT_DATA_DIR)
bingai.start()

bingai_host = get_config("BING_AI_API")

bing_chat_cmd = on_command("#", aliases={"bing"})

bing_draw_cmd = on_command("DE3", aliases={"bing画图", "de3", "微软画图", "画图", "画画"})


@bing_chat_cmd.handle()
async def _(bot: Bot, msg: MessageEvent, params: Message = CommandArg()):
    await bing_chat_cmd.send("正在努力思考中，请稍等...")
    if isinstance(msg, GroupMessageEvent):
        user_id = str(msg.user_id) + "f"
    else:
        user_id = str(msg.group_id) + "g"

    question = params.extract_plain_text()

    def reply(result: str):
        asyncio.run(bot.send(msg, result))

    bingai.put_task(BingAIChatTask(user_id, question, reply))


@bing_draw_cmd.handle()
async def _(bot: Bot, event: MessageEvent, params: Message = CommandArg()):
    prompt = params.extract_plain_text()
    prompt = nsfw_words_filter(prompt)
    if not prompt:
        await bing_draw_cmd.finish("提示词中含有敏感词汇，请重新输入")
        return
    await bing_draw_cmd.send("正在努力画画中（吭哧吭哧~），请稍等...")

    def reply(r: BingAIImageResponse):
        asyncio.run(
            bot.send(event,
                     MessageSegment.image(r.preview) +
                     MessageSegment.text(f"提示词:{prompt}\n\n" +
                                         "\n".join([f"{index + 1}. {url}" for index, url in enumerate(r.img_urls)])
                                         )
                     )
        )

    def reply_error(err: str):
        asyncio.run(bing_draw_cmd.finish(err))

    bingai.put_task(BingAIDrawTask(prompt, reply, reply_error))
