from nonebot import on_command
from nonebot.internal.adapter import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg

__plugin_meta__ = PluginMetadata(
    name="萌娘百科",
    description="萌娘百科搜索网页预览",
    usage="萌娘百科 关键字"
)

from src.common.browser.screenshot.moegirl import screenshot_moe_wiki
from src.plugins.common.rules import rule_args_num

moe_wiki_cmd = on_command("萌娘百科", force_whitespace=True, rule=rule_args_num(min_num=1))


@moe_wiki_cmd.handle()
async def _(params: Message = CommandArg()):
    await moe_wiki_cmd.send("正在为您搜索萌娘百科...")
    img_path = await screenshot_moe_wiki(params.extract_plain_text())
    if img_path:
        data = img_path.read_bytes()
        img_path.unlink()
        await moe_wiki_cmd.finish(await UniMsg.image(raw=data).export())

