from nonebot import get_driver
from .permission import init_permission


@get_driver().on_startup
async def _():
    await init_permission()
