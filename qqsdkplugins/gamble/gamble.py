# -*-coding: UTF8 -*-

import sys
import random
import os
cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import grouppluginbase

currency_name_str_g = u"活跃度"


class Gamble:

    def __init__(self):
        self.gamble_limit_gold = 20


    def gamble(self, group_qq, member_qq, member_name, gold):

        if gold.isdigit():
            gold = int(gold)
        else:
            return u"命令有误！"

        self.group_plugin = grouppluginbase.GroupPluginBase(group_qq)

        sender_info_dic = {"group_qq_number": group_qq, "qq_number": member_qq, "nick": member_name}
        sender_gold = self.group_plugin._get_point(sender_info_dic["qq_number"])
        if sender_gold < gold:
            return u"哎呀~你的%s不足%d无法赌博！"%(currency_name_str_g,gold)

        if gold < self.gamble_limit_gold:

            return u"赌博点数必须要%d以上才能赌博哦"%self.gamble_limit_gold

        if gold > 2000:
            win_probability = 0.57
        else:
            win_probability = 0.5

        if random.random() > win_probability:
            self.group_plugin._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],gold)
            return u"恭喜【%s】，赢得了%d %s"%(sender_info_dic["nick"], gold, currency_name_str_g)
        else:
            self.group_plugin._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],-gold)
            return u"啊哦~【%s】，输掉了%d %s"%(sender_info_dic["nick"], gold, currency_name_str_g)
