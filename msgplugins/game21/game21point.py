# coding=UTF8

import random
import threading
import time
from .import game21pointbase


class Game(game21pointbase.Game):

    rule = u"""
    每个人拿3张牌，参与游戏时只显示2张牌，当游戏结束时显示全部牌，并计算点数（J, Q, k都作为 10点，A作为1点），点数为所有牌之和，点数少于22点时，最大点数者胜利；点数大于21点时，最小者胜利;相同点数庄家为大 
    """

    def __init__(self):

        super(Game, self).__init__()
        self.qq_group_plugin = None
        self.add_handle_func = None
        self.flower_color_list = [u"黑桃", u"红心", u"梅花", u"方块"]
        self.poker_list = []
        for flower_color in self.flower_color_list:
            self.poker_list += [
                (flower_color, self.convert_poker(str(number), opera_type=1)) for number in range(1, 14)
                ]

        self.send_func = None
        self.currency = ""  # 复写
        self.robot_name = ""  # 复写
        self.game_start = False
        self.limit_second = 15
        self.max_player_num = 9
        self.player_poker_num = 3
        self.player_visible_poker_num = 2
        self.chg_poker_list_pcg = 10  # 换牌需要的分数(1/10)
        self.current_second = 0
        self.master_group_qq_number = ""
        self.master_group_uin = ""
        self.rest_poker_list = self.poker_list[:]

        # {"qq_number": {"nick":string, "gold":integer, "poker_list":[],  "point": integer, "win": bool} ,...} gold是下注金额
        self.player_dic = {}

        # player_dic + {"win_count": count}
        self.master_dic = {}

        self.has_master = False
        self.overing = False
        self.master_poker_list = self.get_random_poker_list()

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

    def reset_game_info(self):

        self.current_second = 0
        self.master_group_qq_number = ""
        self.master_group_uin = ""
        self.rest_poker_list = self.poker_list[:]
        self.player_dic = {}
        self.master_dic = {}
        self.has_master = False
        self.overing = False
        self.master_poker_list = self.get_random_poker_list()

    def get_poker_list_final_str(self, poker_list):

        string = ",".join(["".join(__i) for __i in poker_list[:self.player_visible_poker_num]] +
                          ["***"] * (self.player_poker_num - self.player_visible_poker_num))

        return string

    def update_poker_list(self, group_qq, member_qq, member_name):

        sender_info_dic = {"group_qq_number": group_qq, "qq_number": member_qq, "nick": member_name}
        qq_number = sender_info_dic["qq_number"]
        nick = sender_info_dic["nick"]
        if qq_number not in self.player_dic:
            return u"【%s】请先参与游戏才能换牌" % nick

        gold = self.player_dic[qq_number]["gold"] / self.chg_poker_list_pcg
        group_qq_number = self.player_dic[qq_number]["group_qq_number"]
        pay_result = self.pay_gold(group_qq_number, qq_number, gold)
        if pay_result:
            return pay_result
        poker_list = self.get_random_poker_list()
        self.rest_poker_list += self.player_dic[qq_number]["poker_list"]
        self.player_dic[qq_number]["poker_list"] = poker_list
        self.reset_timer()

        return u"【%s】花费了下注金额的1/%d（%d）换成了新的牌：%s" % \
               (nick, self.chg_poker_list_pcg, gold, self.get_poker_list_final_str(poker_list))

    def pay_gold(self, group_qq_number, qq_number, gold):

        point = self.get_point(str(group_qq_number), qq_number)
        if point < gold:
       
            join_failed_note = u"您的 %s 不足 %s，操作失败！" % (self.currency, gold)
            return join_failed_note
        else:
            self.add_point(str(group_qq_number), qq_number, -gold)

    def start_game(self, group_qq, member_qq, member_name, gold, reply_func):

        sender_info_dic = {"group_qq_number": str(group_qq), "qq_number": str(member_qq), "nick": member_name}
        self.send_func = reply_func
        while self.overing:
            pass

        if len(self.player_dic) > self.max_player_num:
            return u"最多只能%d人参与此游戏，请下局再参与吧" % self.max_player_num

        if gold.isdigit():
            gold = int(gold)
        else:
            return u"命令有误！"
        
        self.reset_timer()

        if sender_info_dic["qq_number"] in self.player_dic:
            join_note = u"【%s】已经参与此游戏了，请不要重复!" % sender_info_dic["nick"]
            return join_note
        else:
            pay_result = self.pay_gold(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"], gold)
            if pay_result:
                return pay_result
            poker_list = self.get_random_poker_list()
            self.player_dic[sender_info_dic["qq_number"]] = sender_info_dic
            self.player_dic[sender_info_dic["qq_number"]].update({"poker_list": poker_list, "gold": gold})

            poker_info = u"【%s】的牌：%s" % (sender_info_dic["nick"], self.get_poker_list_final_str(poker_list))

            join_note = u"21点游戏时间为 %d 秒\n" % self.limit_second + poker_info
            
        if not self.game_start:
            self.start_timer()
        self.game_start = True
        return join_note

    def over_game(self):

        self.overing = True
        self.game_start = False
        master_win_count = 0
        master_poker_list = self.master_poker_list
        master_point = sum([int(self.convert_poker(poker[1], opera_type=2)) for poker in master_poker_list])
        player_sum = len(self.player_dic)

        for qq_number in self.player_dic:
            self.player_dic[qq_number]["point"] = \
                sum([int(self.convert_poker(poker[1], opera_type=2))
                     for poker in self.player_dic[qq_number]["poker_list"]]
                    )
            player_point = self.player_dic[qq_number]["point"]
           
            if self.get_max_point([master_point, player_point]) == master_point:
                master_win_count += 1
                self.player_dic[qq_number]["win_count"] = 0
            else:
                master_win_count -= 1
                self.player_dic[qq_number]["win_count"] = 1

        game_result = u"21点游戏时间到！"
        # master_failed_count = player_sum - 1 - master_win_count
        master_win_gold = 0
        for qq_number in self.player_dic:

            nick = self.player_dic[qq_number]["nick"]
            win_count = self.player_dic[qq_number]["win_count"]
            point = self.player_dic[qq_number]["point"]
            gold = self.player_dic[qq_number]["gold"]
            poker_list = self.player_dic[qq_number]["poker_list"]
            win_point = 0
            win_state = ""
            if 0 == win_count:
                win_state = u" 输掉 %d %s" % (gold, self.currency)
                win_point = -gold
                master_win_gold += gold
            if 1 == win_count:
                win_state = u" 赢得 %d %s" % (gold, self.currency)
                win_point = gold
                master_win_gold -= gold

            self.add_point(self.player_dic[qq_number]["group_qq_number"], qq_number, win_point + gold)
            game_result += u"\n【%s】牌：%s，点数：%d ," % (nick, self.poker_list2str(poker_list), point) + win_state

        master_win_info = u""
        if master_win_count == player_sum - 1:
            master_win_info = u"\n庄家通杀！"
        elif master_win_count < 0:
            master_win_info = u"\n庄家通赔！"

        if master_win_gold < 0:
            master_win_info += u"输掉了 %d %s" % (abs(master_win_gold), self.currency)
        else:
            master_win_info += u"赢得了 %d %s" % (master_win_gold, self.currency)

        game_result += u"\n【%s】(庄家)牌：%s，点数: %d " % \
                       (self.robot_name, self.poker_list2str(master_poker_list), master_point)
        game_result += master_win_info
        self.send_func(game_result)

        self.reset_game_info()
        self.overing = False

    @staticmethod
    def poker_list2str(poker_list):

        return ",".join([",".join(__i) for __i in poker_list])

    def get_random_poker(self):

        poker = random.choice(self.rest_poker_list)
        self.rest_poker_list.remove(poker)

        return poker

    def get_random_poker_list(self):

        poker_list = [self.get_random_poker() for __i in range(self.player_poker_num)]

        return poker_list

    def __timer(self):
        
        while True:
            self.current_second += 1
            if self.current_second > self.limit_second:
                self.over_game()
                break
            time.sleep(1)

    def reset_timer(self):

        self.current_second = 0

    def start_timer(self):

        threading.Thread(target=self.__timer).start()
