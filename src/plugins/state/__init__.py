from nonebot import on_fullmatch

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="运行状态",
    description="查看机器人运行状态",
    usage="运行状态",
)

from src.common.state import state

state_cmd = on_fullmatch(('运行状态', 'status'))


@state_cmd.handle()
async def _():
    await state_cmd.finish(state())
