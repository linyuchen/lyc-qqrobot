from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import GroupMsg, GroupSendMsg
from qqsdk.qqclient import QQClientBase


@on_command("撤回",
            bind_msg_type=(GroupMsg, ),
            param_len=-1,
            desc="撤回 撤回最近一条消息，或者对着指定消息回复撤回，或者撤回指定条数的消息，如：撤回 2",
            cmd_group_name="群消息撤回")
def recall_group_msg(msg: GroupMsg, params: list[str]):
    if msg.quote_msg:
        msg.quote_msg.recall()
        return
    qq_client: QQClientBase = msg.qq_client
    sent_ids = msg.qq_client.sent_group_msg_ids.get(msg.group.qq, [])
    msg_len = 1
    if params:
        if params[0].isdigit():
            msg_len = int(params[0])
    for i in range(msg_len):
        if len(sent_ids) != 0:
            qq_client.recall_msg(sent_ids.pop())

