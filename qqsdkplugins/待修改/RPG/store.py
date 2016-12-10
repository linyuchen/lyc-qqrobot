#coding=UTF8

import goods_base
import store_base
from rpg_global_values import *

GoodsBase = goods_base.GoodsBase

class Store(store_base.StoreBase):

    def __init__(self):

        super(Store,self).__init__()
        
    def get_goods_tag_by_name(self,goods_name):

#        sql_str = "select tag from %s where name=?"%(goods_table_name_str_g)
#        result = sqlite.query(sql_str,(goods_name,))
        for goods in goods_base.all_goods_dic.values():
            if goods_name == goods.attrs[name_str_g]:
                return goods.attrs[tag_str_g]

        return None

        """

        if result:
            goods_tag = result[0][0]
        else:
            goods_tag = None

        return goods_tag

        """

    def shop_goods(self,person_obj,goods_name,num):

        goods_tag = self.get_goods_tag_by_name(goods_name)
        if not goods_tag:
            return u"商店没有【%s】这件商品哦"%goods_name
        shop_result = super(Store,self).shop_goods(person_obj,goods_tag,num)
        if 0 == shop_result:
            return u"购买【%s】成功"%goods_name
        elif 1 == shop_result:
            return u"很抱歉哦，您的余额不够，买不起【%s】"%goods_name
        elif 2 == shop_result:
            return u"您的物品或者装备超过%d个，不能再拿多余的物品！"%person_obj.max_things_num

    def sell_goods(self,person_obj,goods_name,num=1):

        goods_tag = self.get_goods_tag_by_name(goods_name)
        if not goods_tag:
            return u"这个世界有【%s】这个玩意儿吗"%(goods_name)


        sell_result = super(Store,self).sell_goods(person_obj,goods_tag,num)
#        print sell_result
        if sell_result[0] == 0:
            return u"【%s】卖掉了%d件 %s 回收了%d %s"%(person_obj.attrs[name_str_g], num, goods_name, sell_result[1], currency_name_str_g)
            
        elif sell_result[0] == -1:
            return u"您没有【%s】哦"%(goods_name)
        elif sell_result[0] == -2:
            return u"您的【%s】不够%d件哦"%(goods_name,num)

    def shop_magic(self,person_obj,magic_name):

        """
        """
        magic_tag = self.get_goods_tag_by_name(magic_name)
#        print magic_tag
        error = u"这个世界有【%s】这个技能吗"%(magic_name)
        if not magic_tag:
            return error
            
        
        magic = goods_base.all_goods_dic[magic_tag]
        if person_obj.attrs[gold_str_g] < magic.attrs[price_str_g]:
            return u"%s不足%d，无法学习 %s 这项技能"%(currency_name_str_g,magic.attrs[price_str_g],magic_name)
        if person_obj.attrs[level_str_g] < magic.attrs[level_str_g]:
            return u"必须要等级达到%d级才能学习 %s 哦"%(magic.attrs[level_str_g],magic_name)

        result = person_obj.add_magic(magic_tag)
        if result == -2:
            return u"你已经拥有 %s 这项技能了!"%(magic_name)
        elif result == 0:
            return u"学习 %s 成功！"%(magic_name)
        elif result == -1:
            return error
            
#        print result




