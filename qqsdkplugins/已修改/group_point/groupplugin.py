#coding=UTF8

import os
cur_path = os.path.dirname(__file__) or "."

import sys
sys.path.append(cur_path + "/../..")

import time

from global_values import *
from grouppluginbase import GroupPluginBase

class GroupPlugin(GroupPluginBase):

    pointSummary = u"""
        活跃度代表着您在本群的发言数量，每发言一条增加一点活跃度。
        也可以通过玩群内小游戏获等等方获取取活跃度，很有趣的哦~

        建议群主每月将活跃度前三名的群成员设置为管理员，这样可以促进群的发展
    """

    def __init__(self,group_qq_number):

        super(GroupPlugin, self).__init__(group_qq_number)
        self.wealth_level_list = [(u"一无所有",0),(u"乞丐",2000),(u"无业游民",2800),(u"失业人口",6000),(u"打工仔",9800),(u"温饱户",16000),(u"白领",50000),(u"小康家庭",118000),(u"金领",250000),(u"暴发户",800000),(u"百万富翁",1800000),(u"千万富翁",10000000),(u"中国首富",88888888),(u"亚洲首富",333333333),(u"世界首富",888888888),(u"初入神境",100000000000000000000000000000000000000000000000000000000000),(u"人阶之神",200000000000000000000000000000000000000000000000000000000000),(u"地阶之神",300000000000000000000000000000000000000000000000000000000000),(u"天阶之神",500000000000000000000000000000000000000000000000000000000000),(u"仙阶之神",900000000000000000000000000000000000000000000000000000000000),(u"登峰造极",1000000000000000000000000000000000000000000000000000000000000),(u"造物主",10000000000000000000000000000000000000000000000000000000000000)] # (level name，point num)
        self.add_point = self._add_point

    def get_clear_chance(self, qq_number, nick):
        num = self._get_clear_chance(qq_number)
        return u"【%s】(%s)还有%d次清负机会" % (nick, qq_number, num)

    def clear_point(self, my_qq_number, my_nick, aim_qq_number, aim_nick):
        clear_chance = self._get_clear_chance(my_qq_number)
        if clear_chance <= 0:
            return u"【%s】(%s)清负机会次数不足，无法清负活跃度" % (my_nick, my_qq_number)

        point = self._get_point(aim_qq_number)
        if point > 0:
            return u"【%s】(%s)的活跃度还没负呢，确定要清负？" % (aim_nick, aim_qq_number)

        self._set_point(aim_qq_number, 0)
        clear_chance -= 1
        self._set_clear_chance(my_qq_number, clear_chance)

        return u"清负成功，【%s】(%s)还有%d次清负机会" % (my_nick, my_qq_number, clear_chance)


    def add_point(self, qq_number, nick, num=1):

        self._add_point(qq_number,nick,num)

    def get_point(self,qq_number,nick):

        point = self._get_point(qq_number)
        index = self._index_of_rank(qq_number)
        level = self.get_point_level(point)
        return u"%s (%s)的%s为%d点\n当前排名为 %d 位\n当前等级为（%s）"%(nick, qq_number, currency_name_str_g, point, index, level)

    def get_point_level(self,point):
        
        level = self.wealth_level_list[0][0]
        for i in self.wealth_level_list:
            if point > i[1]:
                level = i[0]
            else:
                break
        return level

    def get_level_summary(self):

        result = u"####等级说明####\n"
        for i in self.wealth_level_list:
            result += u"%s：%d\n"%(i[0],i[1])

        return result


    def get_point_rank(self):

        rank_list = self._get_point_rank()

        result = ""
        index = 1
        for i in rank_list:
#           i[0]: qq_number
#           i[1]: point
#           i[2]: name
            result += u"第%d名：%s(%s)，%s %s，等级(%s)\n"%(index, i[2],i[0],currency_name_str_g,i[1],self.get_point_level(i[1]))
            index += 1
        return result
    
        


    def sign(self,qq_number,nick):
        """

        """

        sign_info = super(GroupPlugin, self).sign(qq_number) # (sign_date, sign_count, continuous_sign_count, geted_point) 

        if None == sign_info:
            return u"今天【%s】已经签到过了，请不要重复签到！"%nick
        else:
            return u"【%s】签到成功，获得%d %s\n上次签到时间：%s\n已经连续签到 %d 天\n总签到了 %d 天"%(nick,sign_info[3], currency_name_str_g, sign_info[0], sign_info[2], sign_info[1])


    def transfer_point(self,qq_number,nick,param):
        
        error = u"命令有误！"
        param = param.split()
        #print param
        if len(param) < 2:
            return error

        aim_qq_number = param[0]
        num = param[1]
        if not num.isdigit():
            return error
        retcode = self._transfer_point(qq_number, nick, aim_qq_number, int(num))
        if retcode == 0:
            return u"转账成功！"
        elif retcode == 1:
            return u"对不起，您的余额不够要转的额度！"
        elif retcode == 2:
            return u"对不起，您要转账的对象不存在！"


if "__main__" == __name__:

    group = "3011590"
    member = "123"
    nick = "hi"
    test = GroupPlugin(group)

    print test.get_clear_chance(member, nick)

    print test.clear_point(member, nick)
    # print test.sign(member, nick)
    print test.get_point(member, nick)


