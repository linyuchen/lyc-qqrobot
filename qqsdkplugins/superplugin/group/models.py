# -*- coding:UTF8 -*-
from django.db import models
from account.models import MyUser

# Create your models here.


class GroupGlobalSetting(models.Model):
    sign_add_percentage = models.FloatField(default=0.0001)  # 签到能得到当前活跃度 * sign_add_percentage * 连续签到次数
    sign_least_point = models.IntegerField(default=2000)  # 签到最少能得这么多活跃度
    currency = models.CharField(max_length=20, default=u"活跃度")  # 群积分名字
    talk_point = models.IntegerField(default=1)  # 发言奖励多少积分

    @staticmethod
    def get_setting():
        setting = GroupGlobalSetting.objects.first()
        if not setting:
            setting = GroupGlobalSetting()
            setting.save()

        return setting


class GroupUser(models.Model):
    """
    用户在群里面的信息
    """
    user = models.ForeignKey(MyUser)
    nick = models.CharField(max_length=20)  # 群昵称
    group_qq = models.CharField(max_length=20)  # 群号
    point = models.TextField(default="0")  # 活跃度
    sign_continuous = models.IntegerField(default=1)  # 连续签到次数. 差了一天不签到就断掉,连续签到次数变成1

    def get_point(self):
        return int(self.point)

    def add_point(self, point):
        """
        :param point: int
        :return:
        """
        new_point = self.get_point() + point
        self.point = str(new_point)
        self.save()

    @staticmethod
    def get_user(group_qq, qq):
        u = MyUser.get_user(qq)
        gu, e = GroupUser.objects.get_or_create(user=u, group_qq=group_qq)
        return gu


class SignRecord(models.Model):
    """
    签到记录
    """
    user = models.ForeignKey(GroupUser)
    time = models.DateTimeField(auto_now_add=True)
    add_point = models.TextField()  # 本次签到所加的活跃度


class TransferPointRecord(models.Model):
    """
    转活跃度记录
    """
    user = models.ForeignKey(GroupUser)
    to_user = models.ForeignKey(GroupUser)
    point = models.TextField()
    time = models.DateTimeField(auto_now_add=True)