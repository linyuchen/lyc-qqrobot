import inspect
from typing import Callable, Awaitable, Coroutine, Type

from nonebot import Bot, get_loaded_plugins
from nonebot.internal.matcher import Matcher
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg, Event, Message
from nonebot_plugin_alconna import UniMsg, At
from nonebot_plugin_uninfo import Uninfo, get_session


def is_at_me(session: Uninfo, msg: UniMsg) -> bool:
    ats = msg.get(At)
    for segment in ats:
        if segment.target == str(session.self_id):
            return True


def rule_args_num(num=None, min_num=None, max_num=None):
    def _(args: Message = CommandArg()):
        args_len = len(args.extract_plain_text().split())
        if not (num is None):
            return args_len == num
        if not (min_num is None):
            if args_len < min_num:
                return False
        if not (max_num is None):
            if args_len > max_num:
                return False

        return True

    return Rule(_)


def rule_is_group_msg():
    """
    """

    async def _(bot: Bot, event: Event):
        session = await get_session(bot, event)
        is_group = session and session.scene.is_group
        return is_group

    return Rule(_)


TypeRuleChecker = Callable[[Type[Matcher], Bot, Event], bool] | Awaitable
inject_checkers: list[TypeRuleChecker] = []


def inject_plugin_rule(func: TypeRuleChecker):
    # 给每个插件注入规则检查函数
    inject_checkers.append(func)


inited = False


async def init_rules():
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

            m.rule &= Rule(inject_check)

    inited = True
