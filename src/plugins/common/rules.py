from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.internal.rule import Rule
from nonebot.params import CommandArg


def is_at_me(event: GroupMessageEvent) -> bool:
    for segment in event.original_message:
        if segment.type == "at" and segment.data.get("qq") == str(event.self_id):
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
