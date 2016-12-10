<<<<<<< HEAD:qqsdkplugins/待修改/idioms_solitaire/idiomssolitaire.py
#coding=UTF8

import os
import sys
import threading
import time
import traceback

cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import idiomssolitairebase
import grouppluginbase

from global_values import *

GroupPluginBase_ = grouppluginbase.GroupPluginBase


class IdiomsSolitaire(idiomssolitairebase.IdiomsSolitaireBase):

    def __init__(self):

        super(IdiomsSolitaire,self).__init__()

        self.reply_func = None

        self.game_limit_second = 30
        self.today_game_count = 100
        self.gc_table = "t_game_count"
        self.reset_game_info()


    def reset_game_info(self):

        super(IdiomsSolitaire,self).reset_game_info()
        self.current_game_winner_name = ""
        self.current_game_winner_qq_number = ""
        self.current_game_group_qq_number = ""
        self.current_game_group_uin = ""
        self.current_idiom = ""
        self.game_win_point = 0 
        self.game_succes_level_point = 100
        self.game_succes_level_point_percentage = (1000000 * 1000000 * 100000000 * 1000000) / 1.0
        self.game_success_point = 0
        self.success_count = 0
        self.overing = False
        self.GroupPluginBase = None
        

    def get_now_idiom_note(self,idiom):

        return u"当前成语为 【%s】 请接“%s”开头的成语, 每次接龙时间为%d秒，时间一到最后接上的一人为本场游戏赢家\n"%(idiom, idiom[-1], self.game_limit_second)

    def start_game(self,group_uin,reply_func):

        #print group_uin
        self.GroupPluginBase = GroupPluginBase_(group_uin)
        self.reply_func = reply_func
        self.current_game_group_uin = group_uin
        if self.current_idiom:
            return u"成语接龙游戏已经开始了，请勿重复！"
        self.exists_idiom_list = []
        self.current_idiom = self.get_random_idiom()
#        self.current_idiom = u"代代相传"
        self.start_time()
        return self.get_now_idiom_note(self.current_idiom)


    def judge_idiom(self,group_qq, member_qq, member_name, idiom):

        sender_info_dic = {"group_qq_number": group_qq, "group_uin": group_qq, "qq_number": member_qq, "nick": member_name}

        while self.overing:pass

        self.current_game_group_qq_number = sender_info_dic["group_qq_number"]
        self.current_game_group_uin = sender_info_dic["group_uin"]
        """
#        current_gamer_game_date = GroupPluginBase.get_idiomssolitaire_date(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
#        current_gamer_today_game_count = GroupPluginBase.get_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
        if current_gamer_game_date == time.strftime("%Y-%m-%d"):
            if current_gamer_today_game_count > self.today_game_count:
                return u"每人每天只能接龙 %d 次哦，请明天再玩吧~\n"%(self.today_game_count)
            else:
                GroupPluginBase.set_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"], current_gamer_today_game_count + 1)
        else:
            GroupPluginBase.set_idiomssolitaire_date(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
            GroupPluginBase.set_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"], 1)
        """

        result_code = self.judge(idiom)
        self.reset_timer()
        if 0 == result_code:
            return u"笨蛋！%s 不是成语！"%idiom

        elif 1 == result_code:
            if self.success_count > 100:
                return u"连续成功次数上限了，请重新开始游戏吧！"
            self.success_count += 1
            self.game_win_point += self.game_succes_level_point
            self.game_success_point += self.game_succes_level_point
            cur_player_point = self.GroupPluginBase._get_point(sender_info_dic["qq_number"])
            additional_win_point = cur_player_point / self.game_succes_level_point_percentage
            additional_win_point = int(additional_win_point)
            #print additional_win_point
            additional_win_point = additional_win_point if additional_win_point > 0 else 0
            self.GroupPluginBase._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],self.game_success_point + additional_win_point)
            self.game_succes_level_point_percentage /= 1.5 
            self.current_game_winner_name = sender_info_dic["nick"]
            self.current_game_winner_qq_number = sender_info_dic["qq_number"]
            self.exists_idiom_list.append(idiom)
            return u"恭喜 %s 接龙成功,奖励%d点%s\n接龙的越久，奖励越多哦~"%(sender_info_dic["nick"], self.game_success_point + additional_win_point, currency_name_str_g) + self.get_now_idiom_note(idiom)

        elif 2 == result_code:
            return u"%s 接龙失败！"%sender_info_dic["nick"] + self.get_now_idiom_note(self.current_idiom)

        elif 3 == result_code:
            return u"%s 这个成语已经出现过了,请换一个成语."%(idiom) + self.get_now_idiom_note(self.current_idiom)

        elif 4 == result_code:
            return u"成语接龙游戏还为未开始，请先发起游戏\n"

    def over_game(self):

        if self.current_game_winner_name:
            self.overing = True
            self.GroupPluginBase._add_point(self.current_game_winner_qq_number,self.current_game_winner_name, self.game_win_point)


            game_over_note = u"成语接龙游戏时间到\n恭喜【%s】赢得本场游戏胜利，奖励%d %s"%(self.current_game_winner_name, self.game_win_point,currency_name_str_g)
        else:
            game_over_note = u"成语接龙游戏时间到，很遗憾，没一个人想出来【%s】字开头的成语"%self.current_idiom[-1]

#        print game_over_note
        try:
            self.reply_func( game_over_note)
        except:
            traceback.print_exc()
        self.overing = False
        self.reset_game_info()

    def timer(self):

#        print "timer run"
        self.current_game_second = 0
        while True:
#            print self.current_game_second
            if self.current_game_second > self.game_limit_second:
                break
            time.sleep(1)
            self.current_game_second += 1

        self.over_game()
    
    def reset_timer(self):

        self.current_game_second = 0
    

    def start_time(self):

        threading.Thread(target=self.timer).start()

if "__main__" == __name__:

    test = IdiomsSolitaire()
    print test.start_game("g",None)
    sender_info_dic = {"nick":u"我", "qq_number":"q", "group_qq_number": "g", "group_uin": "uin"}
    while True:
        idiom = raw_input().decode("gbk")
        print test.judge_idiom(sender_info_dic,idiom)
=======
#coding=UTF8

import os
import sys
import threading
import time
import traceback

cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/../group_point")
import idiomssolitairebase
import grouppluginbase

from global_values import *

GroupPluginBase_ = grouppluginbase.GroupPluginBase


class IdiomsSolitaire(idiomssolitairebase.IdiomsSolitaireBase):

    def __init__(self):

        super(IdiomsSolitaire,self).__init__()

        self.reply_func = None

        self.game_limit_second = 30
        self.today_game_count = 100
        self.gc_table = "t_game_count"
        self.reset_game_info()


    def reset_game_info(self):

        super(IdiomsSolitaire,self).reset_game_info()
        self.current_game_winner_name = ""
        self.current_game_winner_qq_number = ""
        self.current_game_group_qq_number = ""
        self.current_game_group_uin = ""
        self.current_idiom = ""
        self.game_win_point = 0 
        self.game_succes_level_point = 100
        self.game_succes_level_point_percentage = (1000000 * 1000000 * 100000000 * 1000000) / 1.0
        self.game_success_point = 0
        self.success_count = 0
        self.overing = False
        self.GroupPluginBase = None
        

    def get_now_idiom_note(self,idiom):

        return u"当前成语为 【%s】 请接“%s”开头的成语, 每次接龙时间为%d秒，时间一到最后接上的一人为本场游戏赢家\n"%(idiom, idiom[-1], self.game_limit_second)

    def start_game(self,group_uin,reply_func):

        #print group_uin
        self.GroupPluginBase = GroupPluginBase_(group_uin)
        self.reply_func = reply_func
        self.current_game_group_uin = group_uin
        if self.current_idiom:
            return u"成语接龙游戏已经开始了，请勿重复！"
        self.exists_idiom_list = []
        self.current_idiom = self.get_random_idiom()
#        self.current_idiom = u"代代相传"
        self.start_time()
        return self.get_now_idiom_note(self.current_idiom)


    def judge_idiom(self,group_qq, member_qq, member_name, idiom):

        sender_info_dic = {"group_qq_number": group_qq, "group_uin": group_qq, "qq_number": member_qq, "nick": member_name}

        while self.overing:pass

        self.current_game_group_qq_number = sender_info_dic["group_qq_number"]
        self.current_game_group_uin = sender_info_dic["group_uin"]
        """
#        current_gamer_game_date = GroupPluginBase.get_idiomssolitaire_date(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
#        current_gamer_today_game_count = GroupPluginBase.get_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
        if current_gamer_game_date == time.strftime("%Y-%m-%d"):
            if current_gamer_today_game_count > self.today_game_count:
                return u"每人每天只能接龙 %d 次哦，请明天再玩吧~\n"%(self.today_game_count)
            else:
                GroupPluginBase.set_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"], current_gamer_today_game_count + 1)
        else:
            GroupPluginBase.set_idiomssolitaire_date(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"])
            GroupPluginBase.set_today_idiomssolitaire_count(sender_info_dic["group_qq_number"], sender_info_dic["qq_number"], 1)
        """

        result_code = self.judge(idiom)
        self.reset_timer()
        if 0 == result_code:
            return u"笨蛋！%s 不是成语！"%idiom

        elif 1 == result_code:
            if self.success_count > 100:
                return u"连续成功次数上限了，请重新开始游戏吧！"
            self.success_count += 1
            self.game_win_point += self.game_succes_level_point
            self.game_success_point += self.game_succes_level_point
            cur_player_point = self.GroupPluginBase._get_point(sender_info_dic["qq_number"])
            additional_win_point = cur_player_point / self.game_succes_level_point_percentage
            additional_win_point = int(additional_win_point)
            #print additional_win_point
            additional_win_point = additional_win_point if additional_win_point > 0 else 0
            self.GroupPluginBase._add_point(sender_info_dic["qq_number"],sender_info_dic["nick"],self.game_success_point + additional_win_point)
            self.game_succes_level_point_percentage /= 1.5 
            self.current_game_winner_name = sender_info_dic["nick"]
            self.current_game_winner_qq_number = sender_info_dic["qq_number"]
            self.exists_idiom_list.append(idiom)
            return u"恭喜 %s 接龙成功,奖励%d点%s\n接龙的越久，奖励越多哦~"%(sender_info_dic["nick"], self.game_success_point + additional_win_point, currency_name_str_g) + self.get_now_idiom_note(idiom)

        elif 2 == result_code:
            return u"%s 接龙失败！"%sender_info_dic["nick"] + self.get_now_idiom_note(self.current_idiom)

        elif 3 == result_code:
            return u"%s 这个成语已经出现过了,请换一个成语."%(idiom) + self.get_now_idiom_note(self.current_idiom)

        elif 4 == result_code:
            return u"成语接龙游戏还为未开始，请先发起游戏\n"

    def over_game(self):

        if self.current_game_winner_name:
            self.overing = True
            self.GroupPluginBase._add_point(self.current_game_winner_qq_number,self.current_game_winner_name, self.game_win_point)


            game_over_note = u"成语接龙游戏时间到\n恭喜【%s】赢得本场游戏胜利，奖励%d %s"%(self.current_game_winner_name, self.game_win_point,currency_name_str_g)
        else:
            game_over_note = u"成语接龙游戏时间到，很遗憾，没一个人想出来【%s】字开头的成语"%self.current_idiom[-1]

#        print game_over_note
        try:
            self.reply_func( game_over_note)
        except:
            traceback.print_exc()
        self.overing = False
        self.reset_game_info()

    def timer(self):

#        print "timer run"
        self.current_game_second = 0
        while True:
#            print self.current_game_second
            if self.current_game_second > self.game_limit_second:
                break
            time.sleep(1)
            self.current_game_second += 1

        self.over_game()
    
    def reset_timer(self):

        self.current_game_second = 0
    

    def start_time(self):

        threading.Thread(target=self.timer).start()

if "__main__" == __name__:

    test = IdiomsSolitaire()
    print test.start_game("g",None)
    sender_info_dic = {"nick":u"我", "qq_number":"q", "group_qq_number": "g", "group_uin": "uin"}
    while True:
        idiom = raw_input().decode("gbk")
        print test.judge_idiom(sender_info_dic,idiom)
>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/idioms_solitaire/idiomssolitaire.py
