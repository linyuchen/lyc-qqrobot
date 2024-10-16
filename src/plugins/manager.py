from contextlib import AsyncExitStack
from typing import Optional

from nonebot import get_loaded_plugins, Bot, get_driver
from nonebot.adapters import Event
from nonebot.typing import T_DependencyCache
from nonebot.plugin import Plugin
from nonebot.matcher import Matcher
driver = get_driver()


def manager_permission(matcher: Matcher, bot: Bot, event: Event):
    plugin: Plugin = matcher.plugin
    plugin_name = plugin.metadata.name
    plugin_id = plugin.id_
    return True


@driver.on_startup
async def _():
    plugins = get_loaded_plugins()
    for p in plugins:
        for m in p.matcher:
            def p_func(bot, event, matcher=m):
                return manager_permission(matcher=matcher, bot=bot, event=event)
            m.permission = m.permission | p_func
