# -*- coding:UTF-8 -*-
"""
处理数据库的一些变动
"""
import django_setup
import os
django_setup.sys.path.append(os.path.dirname(django_setup.CURRENT_PATH))
from group.models import GroupUser
from globalconf.admin_action import AdminAction


def migrate_sign():
    """
    把所有人的连续签到天数变成签到总天数
    :return:
    """
    users = GroupUser.objects.all()
    for user in users:
        user.sign_continuous = user.total_sign
        user.save()


def add_point():
    group_qq = "30115908"
    add_num = int("6" * 74)
    users = GroupUser.objects.filter(group_qq=group_qq)
    for user in users:
        if user.get_point() < 0:
            AdminAction.set_group_point(group_qq, user.user.qq, add_num)
        else:
            user.add_point(add_num)

if __name__ == "__main__":
    # migrate_sign()

    add_point()
