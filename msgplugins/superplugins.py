# -*- coding:UTF-8 -*-

from msgplugins.msgcmd.cmdaz import CMD, on_command
from msgplugins.msgcmd.permission import CMDPermissions
from msgplugins.superplugin import AdminAction
from msgplugins.superplugin import GroupAction
from msgplugins.superplugin import UserAction
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg

cmd_group_name = "群活跃度"


@on_command("转活跃度",
            desc="转活跃度给他人",
            cmd_group_name=cmd_group_name,
            example="转活跃度 @喵了个咪 100",
            param_len=1,
            int_param_index=[0],
            bind_msg_type=(GroupMsg,),
            ignore_at_other=False
            )
def transfer_point(msg: GroupMsg, params: list[str]):
    group_action = GroupAction(msg.group.qq, msg.group_member.qq)
    if not msg.at_member:
        msg.reply("请@要转账的人")
        return
    target_qq = msg.at_member.qq
    result = group_action.transfer_point(target_qq, int(params[0]))
    msg.reply(result)


@on_command("我的金币", cmd_group_name=cmd_group_name,
            desc="金币可以跨群使用，可以转活跃度",
            example="我的金币",
            )
def my_gold(msg: GroupMsg | FriendMsg, params: list[str]):
    user_action = UserAction(msg.qq)
    result = user_action.get_point()
    msg.reply(result)


@on_command("活跃度转金币", cmd_group_name=cmd_group_name,
            desc="活跃度转金币",
            example="活跃度转金币 100, 100是活跃度数量",
            bind_msg_type=(GroupMsg,),
            param_len=1,
            int_param_index=[0]
            )
def point2gold(msg: GroupMsg | FriendMsg, params: list[str]):
    group_action = GroupAction(msg.group.qq, msg.group_member.qq)
    result = group_action.group_point2private_point(int(params[0]))
    msg.reply(result)


@on_command("金币转活跃度", cmd_group_name=cmd_group_name,
            desc="金币转活跃度",
            example="金币转活跃度 100, 100是金币数量",
            bind_msg_type=(GroupMsg,),
            param_len=1,
            int_param_index=[0]
            )
def gold2point(msg: GroupMsg | FriendMsg, params: list[str]):
    group_action = GroupAction(msg.group.qq, msg.group_member.qq)
    result = group_action.private_point2group_point(int(params[0]))
    msg.reply(result)


class GroupMsgEvent(MsgHandler):
    name = "群活跃度"
    cmd_name = desc = "签到\n活跃度\n活跃度排名"
    bind_msg_types = (GroupMsg,)

    def handle(self, msg: GroupMsg):

        user_action = UserAction(msg.group_member.qq)
        group_action = GroupAction(msg.group.qq, msg.group_member.qq)
        group_action.group_user.add_point(group_action.group_setting.talk_point)
        group_action.group_user.nick = msg.group_member.get_name()
        group_action.group_user.save()
        cmds = [
            CMD("签到", handle_func=group_action.sign),
            CMD("我的活跃度", alias=["活跃度查询", "查询活跃度", "活跃度"], handle_func=group_action.get_point),
            CMD("活跃度排名", alias=["活跃度排行", "活跃度排行榜", "查看排行榜"],
                handle_func=group_action.get_point_rank),
            CMD("清负活跃度", handle_func=group_action.clear_point),
            CMD("清负次数", handle_func=group_action.get_clear_chance),
            # CMD("我的状态", handle_func=user_action.get_point),
            # CMD("我的金币", handle_func=user_action.get_point),
            # CMD("转活跃度", param_len=2, int_param_index=[1], alias=["转账"],
            #     handle_func=group_action.transfer_point),
            CMD("清负他人活跃度", handle_func=group_action.clear_other_point, param_len=1),
            # CMD("活跃度兑换金币", handle_func=group_action.group_point2private_point, param_len=1,
            #     int_param_index=[0]),
            # CMD("金币兑换活跃度", handle_func=group_action.private_point2group_point, param_len=1,
            #     int_param_index=[0]),
        ]
        trigger_cmd_name = ""
        result = ""
        for cmd in cmds:
            result = cmd.handle(msg.msg)
            if result:
                trigger_cmd_name = cmd.cmd_name
                break

        if result:
            at = not (trigger_cmd_name in ["签到", "我的活跃度"])
            msg.reply(result, at)
            msg.destroy()


@on_command("设活跃度", cmd_group_name=cmd_group_name,
            desc="设活跃度，需要超级管理员权限",
            example="设活跃度 群号 群成员QQ号 100, 100是活跃度数量",
            permission=CMDPermissions.SUPER_ADMIN,
            param_len=3,
            int_param_index=[2],
            )
def set_group_point(msg: GroupMsg | FriendMsg, params: list[int]):
    result = AdminAction().set_group_point(params[0], params[1], params[2])
    msg.reply(result)


@on_command("加活跃度", cmd_group_name=cmd_group_name,
            desc="加活跃度，需要超级管理员权限",
            example="加活跃度 群号 群成员QQ号 100, 100是活跃度数量",
            permission=CMDPermissions.SUPER_ADMIN,
            param_len=3,
            int_param_index=[2],
            )
def add_group_point(msg: GroupMsg | FriendMsg, params: list[int]):
    result = AdminAction().add_group_point(params[0], params[1], params[2])
    msg.reply(result)


@on_command("查活跃度", cmd_group_name=cmd_group_name,
            desc="查活跃度，需要超级管理员权限",
            example="查活跃度 QQ号",
            permission=CMDPermissions.SUPER_ADMIN,
            param_len=1,
            int_param_index=[0],
            )
def add_group_point(msg: GroupMsg | FriendMsg, params: list[int]):
    result = AdminAction().get_point(str(params[0]))
    msg.reply(result)


class AdminMsgEvent(MsgHandler):
    name = "群活跃度"
    bind_msg_types = (FriendMsg, GroupMsg)

    def __init__(self, **kwargs):
        super(AdminMsgEvent, self).__init__(**kwargs)
        self.cmds = [
            # CMD("查活跃度", handle_func=AdminAction.get_point, param_len=1),
            # CMD("加活跃度", handle_func=AdminAction.add_group_point, param_len=3,
            #     int_param_index=[2]),
            # CMD("设活跃度", handle_func=AdminAction.set_group_point, param_len=3,
            #     int_param_index=[2]),
            CMD("查清负次数", handle_func=AdminAction.get_clear_chance, param_len=1,
                int_param_index=[0]),
            CMD("加清负次数", handle_func=AdminAction.add_clear_chance, param_len=2,
                int_param_index=[1])
        ]

    def handle(self, msg: FriendMsg):
        result = ""

        if not msg.friend.is_super_admin:
            return

        for cmd in self.cmds:
            result = cmd.handle(msg.msg)
            if result:
                break

        if result:
            msg.reply(result)
            msg.destroy()
