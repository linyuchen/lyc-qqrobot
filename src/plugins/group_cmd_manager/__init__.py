import pathlib
from dataclasses import dataclass, field

from nonebot.permission import SUPERUSER
from nonebot import on_fullmatch, get_driver, on_command, on_message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageEvent, Bot, GroupMessageEvent

from src.common import DATA_DIR
from src.common.pickledb import PickleDB

DB_PATH = pathlib.Path(DATA_DIR) / 'cmd_manager.pickle'


@dataclass
class CMDManagerDataType:
    group_cmds: dict[str, set] = field(default_factory=dict)  # group_id: set[cmd]


db = PickleDB[CMDManagerDataType](DB_PATH, CMDManagerDataType())

list_cmd = on_fullmatch("屏蔽命令列表", permission=SUPERUSER)


@on_message().handle()
async def random_speed_up_gif(bot: Bot, event: MessageEvent):
    msg_text = event.message.extract_plain_text().strip()
    groups = db.db_data.group_cmds
    ignore_cmds = groups.get(vars(event).get('group_id'), set())
    for cmd in ignore_cmds:
        if msg_text.startswith(cmd):
            raise Exception(f'ignore cmd {cmd}')


@list_cmd.handle()
async def _(event: MessageEvent):
    groups = db.db_data.group_cmds
    ignore_cmds = groups.get(vars(event).get('group_id'), set())
    res = '屏蔽命令列表：' + ','.join(ignore_cmds)
    await list_cmd.finish(res)


add_cmd = on_command("添加屏蔽命令", permission=SUPERUSER)


@add_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    cmds: set[str] = db.db_data.group_cmds.get(str(event.group_id), set())
    cmds.add(cmd)
    db.save()
    add_cmd.finish('done')


del_cmd = on_command("删除屏蔽命令", permission=SUPERUSER)


@del_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    cmd = args.extract_plain_text()
    cmds: set[str] = db.db_data.group_cmds.get(str(event.group_id), set())
    try:
        cmds.remove(cmd)
    except:
        pass
    finally:
        db.save()
    del_cmd.finish('done')
