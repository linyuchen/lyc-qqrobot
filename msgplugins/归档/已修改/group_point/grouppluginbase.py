#coding=UTF8


import sys


import thread
import time
import sys
import re
import os
import traceback

#import sqliteserver

cur_path = os.path.dirname(__file__)
cur_path = cur_path or "."
sys.path.append(cur_path + "/../sqlite_sserver/")

import sqliteSclient
import sqlite_db_config
#sqlite_server = sqliteserver.Sqlite(DB_PATH)
#sqlite_server = sqliteserver.Sqlite_Safe(DB_PATH)

class GroupPluginBase(object):

    def __init__(self,group_qq):

#        self.qq_instance = qq_instance
        self.t_group_point = "t_point"
        self.sqlite = sqliteSclient.Sqlite(sqlite_db_config.sqlite_server, sqlite_db_config.sqlite_port, sqlite_db_config.groupmdb_name)
#       签到加活跃度算法：
#       获得活跃度 = 连续签到天数 * self.sign_add_percentage * 自身活跃度
#       如果 获得活跃度 < self.sign_point 则获得活跃度 =  self.sign_point
        self.sign_point = 2000 #  签到获得
        self.sign_add_percentage = 1. / 10000 # 签到一次所加万分比 
        self.point_table = "t_point"
        self.sign_table = "t_sign"
        self.sign_continuous_table = "t_sign_continuous"
        self.clear_table = "t_clear_chance" # 清负机会
        
        self.group_qq = group_qq

        self.__get_value = self.sqlite.get_value
        self.__set_value = self.sqlite.set_value

    def _get_clear_chance(self, qq_number):
        result = self.__get_value(self.clear_table, ["chance"], {"member_qq":qq_number})
        if result:
            return result[0][0]
        else:
            return 0

    def _set_clear_chance(self, qq_number, num):
        self.__set_value(self.clear_table, {"chance":int(num), "member_qq":qq_number}, {"member_qq": qq_number})

    def _add_clear_chance(self, qq_number, num):
        current_num = self._get_clear_chance(qq_number)
        current_num += num
        self._set_clear_chance(qq_number, current_num)
    
    def _get_point(self, qq_number):
        """
        @return point:int
        """
        
        result = self.__get_value(self.point_table, ["point"], {"group_qq": self.group_qq, "member_qq":qq_number})

        if result:
            return int(eval(result[0][0]))
        else:
            return 0

    def _set_point(self, qq_number, num):

        self.__set_value(self.point_table, {"point":unicode(num), "group_qq": self.group_qq, "member_qq":qq_number}, {"group_qq": self.group_qq, "member_qq": qq_number})

    def _add_point(self, qq_number, name, num=1):

        num = int(num)
        result = self.__get_value(self.point_table, ["point"], {"group_qq": self.group_qq, "member_qq":qq_number})

        if result:
            old_point = int(eval(result[0][0]))
        else:
            old_point = 0

        #print old_point

        self.__set_value(self.point_table, {"group_qq": self.group_qq, "member_qq": qq_number, "point":unicode(old_point + num), "name": name}, {"group_qq": self.group_qq, "member_qq": qq_number})

    def _transfer_point(self, my_qq_number, my_name, aim_qq_number, num):
        """
        @return: 1 no enough, 2 aim_qq_number not exists, 0 success
        @rtype: int
        """
        point = self._get_point(my_qq_number)
#        print point
        if point < num or point == 0:
            return 1
        aim_info = self.__get_value(self.point_table, ["point", "name"], {"group_qq":self.group_qq, "member_qq":aim_qq_number})
        if aim_info == []:
            return 2

        self._add_point(my_qq_number, my_name, -num)
        self._add_point(aim_qq_number, aim_info[0][1], num)

        return 0


    def _get_point_rank(self,num=10):
        """
        @return: [("qq_number",point int,"name"),]
        @rtype: list
        """

        sql_string = "SELECT member_qq,point,name FROM %s where group_qq='%s' ORDER BY point+0 DESC LIMIT %d"%(self.t_group_point, self.group_qq, num)
        result = self.sqlite.query(sql_string)
        result = [(i[0],int(eval(i[1])), i[2]) for i in result]
#        print result

        return result


    def _index_of_rank(self, qq_number):

        sql_string = "SELECT member_qq,point FROM %s where group_qq='%s' ORDER BY point+0 DESC LIMIT -1"%(self.t_group_point, self.group_qq)
        all_rank_list = self.sqlite.query(sql_string)
#        print all_rank_list
        point = self._get_point(qq_number) 
        indexTuple = [unicode(qq_number),u"%d"%(point)]
        index = all_rank_list.index(indexTuple)

        return index + 1


    def __check_continue_sign(self, sign_date):

        last_time = time.time() - time.mktime(time.strptime(sign_date,"%Y-%m-%d"))
        if last_time >= (2 * 24 * 60 * 60):
            return False
        return True


    def sign(self, qq_number):
        """
        @return None: signed
        @return: (sign_date, sign_count, continuous_sign_count, geted_point)
        @rtype: tuple
        """

        sign_info = self.__get_value(self.sign_table, ["sign_date", "total", "continuous"], {"group_qq":self.group_qq, "member_qq": qq_number})
        today = time.strftime("%Y-%m-%d")
        continuous_sign_count = 0
        sign_total = 0
        if sign_info:
            last_sign_date = sign_info[0][0]
            sign_total = sign_info[0][1] 
            continuous_sign_count = sign_info[0][2]
            
            if last_sign_date == today:
                return None
            elif not self.__check_continue_sign(last_sign_date):
                continuous_sign_count = 0
        else:
            last_sign_date = today
        continuous_sign_count += 1
        sign_total += 1
        self.__set_value(self.sign_table, {"member_qq": qq_number, "sign_date": today, "continuous": continuous_sign_count,
            "total": sign_total, "group_qq": self.group_qq}, {"group_qq": self.group_qq, "member_qq": qq_number})

#            print continuous_sign_count
        point = self._get_point(qq_number)
        geted_point = point * self.sign_add_percentage * (continuous_sign_count)
#            print geted_point
        #geted_point = self.sign_point + geted_point
        if geted_point < self.sign_point:
            geted_point = self.sign_point
        geted_point = int(geted_point)
#            print geted_point
        if geted_point < 2000:
            geted_point = 2000 * continuous_sign_count
        self._add_point(qq_number, "", geted_point)

        return last_sign_date, sign_total, continuous_sign_count, geted_point



if "__main__" == __name__:

    group_qq = "30115908"
    member_qq = "1412971608"
    member_name = u"name"
    test = GroupPluginBase(group_qq)
    #print test._get_point(member_qq)
#    test._add_point(member_qq, member_name, 1)
#    test._set_point(member_qq, 0)
#    print test.sign(member_qq)
    print test._get_clear_chance(member_qq)
    print test._add_clear_chance(member_qq, 2)
#    print test._set_clear_chance(member_qq, 2)

    

