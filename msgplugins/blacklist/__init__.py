import config
from config import get_config, set_config
from qqsdk.message import GeneralMsg, GroupMsg, FriendMsg
from msgplugins.msgcmd import on_command, CMDPermissions

CONFIG_KEY = "blacklist"

black_list = get_config(CONFIG_KEY, [])


@on_command("", priority=100, cmd_group_name="黑名单", auto_destroy=False)
def check_ignore_cmd(msg: GeneralMsg, params: list[str]):
    if isinstance(msg, GroupMsg):
        qq = msg.group_member.qq
    else:
        qq = msg.qq
    if qq in black_list:
        return msg.destroy()


@on_command("加入黑名单", cmd_group_name="黑名单",
            param_len=1,
            desc="加入黑名单 QQ号",
            permission=CMDPermissions.SUPER_ADMIN)
def ignore_user(msg: GeneralMsg, params: list[str]):
    qq = params[0]
    if qq in config.get_config("ADMIN_QQ", []):
        return msg.reply("不能屏蔽超级管理员")

    if qq not in black_list:
        black_list.append(qq)
        set_config(CONFIG_KEY, black_list)
    msg.reply(f"用户{qq}已加入黑名单")


@on_command("取消黑名单", cmd_group_name="黑名单",
            param_len=1,
            desc="取消黑名单 QQ号",
            permission=CMDPermissions.SUPER_ADMIN)
def unignore_user(msg: GeneralMsg, params: list[str]):
    qq = params[0]
    if qq in black_list:
        black_list.remove(qq)
        set_config(CONFIG_KEY, black_list)
    msg.reply(f"用户{qq}已移除黑名单")
