#coding=UTF

import random

import knapsack_base
import magics_funcs
import store_base
import things_funcs

things_funcs = things_funcs.ThingsFuncs()
magics_funcs = magics_funcs.MagicsFuncs()
knapsack = knapsack_base.KnapsackBase()
store = store_base.StoreBase()
from things_base import *


class PersonBase(ThingsBase):

    def __init__(self,tag):

        super(PersonBase, self).__init__(tag)

        self.table_name = person_table_name_str_g

        #基本属性
        self.max_things_num = 24
        self.attrs[power_str_g] = 10
        self.attrs[level_health_str_g] = 20 # 每级增加的血量
        self.attrs[level_mana_str_g] = 5 # 每级增加的魔法值
        self.attrs[level_attack_force_str_g] = 5 # 每级增加的攻击力
        self.attrs[level_defensive_str_g] = 5 # 每级增加的防御力
        self.attrs[gold_str_g] = 0 # 拥有的财富
        
        self.attrs[die_experience_str_g] = self.attrs[level_str_g] * 3 # 死亡掉落的经验值
        self.attrs[die_gold_str_g] = 10 # 死亡掉落的财富
        self.attrs[level_die_gold_str_g] = 3 # 每级增加的死亡掉落财富
        self.attrs[up_experience_percentage_str_g] = 0.3# 下一级所需经验值为上一级的百分比
        self.attrs[up_experience_str_g] = 30 # 下一级所需的经验值
        self.attrs[is_die_str_g] = 0

        self.attack2die_limit_count = 50000
#        self.create_table()
        self.init_all()

    def init_all(self):

        self.init_extra_attrs()
        self.read()
       
        self.read_knapsack()
        self.sorting_knapsack()
        self.dress_equip()
 
    def init_extra_attrs(self):
        # 额外属性
        self.extra_attrs = {}
        self.extra_attrs[health_limit_str_g] = 0
        self.extra_attrs[mana_limit_str_g] = 0
        self.extra_attrs[health_str_g] = 0
        self.extra_attrs[mana_str_g] = 0
        self.extra_attrs[min_attack_force_str_g] = 0
        self.extra_attrs[max_attack_force_str_g] = 0
        self.extra_attrs[defensive_str_g] = 0


    def read_knapsack(self):
        # 读取背包
        self.things_list = knapsack.read(self.attrs[tag_str_g]) # [[thing_tag,num,category,name],...]
        
    def get_things_num(self):

        return sum([thing[1] for thing in self.things_list])

    def sorting_knapsack(self):

        self.equip_list = [thing for thing in self.things_list if thing[2] == equip_category_str_g]
        self.goods_list = [thing for thing in self.things_list if thing[2] == goods_category_str_g]
        self.magic_list = [thing for thing in self.things_list if thing[2] == magic_category_str_g]


    def save_knapsack(self):

        """
        for i in self.things_list:
            print i[1]
            if i[1] <= 0:
                knapsack.del_thing(self.attrs[tag_str_g,i[0]])
        """
        knapsack.save(self.attrs[tag_str_g], self.things_list)


    def dress_equip(self):

        # 装上装备
        for equip in self.equip_list:
            for i in xrange(equip[1]):
                things_funcs.things_funcs_dic[equip[0]](self)
        # 把额外属性加入基本属性
        for key in self.attrs:
            if self.extra_attrs.has_key(key):
#                print type(self.attrs[key]), type(self.extra_attrs[key])
                all = long(self.attrs[key]) + self.extra_attrs[key]
                self.attrs[key] = all
    
    def unwield(self):

        for key in self.attrs:
            if self.extra_attrs.has_key(key):
                self.attrs[key] -= self.extra_attrs[key]

        self.init_extra_attrs()

    def get_up_experience(self):

        up_experience = self.attrs[up_experience_str_g] * (1 + self.attrs[up_experience_percentage_str_g])
        return int(up_experience)

    def check_up_level(self):

        if self.attrs[experience_str_g] > self.attrs[up_experience_str_g]:
            self.attrs[level_str_g] += 1
            self.attrs[experience_str_g] -= self.attrs[up_experience_str_g]
            self.attrs[up_experience_str_g] = self.get_up_experience()
            self.attrs[health_str_g] += self.attrs[level_health_str_g]
            self.attrs[health_limit_str_g] += self.attrs[level_health_str_g]
            self.attrs[mana_limit_str_g] += self.attrs[level_mana_str_g]
            self.attrs[min_attack_force_str_g] += self.attrs[level_attack_force_str_g]
            self.attrs[max_attack_force_str_g] += self.attrs[level_attack_force_str_g]
            self.attrs[defensive_str_g] += self.attrs[level_defensive_str_g]
            self.attrs[die_experience_str_g] = self.attrs[level_str_g] * 3 # 死亡掉落的经验值
            self.attrs[die_gold_str_g] += self.attrs[level_die_gold_str_g]
            return True
        else:
            return False

    def attack(self,attacked_person):

        attack_result = self._attack(self,attacked_person)
#        attack_result = self._attack(attack_person,attacked_person)
#        attacked_result = self._attack(attacked_person,attack_person)
#        attack_person.save()
#        attacked_person.save()
#        self.save()

        return attack_result


    def _attack(self,attack_person,attacked_person):
        """
        @param attack_person: 攻击者obj
        @param attacked_person: 被攻击者obj
        @type: Person

        @return result_dic:
            {attack_result: str
                -1: 攻击者死亡状态，无法攻击
                0: 被攻击者死亡状态，无法攻击
                1：被攻击者健在
                2: 被攻击者死亡
                3: 被攻击者死亡，攻击者升级

            attacked_person_losed_health:int
            }
        @rtype: dict
        """

        result_dic = {"attack_result":0,"attack_person_losed_health":0,"attacked_person_losed_health":0}

        if attacked_person.attrs[is_die_str_g] == 1:
            result_dic["attack_result"] = "0"
            return result_dic
        elif attack_person.attrs[is_die_str_g] == 1:
            result_dic["attack_result"] = "-1"
            return result_dic

#        print attack_force[0]
#        print attack_person.attrs[min_attack_force_str_g],attack_person.attrs[max_attack_force_str_g]
        if attack_person.attrs[min_attack_force_str_g] == attack_person.attrs[max_attack_force_str_g] or attack_person.attrs[min_attack_force_str_g] > attack_person.attrs[max_attack_force_str_g]:
            attack_force = attack_person.attrs[min_attack_force_str_g]
        else:
           attack_force = random.randint(attack_person.attrs[min_attack_force_str_g],attack_person.attrs[max_attack_force_str_g])

        attacked_person_losed_health = attack_force - attacked_person.attrs[defensive_str_g]
        if attacked_person_losed_health < 0:
            attacked_person_losed_health = 0
        attacked_person.attrs[health_str_g] -= attacked_person_losed_health
        result_dic["attacked_person_losed_health"] = attacked_person_losed_health

        if attacked_person.check_die():
            attack_person.attrs[experience_str_g] +=  attacked_person.attrs[die_experience_str_g]
            attack_person.attrs[gold_str_g] +=  attacked_person.attrs[die_gold_str_g]
            if attack_person.check_up_level():
                 result_dic["attack_result"] = "3"
            else:
                 result_dic["attack_result"] = "2"
        else:
             result_dic["attack_result"] = "1"

        return result_dic

    def attack2die(self,attacked_person):

        attack_count = 0
        is_die = False
        attacked_is_die = False
        lose_health = 0
        attacked_lose_health = 0 # 被攻击者掉的血量
        is_up_level = False
        no_die = True # 无人死亡
#        attacked_is_up_level = False

        while attack_count <= self.attack2die_limit_count:
            attack_result_dic = self._attack(self,attacked_person)
#            print attack_result_dic
            if attack_result_dic["attack_result"] == "-1":
                is_die = True
                break
            elif attack_result_dic["attack_result"] == "0":
                attacked_is_die = True
                break
            elif attack_result_dic["attack_result"] == "3":
                attacked_is_die = False
                is_up_level = True

            attack_count += 1
            attacked_lose_health += attack_result_dic["attacked_person_losed_health"]

            attacked_result_dic = attacked_person._attack(attacked_person,self)
            lose_health += attacked_result_dic["attacked_person_losed_health"]
        if attack_count >= self.attack2die_limit_count:
            no_die = True
        else:
            no_die = False
        result = {"attack_count":attack_count, "is_die": is_die, "attacked_is_die": attacked_is_die, "lose_health":lose_health, "attacked_lose_health": attacked_lose_health, "is_up_level": is_up_level, "no_die":no_die}
        return result
        
    def check_die(self):

        if self.attrs[health_str_g] < 0:
            self.attrs[is_die_str_g] = 1
            self.attrs[health_str_g] = 0
            """
            if self.attrs[gold_str_g] < self.attrs[die_gold_str_g]:
                self.attrs[gold_str_g] -= self.attrs[die_gold_str_g]
            """

            return True
        else:
            return False

    

    def use_goods(self,goods_tag,num):
        """
        @param goods_tag: 
        @type: str
        @return -1: not have the goods
        @return -2: not enough num
        @return -3: num is too large
        @return 0: use success
        """

        if num > 500:
            return -3

        goods_tag_list = [goods[0] for goods in self.goods_list]
#        print goods_tag_list
        if goods_tag not in goods_tag_list:
            return -1
         
        things_tag_list = [thing[0] for thing in self.things_list]
        thing_index = things_tag_list.index(goods_tag)
        thing = self.things_list[thing_index]
        if thing[1] < num:
            return -2
        self.reduce_goods(thing[0],num)
        
        
#        print things_funcs.things_funcs_dic
        for i in range(num):
            things_funcs.things_funcs_dic[goods_tag](self)
#        self.save()
        return 0

    def add_goods(self,goods_tag,num,category_name):
        """
        @param category: "equip_category" equip_category_str_g, "goods" goods_category_str_g
        """
        """
        print category_name
        if category == equip_category_str_g:
            self.
        elif category == goods_category_str_g:
        """

#        print self.things_list
        things_tag_list = [thing[0] for thing in self.things_list]
#        print things_tag_list
        if goods_tag in things_tag_list:
        
            index = things_tag_list.index(goods_tag)
            self.things_list[index][1] += num
        else:
            self.things_list.append([goods_tag,num,category_name])

        self.sorting_knapsack()
        self.unwield()
        self.dress_equip()

#        print self.things_list
#        self.save()
#        print self.things_list

    def reduce_goods(self,goods_tag,num):
        """
        @return -1: the goods not exist
        @return -2: the num not enough
        @return 0: reduce success
        """

        things_tag_list = [thing[0] for thing in self.things_list]
        if not things_tag_list.count(goods_tag):
            return -1
        thing_index = things_tag_list.index(goods_tag)
        if self.things_list[thing_index][1] < num:
            return -2
        self.things_list[thing_index][1] -= num
#        print self.things_list[thing_index][1]
#        self.save()
        if self.things_list[thing_index][1] <= 0:
            self.things_list.pop(thing_index)
            knapsack.del_thing(self.attrs[tag_str_g],goods_tag)

        self.sorting_knapsack()
        self.unwield()
        self.dress_equip()

#            print self.things_list
#            print self.equip_list
        return 0

    def use_magic(self,magic_obj,aim_person):
        """
        @return -2: the mana not enough
        """
        magics_funcs_dic = magics_funcs.magics_funcs_dic

        magic = magic_obj
        
        if self.attrs[mana_str_g] < magic.attrs[mana_str_g]:
            return -2
        self.attrs[mana_str_g] -= magic.attrs[mana_str_g]
#        self.save()
        result = magics_funcs_dic[magic.attrs[tag_str_g]](self,aim_person)
#        self.save()
#        aim_person.save()
        return result

    def add_magic(self,magic_tag,num=1):
        """
        @return -2: magic is haven
        @return -1: magic is not exist
        @return 0: add success
        """
        
        things_tag_list = [thing[0] for thing in self.things_list if thing[2] == magic_category_str_g]
        if magic_tag in things_tag_list:
            return -2
#        print magics_funcs.magics_funcs_dic
        if not magics_funcs.magics_funcs_dic.has_key(magic_tag):
            return -1
        
        self.things_list.append([magic_tag,num,magic_category_str_g])
        self.sorting_knapsack()
        return 0

    def save(self):

        self.unwield()
        super(PersonBase,self).save()
        self.save_knapsack()
        self.init_all()

    def resurgence(self):

        self.attrs[is_die_str_g] = 0
        self.attrs[health_str_g] = self.attrs[health_limit_str_g]
        self.attrs[mana_str_g] = self.attrs[mana_limit_str_g]
#        self.save()

if "__main__" == __name__:

    test = PersonBase("q")
    print test.attrs
    print test.things_list
    print test.get_things_num()
#    print test.equip_list
#    print test.goods_list
#    test.attrs[experience_str_g] = 100
#    print test.check_up_level()
#    print test.attrs[experience_str_g]
#    print test.check_up_level()
#    print test.attrs[experience_str_g]

    test2 = PersonBase("q2")
#    print store.shop_goods(test2,hlth_wt_w_tag_str_g)
#    print test2.use_goods(hlth_wt_w_tag_str_g)
#    print test.use_goods(hlth_wt_w_tag_str_g)
#    for i in range(3):
#        pass
#        print test.attack(test2)
#        print test.attrs
#        print test2.attrs[health_str_g]
#        print test2.check_die()
