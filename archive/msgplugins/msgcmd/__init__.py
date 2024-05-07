from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.msghandler import set_msg_handler_enabled, MsgHandler
from config import set_config, get_config
from .cmdaz import on_command
from .permission import CMDPermissions

CMD_GROUP = "插件管理"


def manage_cmd_group(enabled: bool, msg: GroupMsg, cmd_group_name: str, group_qq: str):
    if cmd_group_name == CMD_GROUP:
        return msg.reply("不能管理此插件")
    op_name = "开启" if enabled else "关闭"

    try:
        set_msg_handler_enabled(cmd_group_name, enabled, group_qq)
    except Exception as e:
        msg.reply(str(e))
        return
    msg.reply(f"插件【{cmd_group_name}】已{op_name}")


def manage_global_cmd(enabled: bool, msg: GroupMsg | FriendMsg, params: list[str]):
    cmd_group_name = params[0]
    if cmd_group_name == CMD_GROUP:
        return msg.reply("不能管理此插件")
    try:
        set_msg_handler_enabled(cmd_group_name, enabled)
        msg.reply(f"插件【{cmd_group_name}】已全局{'开启' if enabled else '关闭'}")
    except Exception as e:
        msg.reply(str(e))


@on_command("开启插件",
            desc="开启插件 插件名",
            example="开启插件 斗牛",
            alias=("插件开启", "打开插件", "插件打开"),
            param_len=1,
            bind_msg_type=(GroupMsg,),
            permission=CMDPermissions.GROUP_ADMIN | CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(True, msg, params[0], msg.group.qq)


@on_command("关闭插件",
            desc="关闭插件 插件名",
            example="关闭插件 斗牛",
            alias=("插件关闭", "关闭插件", "插件关闭"),
            param_len=1,
            bind_msg_type=(GroupMsg,),
            permission=CMDPermissions.GROUP_ADMIN | CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(False, msg, params[0], msg.group.qq)


@on_command("开启全局插件",
            desc="让插件在所有群都开启，需要机器人主人权限",
            example="开启全局插件 斗牛",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_global_cmd(msg: GroupMsg, params: list[str]):
    manage_global_cmd(True, msg, params)


@on_command("关闭全局插件",
            desc="让插件在所有群都关闭，需要机器人主人权限",
            example="关闭全局插件 斗牛",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_global_cmd(msg: GroupMsg, params: list[str]):
    manage_global_cmd(False, msg, params)


@on_command("开启他群插件",
            desc="在某个群开启某个插件，需要机器人主人权限",
            example="开启他群插件 斗牛 114551",
            param_len=2,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_group_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(True, msg, params[0], params[1])


@on_command("关闭他群插件",
            desc="在某个群关闭某个插件，需要机器人主人权限",
            example="关闭他群插件 斗牛 114551",
            param_len=2,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_group_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(False, msg, params[0], params[1])


@on_command("插件列表",
            desc="插件列表, 获取所有插件名",
            cmd_group_name=CMD_GROUP,
            )
def list_cmd_group(msg: GroupMsg | FriendMsg, params: list[str]):
    reply_text = "插件列表:\n"
    exists_name = []
    is_group_msg = isinstance(msg, GroupMsg)
    for handler in msg.qq_client.msg_handlers:
        if handler.name == CMD_GROUP:
            continue
        if handler.name in exists_name:
            continue
        exists_name.append(handler.name)
        enabled = handler.check_enabled(msg.group.qq if is_group_msg else "")
        if is_group_msg:
            enabled_text = "已开启" if enabled else ("已关闭" if handler.global_enabled else "已被机器人主人关闭")
        else:
            enabled_text = "已开启" if handler.check_enabled() else "已关闭"
        reply_text += f"{handler.name} {enabled_text}\n"
    msg.reply(reply_text)


ignore_cmd_config_key = "ignore_cmd"
ignore_cmd_config = get_config(ignore_cmd_config_key, {})  # {group_qq: [cmd_name]}


@on_command("", cmd_group_name="命令屏蔽管理", priority=100, auto_destroy=False)
def check_ignore_cmd(msg: GroupMsg, params: list[str]):
    group_config: list[str] = ignore_cmd_config.get(msg.group.qq, [])
    for cmd_name in group_config:
        if msg.msg.strip().startswith(cmd_name):
            return msg.destroy()


@on_command("屏蔽命令",
            desc="屏蔽命令 命令名，如：屏蔽命令 #，则发送 #xxx 将不会触发命令",
            param_len=1,
            cmd_group_name="命令屏蔽管理",
            permission=CMDPermissions.GROUP_ADMIN)
def ignore_cmd(msg: GroupMsg, params: list[str]):
    cmd_name = params[0]
    if cmd_name == "屏蔽命令":
        return
    group_config: list[str] = ignore_cmd_config.setdefault(msg.group.qq, [])
    if cmd_name not in group_config:
        group_config.append(cmd_name)
        set_config("ignore_cmd", ignore_cmd_config)
    msg.reply(f"已屏蔽命令【{cmd_name}】")


@on_command("取消屏蔽命令",
            desc="取消屏蔽命令 命令名",
            param_len=1,
            cmd_group_name="命令屏蔽管理",
            permission=CMDPermissions.GROUP_ADMIN)
def unignore_cmd(msg: GroupMsg, params: list[str]):
    cmd_name = params[0]
    group_config: list[str] = ignore_cmd_config.get(msg.group.qq, [])
    if cmd_name in group_config:
        group_config.remove(cmd_name)
        set_config(ignore_cmd_config_key, ignore_cmd_config)
    msg.reply(f"命令【{cmd_name}】已取消屏蔽")


@on_command("查看屏蔽命令",
            desc="查看屏蔽的命令列表",
            cmd_group_name="命令屏蔽管理",
            permission=CMDPermissions.GROUP_ADMIN)
def list_ignore_cmd(msg: GroupMsg, params: list[str]):
    group_config: list[str] = ignore_cmd_config.get(msg.group.qq, [])
    if not group_config:
        msg.reply("当前群未屏蔽任何命令")
        return
    msg.reply(f"当前屏蔽命令：\n" + "\n".join(group_config))
