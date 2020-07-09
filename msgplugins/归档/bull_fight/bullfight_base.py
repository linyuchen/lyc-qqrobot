# coding=UTF8

import random


class BullFightBase(object):

    def __init__(self):

        self.int2alpha_dic = {"11": "J", "12": "Q", "13": "K", "1": "A"}
        self.alpha2int_dic = {"J": "10", "Q": "10", "K": "10", "A": "1"}
        self.alpha2int_dic2 = {"J": "11", "Q": "12", "K": "13", "A": "1"}
        self.flower_color_list = [u"黑桃", u"红心", u"梅花", u"方块"]
        self.poker_list = []
        for flower_color in self.flower_color_list:
            self.poker_list += [(flower_color, self.convert_poker(str(number), opera_type=1))
                                for number in range(1, 14)]

        self.combine_list = []
        self.rest_poker_list = []
        self.__combine(5, 3, self.combine_list)

        self.reset_game_info()

    def convert_poker(self, __poker, opera_type):
        """
        convert 11,12,13,1 to J,Q,K,A ,or reverse
        @param __poker: 牌名
        @param opera_type: 1, int to alpha
        @param opera_type: 2, alpha to int J Q K to 10 10 10
        @param opera_type: 3, alpha to int J Q K to 11 12 13
        @type: int

        @rtype: list
        """

        poker_dic = {}
        if 1 == opera_type:
            poker_dic = self.int2alpha_dic
        
        elif 2 == opera_type:
            poker_dic = self.alpha2int_dic

        elif 3 == opera_type:
            poker_dic = self.alpha2int_dic2

        if __poker in poker_dic:
            return __poker.replace(__poker, poker_dic[__poker])
        else:
            return __poker

    def get_random_poker(self):

        __poker = random.choice(self.rest_poker_list)
        self.rest_poker_list.remove(__poker)

        return __poker

    def reset_game_info(self):

        self.rest_poker_list = self.poker_list[:]

    def get_poker_type(self, __poker_list):
        """
        获取牌的点数大小
        @param __poker_list:
        @return: {"type":牌型,"max_poker":最大的牌,"point":牛的点数(int)（如果是四炸则为四炸的牌点数）,
            "multiple":倍数(int)} 牌型：0 无牛，1 有牛，2 四炸，3 五花牛，4 五小牛
        @rtype: dict
        """
        __result_dic = {}
        bull_point = self.get_bull_point(__poker_list)
        bull_multiple = self.get_bull_multiple(bull_point)
        max_poker = self.get_max_poker(__poker_list)
        is4bomb = self.is4bomb(__poker_list)
        if self.is5little_bull(__poker_list):
            __result_dic["type"] = 4
            __result_dic["max_poker"] = max_poker
            __result_dic["multiple"] = 8
        elif self.is5color_bull(__poker_list):
            __result_dic["type"] = 3
            __result_dic["max_poker"] = max_poker
            __result_dic["multiple"] = 5
        elif is4bomb:
            __result_dic["type"] = 2
            __result_dic["max_poker"] = is4bomb
            __result_dic["point"] = is4bomb[1]
            __result_dic["multiple"] = 4
        elif bull_point:
            __result_dic["type"] = 1
            __result_dic["max_poker"] = max_poker
            __result_dic["point"] = bull_point
            __result_dic["multiple"] = bull_multiple
        else:
            __result_dic["type"] = 0
            __result_dic["max_poker"] = max_poker
            __result_dic["point"] = bull_point
            __result_dic["multiple"] = 1

        return __result_dic

    @staticmethod
    def get_bull_multiple(bull_point):

        if bull_point < 8:
            return 1
        elif bull_point == 8 or bull_point == 9:
            return 2
        elif bull_point == 10:
            return 3

    def get_bull_point(self, __poker_list):
        """
        @return False:不是牛
        @return:integer 牛的点数
        """

        bull_index_list = self.get_bull_index_list(__poker_list)
        rest_index_list = bull_index_list[1]
        if not bull_index_list[0]:
            return False

        point1 = int(self.convert_poker(__poker_list[rest_index_list[0]][1], opera_type=2))
        point2 = int(self.convert_poker(__poker_list[rest_index_list[1]][1], opera_type=2))
        point = point1 + point2
        bull_point = point % 10
        if bull_point == 0:
            bull_point = 10

        return bull_point

    def compare_poker_list(self, poker1_list, poker2_list):

        poker1_type = self.get_poker_type(poker1_list)
        poker2_type = self.get_poker_type(poker2_list)
        max_poker1 = poker1_type["max_poker"]
        max_poker2 = poker2_type["max_poker"]
        # max_poker1_point = int(self.convert_poker(max_poker1[1], 3))
        # max_poker2_point = int(self.convert_poker(max_poker2[1], 3))
        
        if poker1_type["type"] > poker2_type["type"]:
            return True
        elif poker1_type["type"] == poker2_type["type"]:

            if (poker1_type["type"] != 1) and (poker1_type != 2):
                return self.compare_poker(max_poker1, max_poker2)
                
            else:
                point1 = poker1_type["point"]
                point2 = poker2_type["point"]
                if point1 > point2:
                    return True
                elif point1 == point2:
                    return self.compare_poker(max_poker1, max_poker2)

        return False

    def is5little_bull(self, __poker_list):
        """
        @rtype: bool
        """
        num = 0
        for __poker in __poker_list:
            point = __poker[1]
            point = int(self.convert_poker(point, 2))
            if point < 5:
                num += point
                if num > 10:
                    return False
            else:
                return False

        return True

    @staticmethod
    def is5color_bull(__poker_list):
        """
        @rtype: bool
        """

        for __poker in __poker_list:
            if __poker[1] not in ["J", "K", "Q"]:
                return False

        return True

    @staticmethod
    def is4bomb(__poker_list):
        """
        @return False: not 4bomb
        @return __poker:the 4bomb __poker
        @rtype: __poker 二元数组
        """

        point_list = [__poker[1] for __poker in __poker_list]
        for __poker in __poker_list:
            if point_list.count(__poker[1]) >= 4:
                return __poker

        return False

    def get_max_poker(self, __poker_list):

        max_poker = ()
        max_point = 0
        for __poker in __poker_list:
            point = __poker[1]
            # color = __poker[0]
            point = int(self.convert_poker(point, 3))
            if point > max_point:
                max_point = point
                max_poker = __poker
            elif point == max_point:
                if self.compare_color(__poker[0], max_poker[0]):
                    max_poker = __poker

        return max_poker

    def compare_poker(self, poker1, poker2):

        point1 = int(self.convert_poker(poker1[1], 3))
        point2 = int(self.convert_poker(poker2[1], 3))
        if point1 > point2:
            return True

        elif point1 == point2:
            return self.compare_color(poker1[0], poker2[0])

        return False

    def compare_color(self, color1, color2):
        """
        @return True: color1 > color2
        @return False: color2 > color1
        """
        color_index1 = self.flower_color_list.index(color1)
        color_index2 = self.flower_color_list.index(color2)

        return color_index1 < color_index2

    def get_bull_index_list(self, __poker_list):
        """
        @param __poker_list: [(flower_color,poink)...]
        @return: [],[]  牛的index_list,剩余牌的index_list, if [],not bull

        """

        bull_index_list = []  # 最大牛的index

        for index_list in self.combine_list:
            poker_list_ = []
            for index in index_list:
                poker_list_.append(__poker_list[index - 1])

            if sum([int(self.convert_poker(__poker[1], opera_type=2)) for __poker in poker_list_]) % 10 == 0:
                bull_index_list = index_list

        rest_index_list = list(set(bull_index_list) ^ set(range(1, 6)))  # 剩下两张牌的index

        return [index - 1 for index in bull_index_list], [index-1 for index in rest_index_list]
                    
    def __combine(self, all_count, need_count, result_list, buffer_list=[]):

        if need_count == 0:
            return 1
        x = all_count
        while x >= need_count:
            
            buffer_list.append(x)
            if self.__combine(x - 1, need_count - 1, result_list, buffer_list):
                result_list.append(buffer_list[:])
            buffer_list.pop()
            x -= 1

        return 0


if "__main__" == __name__:

    test = BullFightBase()
    poker_list = [test.get_random_poker() for i in range(5)]
#    无牛
    poker_list = [(u"红心", "7"), (u"红心", "3"), (u"红心", "2"), (u"红心", "6"), (u"黑桃", "3")]
    result_dic = test.get_poker_type(poker_list)
    print result_dic
    print result_dic["max_poker"][0]
#    print test.compare_color(u"红心",u"黑桃")
    poker_list1 = [test.get_random_poker() for i in range(5)]
    poker_list1 = [(u"黑桃", "J"), (u"梅花", "A"), (u"方块", "7"), (u"梅花", "8"), (u"红心", "9")]
    print ",".join([poker[0]+poker[1] for poker in poker_list1])
    poker_list2 = [test.get_random_poker() for i in range(5)]
    poker_list2 = [(u"梅花", "7"), (u"梅花", "10"), (u"黑桃", "6"), (u"黑桃", "3"), (u"方块", "A")]
    print ",".join([poker[0]+poker[1] for poker in poker_list2])
    print test.compare_poker_list(poker_list1, poker_list2)
#    print test.compare_poker((u"黑桃","2"),(u"红心","2"))
