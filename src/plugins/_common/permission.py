from typing import Callable
from nonebot import get_loaded_plugins, Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher


def add_permission_to_all(func: Callable[[Matcher, Bot, Event], bool]):
    plugins = get_loaded_plugins()
    for p in plugins:
        for m in p.matcher:
            def p_func(bot, event, matcher=m):
                return func(matcher, bot, event)

            m.permission = m.permission | p_func