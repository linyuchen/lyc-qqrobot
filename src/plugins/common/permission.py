import inspect
from typing import Callable, Coroutine

from nonebot import get_loaded_plugins, get_driver
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Bot, GroupMessageEvent
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.internal.permission import Permission

TypePermissionChecker = Callable[[Matcher, Bot, Event], bool]

inject_checkers: list[TypePermissionChecker] = []


def add_inject_permission_checker(func: TypePermissionChecker):
    inject_checkers.append(func)


inited = False


def init_permission():
    global inited
    if inited:
        return
    plugins = get_loaded_plugins()
    for p in plugins:
        for m in p.matcher:
            async def inject_check(bot, event, matcher=m):
                for func in inject_checkers:
                    result = func(matcher, bot, event)
                    if inspect.iscoroutinefunction(func) or isinstance(result, Coroutine):
                        result = await result
                    if not result:
                        return False
                return True

            def wrap_checker(checker):
                async def wrapped_checker(*args, **kwargs):
                    ori_checker_result = checker(*args, **kwargs)
                    if inspect.iscoroutinefunction(checker) or isinstance(ori_checker_result, Coroutine):
                        ori_checker_result = await ori_checker_result
                    bot = args[0] if len(args) > 0 else kwargs.get("bot")
                    event = args[1] if len(args) > 1 else kwargs.get("event")
                    inject_checker_result = await inject_check(bot, event)
                    result = ori_checker_result and inject_checker_result
                    return result

                return wrapped_checker

            if len(m.permission.checkers) == 0:
                m.permission |= Permission(inject_check)
            else:
                new_checkers = set()
                for ori_checker in m.permission.checkers:
                    new_checkers.add(wrap_checker(ori_checker))
                m.permission.checkers = new_checkers

    inited = True


def check_super_user(user_id: str):
    return user_id in get_driver().config.superusers


async def check_group_admin(bot: Bot, event: PrivateMessageEvent | GroupMessageEvent):
    if isinstance(event, PrivateMessageEvent):
        return check_super_user(str(event.user_id))
    else:
        member_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
        is_admin = member_info.get('role') in ['admin', 'owner']
        return check_super_user(str(event.user_id)) or is_admin
