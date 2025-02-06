from nonebot import get_driver
from .rules import init_rules


@get_driver().on_startup
async def _():
    await init_rules()
