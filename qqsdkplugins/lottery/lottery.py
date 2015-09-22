# -*-coding: UTF8 -*-

import sys
import random
import os
cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import grouppluginbase

currency_name_str_g = u"活跃度"


class Lottery:

    def __init__(self):
        self.gamble_limit_gold = 20


    def lottery(self, group_qq, member_qq, member_name, gold):

        if gold.isdigit():
            gold = int(gold)
        else:
            return u"命令有误！"

        self.group_plugin = grouppluginbase.GroupPluginBase(group_qq)

        sender_info_dic = {"group_qq_number": group_qq, "qq_number": member_qq, "nick": member_name}

        point = self.group_plugin._get_point(sender_info_dic["qq_number"])
        if point < gold:
            return u"【%s】的%s不足 %d 无法抽奖！"%(sender_info_dic["nick"],currency_name_str_g,gold)

        award_list = [4,3,2,1,0,0,0,0,0,0]

        result = random.choice(award_list)
        self.group_plugin._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],num=-gold)
        award = result * gold
        if result == 1:
            note = u"哼哼人品有限，不过本喵心情好，给你个安慰奖吧，奖励%d"%(award)
        elif result != 0:
            note = u"哇塞！得了个%d等奖哦！奖励%d"%(award_list.index(result) + 1,award)
        else:
            note = u"真是倒霉到家了，什么奖都没中！"

        self.group_plugin._add_point(sender_info_dic["qq_number"], sender_info_dic["nick"],num=award)

        return u"【%s】消耗%d %s\n"%(sender_info_dic["nick"],gold,currency_name_str_g) + note
