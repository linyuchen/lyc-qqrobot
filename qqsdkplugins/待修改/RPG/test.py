#coding=UTF8

from global_values import *

import person
import store

Person = person.Person
store = store.Store()
p1 = Person("p1")
p1.attrs[name_str_g] = "p1"
p2 = Person("p2")
p2.attrs[name_str_g] = "p2"
print p1.get_state()
print p2.get_state()
#print p1.things_list
#print p1.goods_list
#print p1.equip_list
print p1.get_things_list("g")
print p1.get_things_list("e")
#print p2.get_state()
print store.show_goods_list()
#print store.shop_goods(p1,u"喵之剑")
#print store.sell_goods(p1,u"喵之剑")
#print p1.things_list
#print p1.get_things_list("e")
#print p1.equip_list
#    p1.resurgence()
#    p2.resurgence()
#    print p1.get_knapsack(ktype="goods")
for i in range(0):
    result = p1.attack(p2)
    print result[0]
    if result[1] not in ["-1","0"]:
        print u"\n【%s】反击："%(p2.attrs[name_str_g])
        print p2.attack(p1)
