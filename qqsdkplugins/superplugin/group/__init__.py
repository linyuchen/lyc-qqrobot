# -*- coding: UTF8 -*-
from django.utils import timezone

from group.models import *


class GroupAction(object):

    def __init__(self, group_qq, user_qq):
        """

        :param group_qq: int
        :param user_qq: int
        """
        self.group_qq = group_qq
        self.user_qq = user_qq
        self.group_user = GroupUser.get_user(group_qq, user_qq)
        self.group_setting = GroupGlobalSetting.get_setting()

    def sign(self):
        """
        签到
        :param qq:
        :param group_qq:
        :return:
        """
        today = timezone.now()
        exist = SignRecord.objects.filter(time__year=today.year, time__month=today.month, time__day=today.day,
                                          user=self.group_user).first()
        if exist:
            return u"今天【%s】已经签到过了，请不要重复签到！" % self.group_user.nick
        else:
            reward_point = self.group_setting.sign_add_percentage * self.group_user.get_point() * \
                           self.group_user.sign_continuous
            last_record = SignRecord.objects.filter(user=self.group_user).last()
            last_record_time = u"无"
            if last_record:
                last_record_time = timezone.make_naive(last_record.time).strftime("%Y-%m-%d")
                if (today - last_record.time) > timezone.timedelta(hours=24):
                    self.group_user.sign_continuous = 1
                    self.group_user.save()

            if reward_point < self.group_setting.sign_least_point:
                reward_point = self.group_setting.sign_least_point
            SignRecord(user=self.group_user, add_point=str(reward_point)).save()
            all_record_count = SignRecord.objects.filter(user=self.group_user).count()

            self.group_user.add_point(reward_point)
            return u"【%s】签到成功，获得%d %s\n上次签到时间：%s\n已经连续签到 %d 天\n总签到了 %d 天" % \
                   (self.group_user.nick, reward_point, self.group_setting.currency, last_record_time,
                    self.group_user.sign_continuous, all_record_count)

    def transfer_point(self, qq, point):
        """

        :param qq: to_user qq
        :param point: int
        :return:
        """
        other_user = GroupUser.objects.filter(group_qq=self.group_qq, user__qq=qq).first()
        if not other_user:
            return u"对不起，您要转账的对象不存在！"

        if point > self.group_user.get_point():
            return u"对不起，您的余额不够要转的额度！"

        self.group_user.add_point(-point)
        other_user.add_point(point)
        TransferPointRecord(user=self.group_user, to_user=other_user, point=str(point)).save()
        return u"转账成功"

    def get_clear_chance(self):
        return u"【%s】(%s)还有%d次清负机会" % \
               (self.group_user.nick, self.group_user.user.qq, self.group_user.user.clear_point_chance)

    def __get_point_rank(self):
        """
        :return: users
        :rtype: list
        """
        users = GroupUser.objects.filter(group_qq=self.group_qq)
        users = list(users)
        users = sorted(users, lambda a, b: cmp(a.get_point(), b.get_point()))
        return users

    def __get_point_rank_index(self):
        users = self.__get_point_rank()
        return users.index(self.group_user)

    def get_point(self):
        return u"%s (%s)的%s为%d, 当前排名为 %d 位" % \
               (self.group_user.nick, self.group_user.user.qq, self.group_setting.currency,
                self.group_user.get_point(), self.__get_point_rank_index())

    def get_point_rank(self):
        users = self.__get_point_rank()
        result = ""
        for index, user in enumerate(users):
            result += u"第%d名：%s(%s)，%s\n" % \
                      (index, user.nick, user.user.qq, user.get_point())

        return result

