from qqsdk.message import GroupMsg, FriendMsg
from qqsdk.message.msghandler import set_msg_handler_enabled, MsgHandler
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
            alias=("插件开启", "打开插件", "插件打开"),
            param_len=1,
            bind_msg_type=(GroupMsg,),
            permission=CMDPermissions.GROUP_ADMIN | CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(True, msg, params[0], msg.group.qq)


@on_command("关闭插件",
            alias=("插件关闭", "关闭插件", "插件关闭"),
            param_len=1,
            bind_msg_type=(GroupMsg,),
            permission=CMDPermissions.GROUP_ADMIN | CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(False, msg, params[0], msg.group.qq)


@on_command("开启全局插件",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_global_cmd(msg: GroupMsg, params: list[str]):
    manage_global_cmd(True, msg, params)


@on_command("关闭全局插件",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_global_cmd(msg: GroupMsg, params: list[str]):
    manage_global_cmd(False, msg, params)


@on_command("开启他群插件",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def open_group_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(False, msg, params[0], params[1])


@on_command("关闭他群插件",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN,
            cmd_group_name=CMD_GROUP)
def close_group_cmd(msg: GroupMsg, params: list[str]):
    manage_cmd_group(False, msg, params[0], params[1])


@on_command("插件列表",
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

