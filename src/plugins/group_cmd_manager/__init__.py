from nonebot import on_fullmatch, on_command, get_driver
from nonebot.adapters.onebot.v11 import Message, MessageEvent, Bot, GroupMessageEvent
from nonebot.internal.adapter import Event
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata

from .util import check_group_message, get_group_ignore_cmds, add_group_ignore_cmd, remove_group_ignore_cmd

__plugin_meta__ = PluginMetadata(
    name="群命令屏蔽",
    description="群里设置屏蔽某些命令",
    usage="屏蔽命令列表、添加屏蔽命令 命令名、删除屏蔽命令 命令名",
)

from ..common.permission import add_inject_permission_checker

driver = get_driver()


def check_group_cmd_permission(matcher: Matcher, bot: Bot, event: Event):
    message = getattr(event, 'message', None)
    if not message:
        return True
    msg_text = message.extract_plain_text().strip()
    not_ignore = check_group_message(vars(event).get('group_id'), msg_text)
    return not_ignore


@driver.on_startup
async def _():
    add_inject_permission_checker(check_group_cmd_permission)


list_cmd = on_fullmatch("屏蔽命令列表", permission=SUPERUSER)


@list_cmd.handle()
async def _(event: MessageEvent):
    group_id = vars(event).get('group_id')
    res = '屏蔽命令列表：' + '，'.join(get_group_ignore_cmds(group_id))
    await list_cmd.finish(res)


add_cmd = on_command("添加屏蔽命令", permission=SUPERUSER)


@add_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    add_group_ignore_cmd(str(event.group_id), cmd)
    await add_cmd.finish('done')


del_cmd = on_command("删除屏蔽命令", permission=SUPERUSER)


@del_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    remove_group_ignore_cmd(str(event.group_id), cmd)
    await del_cmd.finish('done')
