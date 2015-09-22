# -*- coding:UTF-8 -*-

from rpg_global_values import *
import goods_base 

class ThingsFuncs(object):

    things_funcs_dic = {}
    def __init__(self):
        pass
        
    #
    def add_attr(cls,person_obj,goods_tag,key_list):
        """
        @param attrs_list: [attr_key]
        """

        goods = goods_base.all_goods_dic[goods_tag]
        for attr_key in key_list:
            value = goods.attrs[attr_key]
            person_obj.attrs[attr_key] += value


    # 增加额外的属性
    def add_extra_attr(cls,person_obj,goods_tag,key_list):
        """
        @param attrs_list: [attr_key]
        """

        goods = goods_base.all_goods_dic[goods_tag]
        for attr_key in key_list:
#            print attr_key
            value = goods.attrs[attr_key]
#            print value
#            print type(value)
            if person_obj.extra_attrs.has_key(attr_key):
                person_obj.extra_attrs[attr_key] += value
            else:
                person_obj.extra_attrs[attr_key] = value

    def add_func(cls,thing_tag,key_list,ftype):

        if ftype == "extra":
            tfunc = cls.add_extra_attr
        elif ftype == "general":
            tfunc = cls.add_attr
        func = lambda person_obj: tfunc(person_obj,thing_tag,key_list)
        cls.things_funcs_dic[thing_tag] = func


thing_func = ThingsFuncs()

#微型生命药水
key_list = [health_str_g]
thing_func.add_func(hlth_wt_w_tag_str_g,key_list,ftype="general")
#小型生命药水
key_list = [health_str_g]
thing_func.add_func(hlth_wt_x_tag_str_g,key_list,ftype="general")

#微型魔法药水
key_list = [mana_str_g]
thing_func.add_func(mana_wt_w_tag_str_g,key_list,ftype="general")

#生命宝石
key_list = [health_limit_str_g]
thing_func.add_func(hlth_stone_tag_str_g,key_list,ftype="extra")
#魔法宝石
key_list = [mana_limit_str_g]
thing_func.add_func(mana_stone_tag_str_g,key_list,ftype="extra")
#经验书
key_list = [experience_str_g]
thing_func.add_func(experience_book_tag_str_g,key_list,ftype="general")

#喵之剑
key_list = [min_attack_force_str_g,max_attack_force_str_g]
thing_func.add_func(cat_sword_tag_str_g,key_list,ftype="extra")
#喵之盾
key_list = [defensive_str_g]
thing_func.add_func(cat_shield_tag_str_g,key_list,ftype="extra")
#print thing_func.things_funcs_dic

#七星宝剑
key_list = [min_attack_force_str_g,max_attack_force_str_g]
thing_func.add_func(seven_star_sword_tag_str_g,key_list,ftype="extra")

#雷神之盾
key_list = [defensive_str_g]
thing_func.add_func(thunder_shield_tag_str_g,key_list,ftype="extra")
