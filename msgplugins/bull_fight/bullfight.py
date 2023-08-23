# -*- coding: UTF-8 -*-

import threading
import time

from msgplugins.bull_fight import bullfight_base


class BullFight(bullfight_base.BullFightBase):

    def __init__(self, group_qq, qq_client):
        """
        :param group_qq: 群号，str
        """

        self.mutex = threading.RLock()
        super(BullFight, self).__init__()

        self.qq_client = qq_client
        self.group_qq = group_qq
        self.currency = ""
        self.robot_name = ""
        self.add_handle_func = None
        self.game_start = False
        self.max_player_count = 9
        self.limit_second = 15
        self.join_game_note = u"%d秒之后开牌" % self.limit_second
        self.rule = u"""
        """
        self.send_func = None
        self.current_second = 0
        self.master_info_dic = {}
        self.players_info_list = []  # item is dict
        self.running = False
        self.overing = False
        self.player_max_gold = 0  # 闲家最大下注
        self.min_gold = 0  # 群内最小下注
        self.master_deposit_gold = 0  # 庄家押金
        self.player_total_gold = 0  # 闲家所有下注金额
        self.max_multiple = 1

    def reset_game_info(self):

        with self.mutex:
            super(BullFight, self).reset_game_info()
            self.current_second = 0
            self.master_info_dic = {}
            self.players_info_list = []  # item is dict
            self.running = False
            self.overing = False
            self.player_max_gold = 0  # 闲家最大下注
            self.min_gold = 0  # 群内最小下注
            self.master_deposit_gold = 0  # 庄家押金
            self.player_total_gold = 0  # 闲家所有下注金额
            self.max_multiple = 1

    def add_point(self, group_qq, qq, point):
        """

        :param group_qq: str
        :param qq: str
        :param point: int
        :return:
        """
        raise NotImplementedError

    def get_point(self, group_qq, qq):
        """

        :param group_qq: str
        :param qq: str
        :return: int
        """
        raise NotImplementedError

    def deposit_master_gold(self, num):

        self.master_deposit_gold += num
        self.add_point(self.group_qq, str(self.master_info_dic["qq_number"]), -num)

    def return_master_deposit(self):

        self.deposit_master_gold(-self.master_deposit_gold)

    def get_master_gold(self):

        master_gold = self.get_point(self.group_qq, str(self.master_info_dic["qq_number"]))
        return master_gold

    def start_game(self, member_qq, member_name, __send_func, gold="0"):
        """
        游戏入口函数
        :param member_qq:
        :param member_name:
        :param __send_func: 发送消息函数, 函数只有一个参数
        :param gold: 下注金额， str
        :return:
        """

        with self.mutex:
            if self.overing:
                for i in range(10):
                    time.sleep(1)
                self.overing = False

        group_qq = self.group_qq
        __sender_info_dic = {"group_qq_number": group_qq, "qq_number": str(member_qq), "nick": member_name,
                             "send_func": __send_func}

        self.send_func = __sender_info_dic["send_func"]
        if len(self.players_info_list) >= self.max_player_count:
            return u"参与人数最多%d人，请下局再参与" % self.max_player_count
        if not (gold.isdigit()):
            error = u"【%s】的命令有误" % __sender_info_dic["nick"]
            return error
        else:
            gold = int(gold)
            player_gold = self.get_point(self.group_qq, __sender_info_dic["qq_number"])
            if player_gold < gold:
                error = u"【%s】的%s不足%d，无法参与此游戏" % (__sender_info_dic["nick"], self.currency, gold)
                return error
            elif player_gold / self.max_multiple < gold:
                return u"【%s】的下注超过了自身%s总数的1/%d，无法下注！" % \
                    (__sender_info_dic["nick"], self.currency, self.max_multiple)

        with self.mutex:
            if not self.running:
                self.running = True
            threading.Thread(target=self.timer).start()
        self.current_second = 0
        # 庄家参与
        if gold == 0:
            if self.master_info_dic:
                return u"已经有庄家了，庄家是【%s】,请下注!" % (self.master_info_dic["nick"])
            elif [player for player in self.players_info_list if player["qq_number"] == __sender_info_dic["qq_number"]]:
                return u"【%s】已经参与了，请不要重复参与游戏" % (__sender_info_dic["nick"])
            elif self.players_info_list:
                return u"已经有闲家参与了，不能坐庄!"

            self.max_multiple = 8
            master_gold = self.get_point(self.group_qq, __sender_info_dic["qq_number"])
            if self.players_info_list:
                if master_gold < self.player_total_gold * self.max_multiple:
                    error = u"【%s】的%s不足当前所有闲家下注总和的%d倍, 无法坐庄！" % \
                            (__sender_info_dic["nick"], self.currency, self.max_multiple)
                    return error

            self.master_info_dic = __sender_info_dic
            self.master_info_dic["poker_list"] = [self.get_random_poker() for i in range(5)]
            self.master_info_dic["poker_type"] = self.get_poker_type(self.master_info_dic["poker_list"])
            self.master_info_dic["max_gold"] = self.get_point(self.group_qq, str(__sender_info_dic["qq_number"]))
            self.deposit_master_gold(self.player_total_gold * self.max_multiple)

            return u"【%s】参与斗牛游戏，当前庄家【%s】\n%s" % \
                (__sender_info_dic["nick"], __sender_info_dic["nick"], self.join_game_note)
        # 闲家参与
        if not [player for player in self.players_info_list if player["qq_number"] == __sender_info_dic["qq_number"]] \
                and not (self.master_info_dic and self.master_info_dic["qq_number"] == __sender_info_dic["qq_number"]):

            if self.master_info_dic:
                master_gold = self.get_master_gold()
                if gold > master_gold / self.max_multiple:
                    error = u"庄家剩余的%s只有%d，下注不能超过这个数的1/%d哦，不然庄家会欠一屁股债滴！" % \
                            (self.currency, master_gold, self.max_multiple)
                    return error
                else:
                    self.deposit_master_gold(gold * self.max_multiple)

            player_info_dic = __sender_info_dic
            player_info_dic["poker_list"] = [self.get_random_poker() for i in range(5)]
            player_info_dic["poker_type"] = self.get_poker_type(player_info_dic["poker_list"])
            player_info_dic["gold"] = gold
            self.add_point(self.group_qq, str(player_info_dic["qq_number"]), -gold)
            self.player_total_gold += gold
            if gold > self.player_max_gold:
                self.player_max_gold = gold
            self.players_info_list.append(player_info_dic)
            poker_list_str = ["".join(i) for i in player_info_dic["poker_list"]]
            poker_list_str = ",".join(poker_list_str[:3])
            return u"【%s】参与斗牛游戏，前三张牌为：%s，当前闲家:\n%s\n%s" % \
                (__sender_info_dic["nick"], poker_list_str,
                 "\n".join([player["nick"] for player in self.players_info_list]), self.join_game_note)
        else:
            return u"【%s】已经参与了，请不要重复参与游戏" % (__sender_info_dic["nick"])

    def get_system_mater_info_dic(self):

        self.master_info_dic["qq_number"] = "admin"
        self.master_info_dic["nick"] = self.robot_name
        self.master_info_dic["poker_list"] = [self.get_random_poker() for i in range(5)]
        self.master_info_dic["poker_type"] = self.get_poker_type(self.master_info_dic["poker_list"])

    def over_game(self):

        with self.mutex:
            self.overing = True
            self.running = False
        if not self.master_info_dic:
            self.get_system_mater_info_dic()

        if not self.players_info_list:
            self.send_func(u"开牌时间到，无闲家参与斗牛游戏，此局作废\n")
            self.reset_game_info()
            return

            # master_poker_list = self.master_info_dic["poker_list"]
        result = u"庄家【%s】：%s\n" % (self.master_info_dic["nick"], self.get_poker_list_info(self.master_info_dic))
        master_multiple = self.master_info_dic["poker_type"]["multiple"]
        master_win_gold = 0
        master_win_count = 0
        for player_info_dic in self.players_info_list:

            player_multiple = player_info_dic["poker_type"]["multiple"]
            player_gold = player_info_dic["gold"]
            # player_win_gold = 0
            player_poker_list = player_info_dic["poker_list"]
            player_poker_string = self.get_poker_list_info(player_info_dic)
            if self.compare_poker_list(self.master_info_dic["poker_list"], player_poker_list):
                result += u"【%s】：%s，输掉了%d x %d %s\n" % \
                          (player_info_dic["nick"], player_poker_string, master_multiple, player_gold,
                           self.currency)
                player_win_gold = -(master_multiple * player_gold)
                master_win_count += 1
            else:
                result += u"【%s】：%s，赢得了%d x %d %s\n" % \
                          (player_info_dic["nick"], player_poker_string, player_multiple, player_gold,
                           self.currency)
                player_win_gold = player_multiple * player_gold

            master_win_gold -= player_win_gold
            self.add_point(self.group_qq, player_info_dic["qq_number"], player_win_gold + player_gold)

        if master_win_count == len(self.players_info_list):
            result += u"庄家通杀！\n"
        elif master_win_count == 0:
            result += u"庄家通赔！\n"
        if master_win_gold > 0:
            master_win_state = u"赢得了"
        else:
            master_win_state = u"输掉了"
        result += u"庄家%s %d %s\n" % \
                  (master_win_state, abs(master_win_gold), self.currency)
        if self.master_info_dic["qq_number"] != "admin":
            self.add_point(self.group_qq, self.master_info_dic["qq_number"], master_win_gold + self.master_deposit_gold)

        self.send_func(result)
        self.reset_game_info()

    @staticmethod
    def get_poker_list_info(player_info_dic):

        poker_list = player_info_dic["poker_list"]
        poker_string = ",".join(["%s%s" % (poker[0], poker[1]) for poker in poker_list])
        result = u"牌：%s，牌型：" % poker_string
        poker_type = player_info_dic["poker_type"]["type"]
        max_poker = player_info_dic["poker_type"]["max_poker"]

        if poker_type == 0:
            result += u"无牛,最大牌:" + max_poker[0] + max_poker[1]
        elif poker_type == 1:
            bull_point = player_info_dic["poker_type"]["point"]
            result += u"牛%d" % bull_point
        elif poker_type == 2:
            result += u"四炸"
        elif poker_type == 3:
            result += u"五花牛"
        elif poker_type == 4:
            result += u"五小牛"

        return result

    def timer(self):

        while self.running:
            self.current_second += 1
            if self.current_second > self.limit_second:
                self.over_game()
                break
            time.sleep(1)


if "__main__" == __name__:
    class Test(BullFight):

        def __init__(self, group_qq):
            super(Test, self).__init__(group_qq)

        def add_point(self, group_qq, qq, point):
            pass

        def get_point(self, group_qq, qq):
            return 123


    test = Test("1234")
    old_time = time.time()


    def send_func(text):
        print(text)


    print(test.start_game("123", "123", send_func, "1"))
