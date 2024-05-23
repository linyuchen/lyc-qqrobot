# coding=UTF-8


class Game(object):

    def __init__(self):

        self.int2alpha_dic = {"11": "J", "12": "Q", "13": "K", "1": "A"}
        self.alpha2int_dic = {"J": "10", "Q": "10", "K": "10", "A": "1"}

    def get_max_poker(self, poker_list):
        """
        @type poker_list: list
        @param poker_list: [[],], The 2 dimension list

        @rtype: ([],int)
        @return:(max_point_list, max_point) 
        """

        max_poker = []
        max_point = 0
        point_list = []
        max_point_index = 0

        for i in poker_list:
            point_list.append(self.get_sum_point(i))

        max_point = self.get_max_point(point_list)
        max_point_index = point_list.index(max_point)
        max_poker = poker_list[max_point_index]

        return max_poker, max_point

    def get_max_point(self, point_list):

        point_list.sort()

        if point_list[0] < 22:
            max_point = point_list[0]
            for point in point_list[1:]:
                if max_point < point < 22:
                    max_point = point
        else:
            max_point = point_list[0]

        return max_point

    def get_sum_point(self, poker_list):

        poker_list = map(int, poker_list)
        point = sum(poker_list)

        return point

    def convert_poker(self, poker, opera_type):
        """
        convert 11,12,13,1 to J,Q,K,A ,or reverse

        @param opera_type: 1, int to alpha
        @param opera_type: 2, alpha to int
        @type: int

        @type poker_list: list
        @rtype: list
        """

        if 1 == opera_type:
            poker_dic = self.int2alpha_dic

        elif 2 == opera_type:
            poker_dic = self.alpha2int_dic

        if poker in poker_dic:
            return poker.replace(poker, poker_dic[poker])
        else:
            return poker


if "__main__" == __name__:
    test = Game()
    #    print test.get_max_poker([["12","11"],["1","11"]])
    #    print test.convert_poker("J", 2)
    print(test.get_max_point([111, 22, 78]))
