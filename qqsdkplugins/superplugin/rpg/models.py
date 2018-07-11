# -*- coding: UTF-8 -*-

from django.db import models
from django.utils import timezone
from account.models import MyUser

# Create your models here.


class RpgGlobalSetting(models.Model):

    level_up_price = models.IntegerField(default=2)  # 升级加的价值
    level_up_experience = models.IntegerField(default=20)  # 升级所需经验
    level_up_price_experience = models.IntegerField(default=3)  # 升级加所值经验值
    level_up_attack = models.IntegerField(default=3)  # 每级加的攻击力
    level_up_defensive = models.IntegerField(default=3)  # 每级加的防御力
    level_up_health = models.IntegerField(default=3)  # 每级加的防御力
    leveling_today_count = models.IntegerField(default=10)  # 每天练级的次数

    @staticmethod
    def get_setting():
        setting = RpgGlobalSetting.objects.first()
        if not setting:
            setting = RpgGlobalSetting()
            setting.save()

        return setting


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


class RpgSay(models.Model):

    TYPE_SKILL = "skill"
    TYPE_ATTACK = "attack"
    TYPE_LIVE = "live"
    TYPE_DRAW = "draw"

    say = models.TextField()  # 台词
    type = models.CharField(max_length=20)


class RpgSkill(RpgThingBase):
    say = models.ManyToManyField(RpgSay)  # 使用技能时的台词
    date_max_use = models.IntegerField(default=1)  # 每日最多使用次数


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
    goods_use_records = models.ManyToManyField(RpgGoodsUseRecord, blank=True)
    says = models.ManyToManyField(RpgSay, blank=True)  # 动作台词

    @staticmethod
    def get_person(qq):
        user = MyUser.get_user(qq)
        person, e = RpgPerson.objects.get_or_create(user=user)
        return person

    def get_say(self, type_str):
        says = self.says.filter(type=type_str)
        if says.count() > 0:
            return says.order_by('?')[0].say
        return ""

    def add_experience(self, experience):
        result = u""
        self.experience += experience
        setting = RpgGlobalSetting.get_setting()
        if self.experience >= self.level * setting.level_up_experience:
            result = u"level up! 【%s】升级了!" % self.user.nick
            self.level += 1
            self.experience = 0
            self.price += setting.level_up_price
            self.price_experience += setting.level_up_price_experience
            self.min_attack += int(setting.level_up_attack / 2)
            self.max_attack += setting.level_up_attack
            self.health += setting.level_up_health
            self.defensive += setting.level_up_defensive
            self.save()

        return result

    def today_count(self, today=None):
        if not today:
            today = timezone.now()
        return LevelingRecord.objects.filter(time__day=today.day, time__year=today.year, time__month=today.month,
                                             person=self).count()


class LevelingRecord(models.Model):  # 练级记录
    time = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(RpgPerson)
    add_experience = models.IntegerField()  # 练级所加的经验
