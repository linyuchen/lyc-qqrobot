from nonebot import on_fullmatch

from src.common.state import state

state_cmd = on_fullmatch(('运行状态', 'status'))


@state_cmd.handle()
async def _():
    await state_cmd.finish(state())
