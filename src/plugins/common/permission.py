from typing import Callable

from nonebot import get_loaded_plugins, Bot
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher

TypePermissionChecker = Callable[[Matcher, Bot, Event], bool]

permission_checkers: list[TypePermissionChecker] = []


def add_permission_to_all(func: TypePermissionChecker):
    permission_checkers.append(func)


inited = False


def init_permission():
    global inited
    if inited:
        return
    plugins = get_loaded_plugins()
    for p in plugins:
        for m in p.matcher:
            def p_func(bot, event, matcher=m):
                check_result = all([func(matcher, bot, event) for func in permission_checkers])
                return check_result

            m.permission |= p_func
    inited = True
    print('Permission added to all plugins.')
