# -*- coding: UTF8 -*-

import random
from rpg.models import *


class RpgMoveAction(object):

    def __init__(self, qq):
        self.person = RpgPerson.get_person(qq)
        self.setting = RpgGlobalSetting.get_setting()

    def max_step(self, step):
        if not step or abs(step) > self.setting.level_map_step:
            step = self.person.level * self.setting.level_map_step
        return step

    @staticmethod
    def get_max_xy(xy, start_xy, end_xy):
        if xy > end_xy:
            xy = end_xy
        elif xy < start_xy:
            xy = start_xy

        return xy

    def move(self, x, y):
        # x = self.max_step(x)
        # y = self.max_step(y)
        result_x = self.person.position_x + x
        result_y = self.person.position_y + y

        result_x = self.get_max_xy(result_x, self.setting.map_x_start, self.setting.map_x_end)
        result_y = self.get_max_xy(result_y, self.setting.map_y_start, self.setting.map_y_end)
        self.person.position_x = result_x
        self.person.position_y = result_y
        self.person.save()

    def move_up(self, step=0):
        self.move(0, self.max_step(step))
        return self.get_current_pos_info()

    def move_down(self, step=0):
        self.move(0, -self.max_step(step))
        return self.get_current_pos_info()

    def move_left(self, step=0):
        self.move(-self.max_step(step), 0)
        return self.get_current_pos_info()

    def move_right(self, step=0):
        self.move(self.max_step(step), 0)
        return self.get_current_pos_info()

    def __get_current_map(self):
        maps = RpgMap.objects.filter(x_start__lte=self.person.position_x, x_end__gte=self.person.position_x,
                                     y_start__lte=self.person.position_y, y_end__gte=self.person.position_y)

        # tmp = RpgMap.objects.filter( x_start__gte=self.person.position_x)
        # x_start最大，x_end最小，y_start最大， y_end最小
        maps = [maps.order_by("-x_start").first(), maps.order_by("x_end").first(),
                maps.order_by("-y_start").first(), maps.order_by("y_end").first()]

        maps = set(maps)
        maps = list(maps)
        if len(maps) > 0:
            return maps[0]

    def get_current_pos_info(self):
        """
        当前位置
        :return:
        """
        result = u"【%s】的当前坐标 X: %d Y: %d" % (self.person.user.nick, self.person.position_x, self.person.position_y)
        current_map = self.__get_current_map()
        if current_map:
            map_info = u"\n位于: %s" % current_map.name
        else:
            map_info = u"\n位于：荒郊野岭"
        result += map_info
        return result


class RpgAction(object):

    def __init__(self, qq):
        self.person = RpgPerson.get_person(qq)

    @staticmethod
    def __attack_health(person, aim_person):
        """

        :param person:
        :param aim_person:
        :return: attack, 实际掉血
        """
        attack = random.randint(person.min_attack, person.max_attack)
        attack -= aim_person.pesensive
        attack = 0 if attack <= 0 else attack
        return attack

    def attack(self, qq):
        aim_person = RpgPerson.get_person(qq)
        return self.__attack_person(aim_person)

    def __attack_person(self, aim_person):

        result = u""
        attack_say = self.person.get_say(RpgSay.TYPE_ATTACK)

        if attack_say:
            result += "【%s】: %s\n" % (self.person.user.nick, attack_say)
        a_health = self.person.health
        b_health = aim_person.health
        while True:

            b_health -= self.__attack_health(self.person, aim_person)
            a_health -= self.__attack_health(aim_person, self.person)

            if a_health <= 0 or b_health <= 0:
                break

            if a_health == self.person.health and b_health == aim_person.health:
                a_health = b_health = 0
                break

        live_person = None
        failed_person = None
        if a_health > b_health:
            live_person = self.person
            failed_person = aim_person
        elif b_health < a_health:
            live_person = aim_person
            failed_person = self.person

        if not live_person:
            result += u"真是旗鼓相当的对手, 居然平局了！\n"
            result += u"【%s】: %s\n" % (self.person.user.nick, self.person.get_say(RpgSay.TYPE_DRAW))
            result += u"【%s】: %s\n" % (aim_person.user.nick, aim_person.get_say(RpgSay.TYPE_DRAW))
        else:
            result += u"胜者:【%s】\n" % live_person.user.nick
            result += (live_person.get_say(RpgSay.TYPE_LIVE) + "\n")
            result += u"获得%d点经验\n" % failed_person.price_experience
            add_experience_result = live_person.add_experience(failed_person.price_experience)
            if add_experience_result:
                result += (add_experience_result + "\n")

        return result
