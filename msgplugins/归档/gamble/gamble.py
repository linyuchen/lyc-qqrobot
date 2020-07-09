# -*-coding: UTF8 -*-

import random


class Gamble(object):

    def __init__(self):
        self.currency = ""
        self.gamble_limit_gold = 20

    def get_point(self, group_qq, qq):
        """

        :param group_qq: str
        :param qq: str
        :return: int
        """
        raise NotImplementedError

    def add_point(self, group_qq, qq, point):
        """

        :param group_qq: str
        :param qq: str
        :param point: int
        :return:
        """
        raise NotImplementedError

    def gamble(self, group_qq, member_qq, member_name, gold):

        if gold.isdigit():
            gold = int(gold)
        else:
            return u"命令有误！"

        sender_info_dic = {"group_qq_number": str(group_qq), "qq_number": str(member_qq), "nick": member_name}
        sender_gold = self.get_point(str(group_qq), sender_info_dic["qq_number"])
        if sender_gold < gold:
            return u"哎呀~你的%s不足%d无法赌博！"%(self.currency, gold)

        if gold < self.gamble_limit_gold:

            return u"赌博点数必须要%d以上才能赌博哦"%self.gamble_limit_gold

        if gold > 2000:
            win_probability = 0.57
        else:
            win_probability = 0.5

        if random.random() > win_probability:
            self.add_point(str(group_qq), sender_info_dic["qq_number"], gold)
            return u"恭喜【%s】，赢得了%d %s" % (sender_info_dic["nick"], gold, self.currency)
        else:
            self.add_point(str(group_qq), sender_info_dic["qq_number"], -gold)
            return u"啊哦~【%s】，输掉了%d %s" % (sender_info_dic["nick"], gold, self.currency)
