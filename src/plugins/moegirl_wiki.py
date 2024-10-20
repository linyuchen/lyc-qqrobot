from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.internal.adapter import Message
from nonebot.params import CommandArg

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="萌娘百科",
    description="萌娘百科搜索网页预览",
    usage="萌娘百科 关键字"
)

from src.common.browser.webpage_screenshot import screenshot_moe_wiki
from src.plugins.common.rules import rule_args_num

moe_wiki_cmd = on_command("萌娘百科", force_whitespace=True, rule=rule_args_num(min_num=1))


@moe_wiki_cmd.handle()
async def _(params: Message = CommandArg()):
    await moe_wiki_cmd.send("正在为您搜索萌娘百科...")
    img_path = await screenshot_moe_wiki(params.extract_plain_text())
    if img_path:
        await moe_wiki_cmd.finish(MessageSegment.image(img_path))
        img_path.unlink()
