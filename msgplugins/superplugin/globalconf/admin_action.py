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
            result += "群:%s, 点数:%s\n\n" % (group_user.group_qq, group_user.point)

        if not result:
            result = "无数据"
        return result

    @staticmethod
    def get_clear_chance(qq):
        user = MyUser.objects.filter(qq=qq).first()
        if not user:
            return "QQ号有误"
        return "%s的清负次数：%d" % (qq, user.clear_point_chance)

    @staticmethod
    def add_clear_chance(qq, num):
        num = int(num)
        user = MyUser.objects.filter(qq=qq).first()
        if not user:
            return "QQ号有误"

        user.clear_point_chance += num
        user.save()
        return "ok"
