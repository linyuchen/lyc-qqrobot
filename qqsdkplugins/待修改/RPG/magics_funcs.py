<<<<<<< HEAD:qqsdkplugins/待修改/RPG/magics_funcs.py
#coding=UTF8

import random

import goods_base
import things_funcs
from rpg_global_values import *


class MagicsFuncs(things_funcs.ThingsFuncs):

    magics_funcs_dic = {}

    def __init__(self):
        pass

    def add_magic_func(cls,magic_tag,func):
        cls.magics_funcs_dic[magic_tag] = func


def func(user_person,aim_person):
    
    failed = u"【%s】使用了妙手空空，结果什么都没发生"%(user_person.attrs[name_str_g])
    if user_person.attrs["tag"] == aim_person.attrs["tag"]:
        return u"不能对自己使用妙手空空哦~"
    if random.random() < 0.3:
        category = random.randint(0,1)
        if category == 0:
            things_list = aim_person.goods_list
        elif category == 1:
            things_list = aim_person.equip_list
        if not things_list:
            return failed
        goods = random.choice(things_list)
        aim_person.reduce_goods(goods[0],1)
        user_person.add_goods(goods[0],1,goods[2])
        goods = goods_base.all_goods_dic[goods[0]]

        result = u"【%s】使用了妙手空空，偷到了【%s】的一件 %s"%(user_person.attrs[name_str_g],aim_person.attrs[name_str_g],goods.attrs[name_str_g])
        return result

    else:
        return failed


magicsfuncs = MagicsFuncs()
magicsfuncs.add_magic_func("theft",func)

def func__(user_person,aim_person):

    lose_health = aim_person.attrs[health_limit_str_g] * 0.05


#print magicsfuncs.magics_funcs_dic



=======
#coding=UTF8

import random

import goods_base
import things_funcs
from rpg_global_values import *


class MagicsFuncs(things_funcs.ThingsFuncs):

    magics_funcs_dic = {}

    def __init__(self):
        pass

    def add_magic_func(cls,magic_tag,func):
        cls.magics_funcs_dic[magic_tag] = func


def func(user_person,aim_person):
    
    failed = u"【%s】使用了妙手空空，结果什么都没发生"%(user_person.attrs[name_str_g])
    if user_person.attrs["tag"] == aim_person.attrs["tag"]:
        return u"不能对自己使用妙手空空哦~"
    if random.random() < 0.3:
        category = random.randint(0,1)
        if category == 0:
            things_list = aim_person.goods_list
        elif category == 1:
            things_list = aim_person.equip_list
        if not things_list:
            return failed
        goods = random.choice(things_list)
        aim_person.reduce_goods(goods[0],1)
        user_person.add_goods(goods[0],1,goods[2])
        goods = goods_base.all_goods_dic[goods[0]]

        result = u"【%s】使用了妙手空空，偷到了【%s】的一件 %s"%(user_person.attrs[name_str_g],aim_person.attrs[name_str_g],goods.attrs[name_str_g])
        return result

    else:
        return failed


magicsfuncs = MagicsFuncs()
magicsfuncs.add_magic_func("theft",func)

def func__(user_person,aim_person):

    lose_health = aim_person.attrs[health_limit_str_g] * 0.05


#print magicsfuncs.magics_funcs_dic



>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/RPG/magics_funcs.py
