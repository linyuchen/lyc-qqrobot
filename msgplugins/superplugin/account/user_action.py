# -*- coding: UTF8 -*-

from account.models import MyUser


class UserAction(object):

    def __init__(self, qq):
        self.user = MyUser.get_user(qq)

    def get_point(self):
        result = u"金币: %s" % self.user.point
        return result

