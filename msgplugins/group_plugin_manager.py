import config
from config import ADMIN_QQ, plugins
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from .cmdaz import CMD


def get_plugins(group_qq):
    plugins = config.plugins
    res = "插件列表\n"
    for plugin_name in plugins:
        can_group_manage = plugins[plugin_name].get("can_group_manage", True)
        if not can_group_manage:
            continue
        enabled = group_qq not in plugins[plugin_name].get("exclude_groups", [])
        global_enabled = plugins[plugin_name].get("enabled", True)
        enabled = enabled and global_enabled
        summary = plugins[plugin_name].get("summary", "")
        status = f"{'已开启' if enabled else '已关闭'}"
        if not global_enabled:
            status = "已被机器人主人关闭"
        res += f"插件名:{plugin_name}, {summary}, {status}\n"

    return res


class GroupPluginManager(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)
    desc = "发送 插件列表 即可查看各插件状态\n" + \
           "发送 关闭插件+空格+插件名 即可关闭插件\n" + \
           "发送 开启插件+空格+插件名 即可开启插件"

    def handle(self, msg: GroupMsg | FriendMsg):
        plugin_name = ""
        group_qq = ""
        plugin_enabled = False
        if isinstance(msg, FriendMsg):
            if msg.friend.qq == str(ADMIN_QQ):
                cmd = cmd_open = CMD("开启插件", param_len=2, int_param_index=[2])
                cmd_close = CMD("关闭插件", param_len=2, int_param_index=[2])
                if cmd_open.az(msg.msg):
                    cmd = cmd_open
                    plugin_enabled = True
                elif cmd_close.az(msg.msg):
                    plugin_enabled = False
                    cmd = cmd_close
                else:
                    return
                cmd_param = cmd.get_param_list()
                plugin_name, group_qq = cmd_param
            else:
                return
        else:
            cmd_open = CMD("开启插件", param_len=1, sep="")
            cmd_close = CMD("关闭插件", param_len=1, sep="")
            cmd_plugins = CMD("插件列表", alias=["查看插件", "管理插件"], param_len=0)
            if cmd_plugins.az(msg.msg):
                msg.reply(get_plugins(msg.group.qq))
                msg.destroy()
                return
            if cmd_open.az(msg.msg):
                plugin_enabled = True
                cmd = cmd_open
            elif cmd_close.az(msg.msg):
                plugin_enabled = False
                cmd = cmd_close
            else:
                return

            plugin_name = cmd.get_param_list()[0]
            group_qq = msg.group.qq

        if plugin_name:
            if not msg.group_member.isAdmin and msg.group_member.qq != str(ADMIN_QQ):
                msg.reply("插件管理仅管理员或群主可用")
                return
            # 如果插件不能被管理
            if not plugins[plugin_name].get("can_group_manage", True):
                return
            if plugin_name in plugins:
                groups = plugins[plugin_name].get("exclude_groups", [])
                groups = list(set(groups))
                if plugin_enabled:
                    if group_qq in groups:
                        groups.remove(group_qq)
                    msg.reply(f"插件【{plugin_name}】已开启")
                else:
                    if group_qq not in groups:
                        groups.append(group_qq)
                    msg.reply(f"插件【{plugin_name}】已关闭")
                plugins[plugin_name]["exclude_groups"] = groups
                config.plugins = plugins
                config.save_config()
            else:
                msg.reply(f"插件名有误，插件【{plugin_name}】不存在")
            msg.destroy()
