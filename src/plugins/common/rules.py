from nonebot import Bot
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
        is_group = session.scene.is_group
        return is_group

    return Rule(_)

