import httpx
from nonebot import on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name="{插件名称}",
    description="{插件介绍}",
    usage="{插件用法}",

    type="{插件分类}",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="{项目主页}",
    # 发布必填。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

from nonebot.plugin import PluginMetadata

news_cmd = on_fullmatch(("今日新闻", '早报', '晚报'))


@news_cmd.handle()
async def _():
    url = "http://dwz.2xb.cn/zaob"
    async with httpx.AsyncClient() as client:
        image_url = (await client.get(url)).json().get("imageUrl")
        await news_cmd.finish(MessageSegment.image(image_url))
