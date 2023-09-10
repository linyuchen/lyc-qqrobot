import config
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from msgplugins.msgcmd.cmdaz import CMD


class MenuPlugin(MsgHandler):
    name = "菜单"
    bind_msg_types = (GroupMsg, FriendMsg)

    def collect_cmd(self, msg: GroupMsg | FriendMsg):
        friend_cmds: list[str] = []
        group_cmds: list[str] = []
        for handler in msg.qq_client.msg_handlers:
            if not handler.desc:
                continue
            handler: MsgHandler
            if not handler.check_enabled():
                continue
            if FriendMsg in handler.bind_msg_types:
                friend_cmds.append(handler.desc)
            if GroupMsg in handler.bind_msg_types and isinstance(msg, GroupMsg):
                if not handler.check_enabled(msg.group.qq):
                    continue
                group_cmds.append(handler.desc)

        if isinstance(msg, GroupMsg):
            return group_cmds
        elif isinstance(msg, FriendMsg):
            return friend_cmds
        return []

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("菜单", alias=["功能", "帮助"]).az(msg.msg) or (not msg.msg.strip() and getattr(msg, "is_at_me", False)):
            if msg.quote_msg and not msg.msg.strip():
                return
            msg.destroy()
            res = "命令列表(@机器人后发送命令即可触发)：\n\n" + "\n\n".join(self.collect_cmd(msg))
            msg.reply(res)
