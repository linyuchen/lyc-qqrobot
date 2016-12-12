# -*- coding: UTF-8 -*-

from django.db import models
from account.models import MyUser

# Create your models here.


class RpgGlobalSetting(models.Model):

    level_up_price = models.IntegerField(default=2)  # 升级加的价值
    level_up_experience = models.IntegerField(default=20)  # 升级所需经验
    level_up_price_experience = models.IntegerField(default=3)  # 升级加所值经验值
    level_up_attack = models.IntegerField(default=3)  # 每级加的攻击力
    level_up_defensive = models.IntegerField(default=3)  # 每级加的防御力
    level_up_health = models.IntegerField(default=3)  # 每级加的防御力


class RpgThingBase(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField(default=1, null=True, blank=True)  # 当前等级
    price = models.IntegerField(default=1, null=True, blank=True)  # 所值金钱
    price_experience = models.IntegerField(default=1, null=True, blank=True)  # 所值经验值
    min_attack = models.IntegerField(default=1, null=True, blank=True)  # 最小攻击力
    max_attack = models.IntegerField(default=3, null=True, blank=True)  # 最小攻击力
    defensive = models.IntegerField(default=1, null=True, blank=True)  # 防御力
    health = models.IntegerField(default=10, null=True, blank=True)  # 生命值

    class Meta:
        abstract = True


class RpgKill(RpgThingBase):
    say = models.TextField()  # 使用技能时


class RpgGoods(RpgThingBase):
    date_max_use = models.IntegerField(default=1)  # 每日最多使用次数


class RpgGoodsUseRecord(models.Model):
    """
    带有主动技能的物品, 使用记录
    """
    goods = models.ForeignKey(RpgGoods)
    time = models.DateTimeField(auto_now_add=True)


class RpgPerson(RpgThingBase):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    experience = models.IntegerField(default=0)  # 当前拥有的经验值
    health = models.IntegerField(default=10)  # 生命值
    goods_use_records = models.ManyToManyField(RpgGoodsUseRecord, blank=True)
