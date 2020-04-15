# -*- coding:UTF-8 -*-

import os
import sys

import django

import plugin
CURRENT_PATH = os.path.dirname(__file__)
# print(CURRENT_PATH)
sys.path.append(os.path.join(CURRENT_PATH, "superplugin"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superplugin.superplugin.settings")
django.setup()

from superplugin.group.group_action import GroupAction, GroupPointAction
from superplugin.account.user_action import UserAction
from superplugin.globalconf.admin_action import AdminAction
# from superplugin.globalconf.models import *
# from superplugin.group.models import *
from cmdaz import CMD


class GroupMsgEvent(plugin.webqqsdk.msgevent.MsgEvent):

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        :param msg: Message
        """

        # print(msg)
        user_action = UserAction(msg.groupMember.qq)
        group_action = GroupAction(msg.group.qq, msg.groupMember.qq)
        group_action.group_user.add_point(group_action.group_setting.talk_point)
        group_action.group_user.nick = msg.groupMember.get_name()
        group_action.group_user.save()
        cmds = [
            CMD(u"签到", handle_func=group_action.sign),
            CMD(u"我的活跃度", handle_func=group_action.get_point),
            CMD(u"活跃度排名", handle_func=group_action.get_point_rank),
            CMD(u"清负活跃度", handle_func=group_action.clear_point),
            CMD(u"清负次数", handle_func=group_action.get_clear_chance),
            CMD(u"我的状态", handle_func=user_action.get_point),
            CMD(u"我的金币", handle_func=user_action.get_point),
            CMD(u"转活跃度", param_len=2, int_param_index=[1],
                handle_func=group_action.transfer_point),
            CMD(u"清负他人活跃度", handle_func=group_action.clear_other_point, param_len=1),
            CMD(u"活跃度兑换金币", handle_func=group_action.group_point2private_point, param_len=1,
                int_param_index=[0]),
            CMD(u"金币兑换活跃度", handle_func=group_action.private_point2group_point, param_len=1,
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


class AdminMsgEvent(plugin.webqqsdk.msgevent.MsgEvent):

    def __init__(self):
        super(AdminMsgEvent, self).__init__()
        self.cmds = [CMD(u"查活跃度", handle_func=AdminAction.get_point, param_len=1),
                     CMD(u"加活跃度", handle_func=AdminAction.add_group_point, param_len=3,
                         int_param_index=[2]),
                     CMD(u"设活跃度", handle_func=AdminAction.set_group_point, param_len=3,
                         int_param_index=[2]),
                     CMD(u"查清负次数", handle_func=AdminAction.get_clear_chance, param_len=1,
                         int_param_index=[0]),
                     CMD(u"加清负次数", handle_func=AdminAction.add_clear_chance, param_len=2,
                         int_param_index=[1])
                     ]

    def main(self, msg):
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


class Plugin(plugin.QQPlugin):
    """
    此类必须存在
    """
    NAME = u"超级插件"

    def install(self):

        self.qqClient.addGroupMsgEvent(GroupMsgEvent())
        self.qqClient.addFriendMsgEvent(AdminMsgEvent())

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME
