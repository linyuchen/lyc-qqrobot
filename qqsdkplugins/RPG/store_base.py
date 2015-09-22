# -*- coding:UTF-8 -*-

import sys
import db_server

import goods_base

from rpg_global_values import *



class StoreBase(object):

    def __init__(self):

        self.goods_list = []
        self.sqlite = db_server.sqlite
        self.read_goods_list()
        self.sell_return_percentage = 0.8


    def read_goods_list(self):

        sql_string = "select tag from %s"%(goods_table_name_str_g)
        result = self.sqlite.query(sql_string)
#        print result

        for i in result:

            self.goods_list.append(goods_base.all_goods_dic[i[0]])

    def get_tag_by_name(self,name):
        """
        @param name: goods name
        @return goods_object: None not exists
        """

        for goods in self.goods_list:
            if goods.attrs[name_str_g] == name:
                return goods

    def show_goods_list(self,category):
        """
        @param category: "g" goods, "e" equip, "m" magic
        """
        if category == "g":
            category = goods_category_str_g
        elif category == "e":
            category = equip_category_str_g
        elif category == "m":
            category = magic_category_str_g
        show_string = ""
        for i in self.goods_list:
            if category != i.attrs[category_str_g]:
                continue
            show_string += u"%s，价格：%d %s\n简介：%s\n\n"%(i.attrs[name_str_g],i.attrs[price_str_g],currency_name_str_g,i.attrs[summary_str_g])

        return show_string

    def shop_goods(self,person_obj,goods_tag,num):
        """
        @return success_state: 
            0 : succe
            1 : gold not enough
            2 : num too large
        @rtype: integer
        """

        goods = goods_base.all_goods_dic[goods_tag]
        price = goods.attrs[price_str_g] * num
        person_gold = person_obj.attrs[gold_str_g]
#        print person_obj.get_things_num()
        if (num + person_obj.get_things_num()) > person_obj.max_things_num:
            return 2
#        print type(person_gold)
#        print type(price)

        if person_gold < price:
            return 1
        else:
            person_obj.add_goods(goods_tag,num,goods.attrs[category_str_g])
            person_obj.attrs[gold_str_g] -= price

#        person_obj.save()
        return 0

    def sell_goods(self,person_obj,goods_tag,num=1):
        """
        @reutrn 0,gold: sell success
        @return -1,0: not has the goods
        """


        goods = goods_base.all_goods_dic[goods_tag]
        price = goods.attrs[price_str_g] * num * self.sell_return_percentage
        price =int(price)
        person_gold = person_obj.attrs[gold_str_g]
        reduce_result = person_obj.reduce_goods(goods_tag,num)
#        print reduce_result
        if reduce_result == 0:
            person_obj.attrs[gold_str_g] += price
            return 0,price
        else:
            return reduce_result,0




if "__main__" == __name__:

    test = StoreBase()
#    print test.goods_dic["hlth_wt_w"].attrs
    print test.show_goods_list()
    



