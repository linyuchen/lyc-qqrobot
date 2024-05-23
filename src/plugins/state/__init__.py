from nonebot import on_command

from src.common.state import state

state_cmd = on_command('运行状态', aliases={'status', })


@state_cmd.handle()
async def _():
    await state_cmd.finish(state())
