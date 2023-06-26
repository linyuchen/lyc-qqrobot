from qqsdk.message import MsgHandler, GroupMsg, FriendMsg
from qqsdk.message.segment import MessageSegment
from .cmdaz import CMD


class MenuPlugin(MsgHandler):
    bind_msg_types = (GroupMsg, FriendMsg)

    def collect_cmd(self, msg: GroupMsg | FriendMsg):
        friend_cmds: list[str] = []
        group_cmds: list[str] = []
        for h in self.qq_client.msg_handlers:
            if not h.desc:
                continue
            if FriendMsg in h.bind_msg_types:
                friend_cmds.append(h.desc)
            if GroupMsg in h.bind_msg_types:
                group_cmds.append(h.desc)

        if isinstance(msg, GroupMsg):
            return group_cmds
        elif isinstance(msg, FriendMsg):
            return friend_cmds
        return []

    def handle(self, msg: GroupMsg | FriendMsg):
        if CMD("菜单").az(msg.msg) or msg.msg == "":
            msg.reply("\n\n".join(self.collect_cmd(msg)))
            msg.destroy()
