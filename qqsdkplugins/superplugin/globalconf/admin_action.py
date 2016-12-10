# -*- coding: UTF8 -*-

from globalconf.models import *
from group.models import *

global_setting = GlobalSetting.get_setting()


class AdminAction(object):

    @staticmethod
    def check_admin(qq):
        return global_setting.check_admin(qq)

    @staticmethod
    def add_group_point(group_qq, qq, point):
        """

        :param group_qq: str
        :param qq: str
        :param point: int
        :return:
        """
        group_user = GroupUser.get_user(group_qq, qq)
        group_user.add_point(point)
        return "ok"

    @staticmethod
    def set_group_point(group_qq, qq, point):
        """

        :param group_qq: str
        :param qq: str
        :param point: int
        :return:
        """
        group_user = GroupUser.get_user(group_qq, qq)
        group_user.add_point(-group_user.get_point() + point)
        return "ok"

    @staticmethod
    def get_point(qq):
        """

        :param qq: str
        :return: str
        """
        group_users = GroupUser.objects.filter(user__qq=qq)
        result = ""
        for group_user in group_users:
            result += u"群:%s, 点数:%s\n\n" % (group_user.group_qq, group_user.point)

        if not result:
            result = u"无数据"
        return result

