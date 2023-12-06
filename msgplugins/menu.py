from msgplugins.msgcmd.cmdaz import CMD
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg


class MenuPlugin(MsgHandler):
    name = "菜单"
    bind_msg_types = (GroupMsg, FriendMsg)

    def collect_cmd(self, msg: GroupMsg | FriendMsg):
        friend_cmds: list[str] = []
        group_cmds: list[str] = []
        last_name = ""
        handlers = msg.qq_client.msg_handlers[:]
        handlers.sort(key=lambda x: x.name)
        for handler in handlers:
            if not handler.desc:
                continue
            handler: MsgHandler
            if not handler.check_enabled():
                continue
            desc_start_str = "\n" if handler.name == last_name else "\n\n"
            last_name = handler.name
            if FriendMsg in handler.bind_msg_types:
                friend_cmds.append(desc_start_str + handler.desc)
            if GroupMsg in handler.bind_msg_types and isinstance(msg, GroupMsg):
                if not handler.check_enabled(msg.group.qq):
                    continue
                group_cmds.append(desc_start_str + handler.desc)

        if isinstance(msg, GroupMsg):
            return group_cmds
        elif isinstance(msg, FriendMsg):
            return friend_cmds
        return []

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("menu").az(msg.msg) or (not msg.msg.strip() and getattr(msg, "is_at_me", False)):
            if msg.quote_msg and not msg.msg.strip():
                return
            if isinstance(msg, GroupMsg) and msg.is_at_other:
                return
            msg.destroy()
            res = "命令列表(@机器人后发送命令即可触发)：" + "".join(self.collect_cmd(msg))
            msg.reply(res)
