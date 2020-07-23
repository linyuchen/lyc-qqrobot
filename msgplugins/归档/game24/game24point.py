# coding=UTF-8

import time
import threading

import game24point_base


class Game(game24point_base.Game24PointBase):
    rule = u"24点游戏是一种考验你四则运算的游戏\n系统给出四个数字，运转你的大脑，" \
           u"把这四个数字用加减乘除把它算成结果24\n如题目 3,8,2,1 " \
           u"那么式子3*8*(2-1)就是正确的\n注:加减乘除对应 + - * /,支持括号"

    def __init__(self):

        super(Game, self).__init__()
        self.group_plugin = None
        self.win_gold = 30
        self.second_limit = 120  # 限时 秒
        self.today_game_count = 100
        self.win_persentage = 1.0 / (1000000 * 1000000 * 100000000)  # 答对题目奖励自身活跃度的百分比
        self.send_func = None
        self.current_second = 0
        self.now_num_list = []
        self.has_winner = False
        self.running = False
        self.currency = u""  # 货币名称，需要复写

    def reset_info(self):

        self.send_func = None
        self.current_second = 0
        self.now_num_list = []
        self.has_winner = False
        self.running = False

    def start_game(self, send_func):

        if self.running:
            return u"24点游戏已经开始了,请勿重复！\n"
        else:
            self.running = True
            threading.Thread(target=self.timer).start()

        self.send_func = send_func
        super(Game, self).start_game()
        return u"当前题目：%s\n游戏时间为%d秒\n" % (u",".join([str(i) for i in self.now_num_list]), self.second_limit)

    def judge(self, group_qq, member_qq, member_name, arithmetic_string):

        if not self.now_num_list:
            return u"24点游戏还未开始,请先发起"

        result = ""
        __sender_info_dic = {"group_qq_number": str(group_qq), "qq_number": str(member_qq), "nick": member_name}

        retcode = super(Game, self).judge(arithmetic_string,self.now_num_list)

        cur_point = self.get_point(str(group_qq), __sender_info_dic["qq_number"])
        if cur_point < 0:
            return u"啊哦~ 【%s】的%s已经用光光了，没办法参加游戏╮(╯﹏╰）╭" % (__sender_info_dic["nick"], self.currency)
        percentage = self.win_persentage
        win_point = int(percentage * cur_point)
        if win_point < 100:
            win_point = 100

        failed_note = u"扣掉%d %s" % (win_point, self.currency)

        if -1 == retcode:

            result = u"【%s】的答案错误，%s，你这家伙没看题目吗？好好看清楚题目再来回答吧\n" % \
                     (__sender_info_dic["nick"], failed_note)

        elif 1 == retcode:

            result = u"【%s】的答案不正确哦，%s， 重新再算一次吧\n" % (__sender_info_dic["nick"], failed_note)

        elif 2 == retcode:

            result = u"【%s】的命令有误，%s，去看看规则再来回答吧\n" % (__sender_info_dic["nick"], failed_note)

        if retcode == 0:
            
            self.has_winner = True
            self.over_game()
            result = u"bingo！恭喜【%s】答对本题，奖励%s %s" % \
                     (__sender_info_dic["nick"], win_point, self.currency)
        else:
            win_point = - win_point

        self.add_point(str(group_qq), __sender_info_dic["qq_number"], win_point)

        return result

    def timer(self):

        while self.running:

            self.current_second += 1
            if self.current_second > self.second_limit:
                self.over_game()

            time.sleep(1)

    def over_game(self):

        self.running = False

        if not self.has_winner:

            result = u"很遗憾，没人答对此题，此局24点游戏作废!"

            self.send_func(result)

        self.reset_info()
