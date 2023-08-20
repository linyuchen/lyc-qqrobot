import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .cmdaz import CMD


class MenuPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def collect_cmd(self, msg: GroupMsg | FriendMsg):
        friend_cmds: list[str] = []
        group_cmds: list[str] = []
        plugins = config.plugins
        for h in self.qq_client.msg_handlers:
            if not h.desc:
                continue
            h: MsgHandler
            plugin_name = h.get_module_name()
            if not plugins[plugin_name].get("enabled", True):
                continue
            if FriendMsg in h.bind_msg_types:
                friend_cmds.append(h.desc)
            if GroupMsg in h.bind_msg_types and isinstance(msg, GroupMsg):
                exclude_groups = plugins[plugin_name].get("exclude_groups", [])
                exclude_groups = map(str, exclude_groups)
                if msg.group.qq in exclude_groups:
                    continue
                group_cmds.append(h.desc)

        if isinstance(msg, GroupMsg):
            return group_cmds
        elif isinstance(msg, FriendMsg):
            return friend_cmds
        return []

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("菜单", alias=["功能", "帮助"]).az(msg.msg) or (not msg.msg.strip() and getattr(msg, "is_at_me", False)):
            msg.reply("\n\n".join(self.collect_cmd(msg)))
            msg.destroy()
