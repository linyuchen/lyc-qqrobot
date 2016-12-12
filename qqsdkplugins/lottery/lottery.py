# -*-coding: UTF8 -*-

import random


class Lottery:

    def __init__(self):
        self.gamble_limit_gold = 20
        self.currency = u""  # 需要复写

    def lottery(self, group_qq, member_qq, member_name, gold):

        if gold.isdigit():
            gold = int(gold)
        else:
            return u"命令有误！"

        sender_info_dic = {"group_qq_number": str(group_qq), "qq_number": str(member_qq), "nick": member_name}

        point = self.get_point(str(group_qq), sender_info_dic["qq_number"])
        if point < gold:
            return u"【%s】的%s不足 %d 无法抽奖！" % (sender_info_dic["nick"], self.currency, gold)

        award_list = [4, 3, 2, 1, 0, 0, 0, 0, 0, 0]

        result = random.choice(award_list)
        self.add_point(str(group_qq), sender_info_dic["qq_number"], -gold)
        award = result * gold
        if result == 1:
            note = u"哼哼人品有限，不过本喵心情好，给你个安慰奖吧，奖励%d" % award
        elif result != 0:
            note = u"哇塞！得了个%d等奖哦！奖励%d" % (award_list.index(result) + 1, award)
        else:
            note = u"真是倒霉到家了，什么奖都没中！"

        self.add_point(str(group_qq), sender_info_dic["qq_number"], award)

        return u"【%s】消耗%d %s\n" % (sender_info_dic["nick"], gold, self.currency) + note
