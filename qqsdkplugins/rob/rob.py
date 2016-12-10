# -*-coding: UTF8 -*-

import random


class Rob(object):

    def __init__(self):
        self.gamble_limit_gold = 20
        self.currency = u""

    def rob(self, group_qq, member_qq, member_name, qq_number):
        """

        :param group_qq:
        :param member_qq:
        :param member_name:
        :param qq_number: 被抢劫的人
        :return:
        """

        sender_info_dic = {"group_qq_number": str(group_qq), "qq_number": member_qq, "nick": member_name}
        
        expense = 0.03 
        if qq_number == str(sender_info_dic["qq_number"]):
            return u"没事自己抢自己，吃饱了撑的？"
        point = self.get_point(str(group_qq), sender_info_dic["qq_number"])
        if point < 0:
            return u"【%s】的%s不足%d 无法抢劫！" % (sender_info_dic["nick"], self.currency, 0)

        rob_expense_gold = point * expense
        rob_expense_gold = int(rob_expense_gold)

        aim_info = self.check_user(str(group_qq), str(qq_number))
        if not aim_info:
            return u"根本就没这个人存在，你抢什么鬼。。。"
        if aim_info.get_point() < rob_expense_gold:
            return u"对方连你的百分之%d都没有！你还抢？有没有人性。。。" % (expense * 100)

        if random.random() < 0.3:
            self.add_point(str(group_qq), sender_info_dic["qq_number"], -rob_expense_gold)
            self.add_point(str(group_qq), str(qq_number), rob_expense_gold)
            return u"糟糕！【%s】遇到了警察！被警察抓到，缴了%d赔偿金给【%s】" % \
                   (sender_info_dic["nick"], rob_expense_gold, aim_info.nick)
        point = random.randint(int(rob_expense_gold * 0.8), int(rob_expense_gold * 1.2))
        self.add_point(str(group_qq), sender_info_dic["qq_number"], point - rob_expense_gold)
        self.add_point(str(group_qq), qq_number, -point)

        return u"【%s】花费%d,抢到了【%s】的%d %s" % \
               (sender_info_dic["nick"], rob_expense_gold, aim_info.nick, point, self.currency)
