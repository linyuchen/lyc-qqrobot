# -*-coding: UTF8 -*-

import sys
import random
import os
cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import grouppluginbase

currency_name_str_g = u"活跃度"


class Rob:

    def __init__(self):
        self.gamble_limit_gold = 20


    def rob(self,group_qq, member_qq, member_name, qq_number):
        u"""
        @param qq_number: 抢劫对象的QQ号
        """

        self.group_plugin = grouppluginbase.GroupPluginBase(group_qq)
        sender_info_dic = {"group_qq_number": group_qq, "qq_number": member_qq, "nick": member_name}
        
        expense = 0.03 
        if qq_number == str(sender_info_dic["qq_number"]):
            return u"没事自己抢自己，吃饱了撑的？"
        point = self.group_plugin._get_point(sender_info_dic["qq_number"])
        if point < 0:
            return u"【%s】的%s不足%d 无法抢劫！"%(sender_info_dic["nick"],currency_name_str_g,0)

        rob_expense_gold = point * expense
        rob_expense_gold = int(rob_expense_gold)

        aim_info = self.group_plugin.sqlite.get_value(self.group_plugin.t_group_point,["point", "name"], {"group_qq": group_qq, "member_qq": qq_number})
        if aim_info == []:
            return u"根本就没这个人存在，你抢什么鬼。。。"
#        print aim_info
        aim_info = aim_info[0]
        if eval(aim_info[0]) < rob_expense_gold:
            return u"对方连你的百分之%d都没有！你还抢？有没有人性。。。"%(expense*100)


        if random.random() < 0.3:
            self.group_plugin._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],num = - rob_expense_gold)
            self.group_plugin._add_point(qq_number,aim_info[1],num = rob_expense_gold)
            return u"糟糕！【%s】遇到了警察！被警察抓到，缴了%d赔偿金给【%s】"%(sender_info_dic["nick"],rob_expense_gold,aim_info[1])
        point = random.randint(int(rob_expense_gold * 0.8),int(rob_expense_gold * 1.2))
        self.group_plugin._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],num = point - rob_expense_gold)
        self.group_plugin._add_point(qq_number,aim_info[1],num = -point)

        return u"【%s】花费%d %s,抢到了【%s】的%d %s"%(sender_info_dic["nick"],rob_expense_gold,currency_name_str_g,aim_info[1],point,currency_name_str_g)
