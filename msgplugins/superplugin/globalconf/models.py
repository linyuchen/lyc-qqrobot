# -*- coding: UTF8 -*-

from django.db import models

# Create your models here.


class AdminUser(models.Model):
    qq = models.CharField(max_length=20)

    def __unicode__(self):
        return self.qq


class GlobalSetting(models.Model):
    admins = models.ManyToManyField(AdminUser)
    robot_name = models.CharField(max_length=20)
    private_currency_name = models.CharField(max_length=20, default=u"金币")

    @staticmethod
    def get_setting():
        setting = GlobalSetting.objects.first()
        if not setting:
            setting = GlobalSetting(robot_name=u"喵喵咪")
            setting.save()
        return setting

    @staticmethod
    def check_admin(qq):
        if GlobalSetting.get_setting().admins.filter(qq=qq).first():
            return True
        return False


