# -*- coding:UTF8 -*-
from django.db import models
from django.utils import timezone
from account.models import MyUser

# Create your models here.


class GroupGlobalSetting(models.Model):
    sign_add_percentage = models.FloatField(default=0.0001)  # 签到能得到当前活跃度 * sign_add_percentage * 连续签到次数
    sign_least_point = models.IntegerField(default=2000)  # 签到最少能得这么多活跃度
    currency = models.CharField(max_length=20, default=u"活跃度")  # 群积分名字
    talk_point = models.IntegerField(default=1)  # 发言奖励多少积分
    group2private_point_percentage = models.IntegerField(default=10)  # 群积分转个人积分比，100的话就是100个群积分转1个个人积分
    private2group_point_percentage = models.IntegerField(default=9)  # 个人积分转群积分比，100的话就是1个个人积分转成100个群积分

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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    nick = models.CharField(max_length=20)  # 群昵称
    group_qq = models.CharField(max_length=20)  # 群号
    point = models.TextField(default="0")  # 活跃度
    sign_continuous = models.IntegerField(default=1)  # 连续签到次数. 差了一天不签到就断掉,连续签到次数变成1
    total_sign = models.IntegerField(default=0)  # 总共签到了多少次

    def get_point(self):
        return int("%d" % eval(self.point))

    def add_point(self, point):
        """
        :param point: int
        :return:
        """
        new_point = self.get_point() + point
        self.point = "%d" % new_point
        self.save()

    @staticmethod
    def get_user(group_qq, qq) -> "GroupUser":
        u = MyUser.get_user(qq)
        gu, e = GroupUser.objects.get_or_create(user=u, group_qq=group_qq)
        return gu

    def __unicode__(self):
        return u"群：%s, %s(%s)" % (self.group_qq, self.nick, self.user.qq)


class SignRecord(models.Model):
    """
    签到记录
    """
    user = models.ForeignKey(GroupUser, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    add_point = models.TextField()  # 本次签到所加的活跃度

    def __unicode__(self):
        return u"%s %s" % (self.user, timezone.make_naive(self.time).strftime("%Y-%m-%d"))


class TransferPointRecord(models.Model):
    """
    转活跃度记录
    """
    user = models.ForeignKey(GroupUser, on_delete=models.CASCADE)
    to_user = models.ForeignKey(GroupUser, related_name="transfer_point_record", on_delete=models.CASCADE)
    point = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
