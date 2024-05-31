import pathlib
from dataclasses import dataclass, field

from nonebot import on_fullmatch, get_driver, on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.message import event_preprocessor
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from src.common import DATA_DIR
from src.common.pickledb import PickleDB
from src.plugins.common.rules import rule_args_num

BLACK_DB_PATH = pathlib.Path(DATA_DIR) / 'blacklist.pickle'

superusers = get_driver().config.superusers


@dataclass
class BlackListDataType:
    user_ids: set[str] = field(default_factory=set)
    group_ids: set[str] = field(default_factory=set)


black_list_db = PickleDB[BlackListDataType](BLACK_DB_PATH, BlackListDataType())

black_list_cmd = on_fullmatch("黑名单", permission=SUPERUSER)


@black_list_cmd.handle()
async def _():
    black_users = black_list_db.db_data.user_ids
    black_groups = black_list_db.db_data.group_ids
    res = '黑名单群: ' + '，'.join(black_groups) + '\n黑名单用户:' + '，'.join(black_users)
    await black_list_cmd.finish(res)


add_black_group_cmd = on_command('拉黑群', force_whitespace=True, permission=SUPERUSER, rule=rule_args_num(num=1))


@add_black_group_cmd.handle()
async def _(args: Message = CommandArg()):
    group_id = args.extract_plain_text()
    black_list_db.db_data.group_ids.add(group_id)
    black_list_db.save()
    await add_black_group_cmd.finish('done')


add_black_user_cmd = on_command('拉黑用户', force_whitespace=True, permission=SUPERUSER, rule=rule_args_num(1))


@add_black_user_cmd.handle()
async def _(args: Message = CommandArg()):
    user_id = args.extract_plain_text()
    black_list_db.db_data.user_ids.add(user_id)
    black_list_db.save()
    await add_black_user_cmd.finish('done')


del_black_group_cmd = on_command('取消拉黑群', force_whitespace=True, permission=SUPERUSER, rule=rule_args_num(1))


@del_black_group_cmd.handle()
async def _(args: Message = CommandArg()):
    group_id = args.extract_plain_text()
    try:
        black_list_db.db_data.group_ids.remove(group_id)
        black_list_db.save()
    except Exception as e:
        pass
    await del_black_group_cmd.finish('done')


del_black_user_cmd = on_command('取消拉黑用户', force_whitespace=True, permission=SUPERUSER, rule=rule_args_num(1))


@del_black_user_cmd.handle()
async def _(args: Message = CommandArg()):
    user_id = args.extract_plain_text()
    try:
        black_list_db.db_data.user_ids.remove(user_id)
        black_list_db.save()
    except Exception as e:
        pass
    await del_black_user_cmd.finish('done')


@event_preprocessor
async def _(event: MessageEvent):
    user_id = vars(event).get('user_id')
    user_id = str(user_id) if user_id else None
    group_id = vars(event).get('group_id')
    group_id = str(group_id) if group_id else None
    black_users = black_list_db.db_data.user_ids
    black_groups = black_list_db.db_data.group_ids
    if user_id in superusers:
        return
    if user_id in black_users:
        raise Exception(f'ignore black user {user_id}')

    if group_id in black_groups:
        raise Exception(f'ignore black group {group_id}')
