# -*- coding: UTF8 -*-

import datetime
from globalconf.models import GlobalSetting
from group.models import *


class GroupAction(object):

    group_setting = GroupGlobalSetting.get_setting()
    global_setting = GlobalSetting.get_setting()

    def __init__(self, group_qq, user_qq):
        """

        :param group_qq: int
        :param user_qq: int
        """
        self.group_qq = group_qq
        self.user_qq = user_qq
        self.group_user = GroupUser.get_user(group_qq, user_qq)

    def __get_sign_info(self):

        today = timezone.now()
        last_record = SignRecord.objects.filter(user=self.group_user).\
            exclude(time__year=today.year, time__month=today.month, time__day=today.day).last()
        last_record_time = "无"
        if last_record and last_record.time:
            last_record_time = last_record.time.strftime("%Y-%m-%d")

        info = "上次签到时间: %s" % last_record_time
        info += "\n连续签到%d次\n一共签到%d次" % (self.group_user.sign_continuous, self.group_user.total_sign)
        return info

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
        result = ""
        if exist:
            result += u"今天【%s】已经签到过了！" % self.group_user.nick
        else:
            # reward_point = self.group_setting.sign_add_percentage * self.group_user.get_point() * \
            #                self.group_user.sign_continuous
            reward_point = self.group_setting.sign_least_point + 100 * self.group_user.sign_continuous
            last_record = SignRecord.objects.filter(user=self.group_user).last()
            if last_record and last_record.time:
                if (today - last_record.time) > timezone.timedelta(hours=48):
                    self.group_user.sign_continuous = 1
                else:
                    self.group_user.sign_continuous += 1

            if reward_point < self.group_setting.sign_least_point:
                reward_point = self.group_setting.sign_least_point
            SignRecord(user=self.group_user, add_point=str(reward_point), time=timezone.now()).save()
            if int(self.group_user.point) < 0:
                reward_point += -int(self.group_user.point)
            self.group_user.total_sign += 1
            self.group_user.save()
            self.group_user.add_point(reward_point)
            result = "【%s】签到成功，获得%d %s" % (self.group_user.nick, reward_point, self.group_setting.currency)

        result += "\n%s" % self.__get_sign_info()
        return result

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
        if other_user.user.qq == self.group_user.user.qq:
            return u"自己转给自己闲得慌吗"

        self.group_user.add_point(-point)
        other_user.add_point(point)
        TransferPointRecord(user=self.group_user, to_user=other_user, point=str(point)).save()
        return u"转账成功"

    def get_clear_chance(self):
        return u"【%s】(%s)还有%d次清负机会" % \
               (self.group_user.nick, self.group_user.user.qq, self.group_user.user.clear_point_chance)

    def clear_point(self):
        if self.group_user.user.clear_point_chance <= 0:
            return u"清负次数不足！"
        if self.group_user.get_point() < 0:
            self.group_user.point = "0"
            self.group_user.user.clear_point_chance -= 1
            self.group_user.user.save()
            self.group_user.save()
            return u"清负成功！"
        else:
            return u"无效操作，不需要清负"

    def clear_other_point(self, other_qq):
        if self.group_user.user.clear_point_chance <= 0:
            return u"清负次数不足！"
        other_user = GroupUser.objects.filter(group_qq=self.group_qq, user__qq=other_qq).first()
        if other_user and other_user.get_point() < 0:
            other_user.point = "0"
            other_user.save()
            self.group_user.user.clear_point_chance -= 1
            self.group_user.user.save()
            self.group_user.save()
            return u"清负成功"
        else:
            return u"无效操作，不需要清负"

    def __get_point_rank(self):
        """
        :return: users
        :rtype: list
        """
        users = GroupUser.objects.filter(group_qq=self.group_qq)
        users = list(users)
        users = sorted(users, key=lambda a: -a.get_point())
        return users

    def __get_point_rank_index(self):
        users = self.__get_point_rank()
        return users.index(self.group_user) + 1

    def get_point(self):
        return u"%s (%s)的%s为%d, 当前排名为 %d 位" % \
               (self.group_user.nick, self.group_user.user.qq, self.group_setting.currency,
                self.group_user.get_point(), self.__get_point_rank_index())

    def get_point_rank(self):
        users = self.__get_point_rank()[:10]
        result = ""
        for index, user in enumerate(users):
            result += u"第%d名：%s(%s)，%s\n" % \
                      (index + 1, user.nick, user.user.qq, user.get_point())

        return result

    def group_point2private_point(self, private_point):
        """
        群积分，转到个人积分
        :param private_point: 要转成多少个人积分, int
        :return:
        """
        need_group_point = self.group_setting.group2private_point_percentage * private_point
        if self.group_user.get_point() < need_group_point:
            return u"%s账户额度不够足%d，无法转换" % (self.group_setting.currency, need_group_point)
        self.group_user.add_point(-need_group_point)
        self.group_user.user.add_point(private_point)
        return u"花费%d%s兑换成功!" % (need_group_point, self.group_setting.currency)

    def private_point2group_point(self, private_point):
        """
        个人积分兑换成群积分
        :param private_point: 要转多少个人积分, int
        :return:
        """
        group_point = self.group_setting.private2group_point_percentage * private_point
        if self.group_user.user.get_point() < private_point:
            return u"%s账户额度不足%d，无法转换" % (self.global_setting.private_currency_name, private_point)
        self.group_user.add_point(group_point)
        self.group_user.user.add_point(-private_point)
        return u"兑换%d%s成功!" % (group_point, self.group_setting.currency)


class GroupPointAction(object):

    def __init__(self):
        self.group_setting = GroupGlobalSetting.get_setting()
        self.currency = self.group_setting.currency
        self.robot_name = GlobalSetting.get_setting().robot_name

    def add_point(self, group_qq, qq, point):
        GroupUser.get_user(group_qq, qq).add_point(point)

    def get_point(self, group_qq, qq):
        return GroupUser.get_user(group_qq, qq).get_point()

    def check_user(self, group_qq, qq):
        return GroupUser.objects.filter(group_qq=group_qq, user__qq=qq).first()
