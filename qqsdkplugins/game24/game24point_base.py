#coding=UTF-8

from __future__ import division
import random
import re
import traceback

class Game24PointBase(object):

    def __init__(self):

        self.num_list = [i for i in range(1,14)]
#        print self.point_list
        self.arithmetic_operator_list = ["+","-","*","/","(",")"]
        self.now_num_list = []

    def start_game(self):

        self.now_num_list = self.get_random_num_list()
        return self.now_num_list
    
    def get_random_num_list(self):
        
        using_num_list = self.num_list[:]
        num_list = []
        for i in range(4):
            num = random.choice(using_num_list)
            using_num_list.remove(num)
            num_list.append(num)

        return num_list

    def judge(self,arithmetic_string,now_num_list):
        """
        @param arithmetic_string: 算术表达式
        @type: string

        @return -1: 数字不对
        @return 0: 式子正确
        @return 1: 算术结果不对
        @return 2：有不明符号
        """

        arithmetic_string = arithmetic_string.lower()

        arithmetic_string = arithmetic_string.replace(u"（","(").replace(u"）",")").replace(u"—","-").replace("x","*").replace(" ", "")
        #print arithmetic_string

        #检测是否是数字及运算符
        pattern = "[\d\+\-\*/\(\)]"
        com_str = re.compile(pattern)
        if re.sub(com_str,"",arithmetic_string):
            return 2

        pattern = "[\+\-\*/\(\)]"
        com_str = re.compile(pattern)
        arithmetic_string_ = re.sub(com_str," ",arithmetic_string)

        num_list = arithmetic_string_.split()
#        print num_list
        if len(num_list) != 4:
#            print u"len not 4"
            return -1
        while num_list:
            num = int(num_list.pop())
            if  num not in now_num_list:
#                print "not in self.num_list"
                return -1
            else:
                now_num_list.remove(num)

        try:
#            print eval(arithmetic_string)
            if eval(arithmetic_string) == 24:
                return 0
            else:
                return 1
        except:
            traceback.print_exc()
            return 2




if "__main__" == __name__:

    test = Game24PointBase()
#    test.get_random_point_list()
    now_num_list = test.start_game()
    print now_num_list

    arithmetic_string = raw_input("")
    print test.judge(arithmetic_string,now_num_list)
