# -*- coding: UTF8 -*-

import random
from rpg.models import *


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
