import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

news_cmd = on_command("今日新闻", aliases={'早报', '晚报'})


@news_cmd.handle()
async def _():
    url = "http://dwz.2xb.cn/zaob"
    async with httpx.AsyncClient() as client:
        image_url = (await client.get(url)).json().get("imageUrl")
        await news_cmd.finish(MessageSegment.image(image_url))
