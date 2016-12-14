# -*- coding:UTF8 -*-

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, name, password=None):

        user = self.model(
          qq=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, qq, password=None):

        user = self.create_user(qq, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    """
    nick = models.CharField(max_length=100, null=True)  # QQ昵称
    is_admin = models.BooleanField(default=False)
    qq = models.CharField(max_length=15, unique=True)  # QQ号
    point = models.TextField(default="0")  # 个人积分，和群无关
    clear_point_chance = models.IntegerField(default=0)  # 清负活跃度机会
    objects = UserManager()
    USERNAME_FIELD = "qq"

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
    def get_user(qq):
        u, e = MyUser.objects.get_or_create(qq=qq)
        return u

    def get_full_name(self):
        return self.nick

    def get_short_name(self):
        return self.nick

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, per, obj=None):
        return True

    def has_module_perms(self, applabel):
        return True

    def __unicode__(self):
        if self.nick:
            return self.nick
        elif self.qq:
            return self.qq
        else:
            return u"匿名"
