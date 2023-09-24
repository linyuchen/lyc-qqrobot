from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, GroupSendMsg

history: dict[str, list[GroupSendMsg]] = {}  # group_qq: [msg, ...]


@on_command("", bind_msg_type=(GroupSendMsg, ), cmd_group_name="群消息撤回")
def group_msg_history(msg: GroupSendMsg, params: list[str]):
    history.setdefault(msg.group.qq, [])
    history[msg.group.qq].append(msg)


@on_command("撤回",
            bind_msg_type=(GroupMsg, ),
            param_len=-1,
            desc="撤回 撤回最近一条消息，或者对着指定消息回复撤回，或者撤回指定条数的消息，如：撤回 2",
            cmd_group_name="群消息撤回")
def recall_group_msg(msg: GroupMsg, params: list[str]):
    if msg.quote_msg:
        msg.quote_msg.recall()
        return
    group_history = history.get(msg.group.qq, [])
    msg_len = 1
    if params:
        if params[0].isdigit():
            msg_len = int(params[0])
    for i in range(msg_len):
        if len(group_history) != 0:
            group_history.pop().recall()

