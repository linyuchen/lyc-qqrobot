# -*- coding:UTF-8 -*-

import os
import sys

import django

CURRENT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(CURRENT_PATH, "superplugin"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msgplugins.superplugin.superplugin.settings")
django.setup()

from msgplugins.superplugin.group.group_action import GroupAction, GroupPointAction
from msgplugins.superplugin.account.user_action import UserAction
from msgplugins.superplugin.globalconf.admin_action import AdminAction
from msgplugins.cmdaz import CMD
from qqsdk.message import MsgHandler, GroupMsg, FriendMsg


class GroupMsgEvent(MsgHandler):
    bind_msg_types = (GroupMsg, )

    def handle(self, msg: GroupMsg):

        # print(msg)
        user_action = UserAction(msg.group_member.qq)
        group_action = GroupAction(msg.group.qq, msg.group_member.qq)
        group_action.group_user.add_point(group_action.group_setting.talk_point)
        group_action.group_user.nick = msg.group_member.get_name()
        group_action.group_user.save()
        cmds = [
            CMD("签到", handle_func=group_action.sign),
            CMD("我的活跃度", alias=["活跃度查询", "积分", "查询活跃度"], handle_func=group_action.get_point),
            CMD("活跃度排名", alias=["活跃度排行", "排行", "排名", "活跃度排行榜", "排行榜"], handle_func=group_action.get_point_rank),
            CMD("清负活跃度", handle_func=group_action.clear_point),
            CMD("清负次数", handle_func=group_action.get_clear_chance),
            CMD("我的状态", handle_func=user_action.get_point),
            CMD("我的金币", handle_func=user_action.get_point),
            CMD("转活跃度", param_len=2, int_param_index=[1], alias=["转账"],
                handle_func=group_action.transfer_point),
            CMD("清负他人活跃度", handle_func=group_action.clear_other_point, param_len=1),
            CMD("活跃度兑换金币", handle_func=group_action.group_point2private_point, param_len=1,
                int_param_index=[0]),
            CMD("金币兑换活跃度", handle_func=group_action.private_point2group_point, param_len=1,
                int_param_index=[0]),
        ]

        result = ""
        for cmd in cmds:
            result = cmd.handle(msg.msg)
            if result:
                break

        if result:
            msg.reply(result)
            msg.destroy()


class AdminMsgEvent(MsgHandler):

    bind_msg_types = (FriendMsg, )

    def __init__(self, qq_client):
        super(AdminMsgEvent, self).__init__(qq_client)
        self.cmds = [CMD("查活跃度", handle_func=AdminAction.get_point, param_len=1),
                     CMD("加活跃度", handle_func=AdminAction.add_group_point, param_len=3,
                         int_param_index=[2]),
                     CMD("设活跃度", handle_func=AdminAction.set_group_point, param_len=3,
                         int_param_index=[2]),
                     CMD("查清负次数", handle_func=AdminAction.get_clear_chance, param_len=1,
                         int_param_index=[0]),
                     CMD("加清负次数", handle_func=AdminAction.add_clear_chance, param_len=2,
                         int_param_index=[1])
                     ]

    def handle(self, msg: FriendMsg):
        result = ""
        if not AdminAction.check_admin(msg.friend.qq):
            return

        for cmd in self.cmds:
            result = cmd.handle(msg.msg)
            if result:
                break

        if result:
            msg.reply(result)
            msg.destroy()

