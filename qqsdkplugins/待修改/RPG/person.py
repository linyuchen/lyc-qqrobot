<<<<<<< HEAD:qqsdkplugins/待修改/RPG/person.py
#-*- coding: UTF-8 -*-

import goods_base
import person_base
import store
from rpg_global_values import *

store = store.Store()

class Person(person_base.PersonBase):

    def __init__(self,tag):

        super(Person,self).__init__(tag)
        self.level_list = [(u"初学弟子",1),(u"初入江湖",10),(u"江湖新秀",20),(u"江湖少侠",30),(u"江湖大侠",40),(u"江湖豪侠",50),(u"一派掌门 ",60),(u"一代宗师 ",70),(u"武林盟主",80),(u"独孤求败",90),(u"隐退江湖",100)]
#        PersonBase.__init__(self,tag)
        self.resurgence_gold = 10


    """
    def get_knapsack(self,ktype):
#        @param: ktype:背包类型，"goods" ,"equip"
#        @type: string
#        @return: 背包内容
#        @rtype: string

        super(Person,self).read_knapsack()
        if "goods" == ktype:
            result = u"我的物品:\n"
            things_list = self.goods_list
        elif "equip" == ktype:
            result = u"我的装备:\n"
            things_list = self.equip_list
        elif category == "m":
            things_list = self.magic_list
            result = u"我的技能：\n"
        for thing in things_list:
            thing_name = GoodsBase(thing[0])
            result += "%s,数量%d\n"%(thing[-1])
       
        return result
    """

    def attack(self,attacked_person):

        attack_result = super(Person,self).attack(attacked_person)
        if attack_result["attack_result"] == "-1":
            result = u"【%s】您已经死掉了，无法进行攻击"%self.attrs[name_str_g]
        elif attack_result["attack_result"] == "0":
            result = u"【%s】已经早就死翘翘了，你还攻击他，那么喜欢鞭尸呀！"%attacked_person.attrs[name_str_g]
        elif attack_result["attack_result"] in ["1","2","3"]:
            result = u"【%s】对【%s】进行攻击，【%s】失去了%d点血"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],attacked_person.attrs[name_str_g],attack_result["attacked_person_losed_health"])
            if attack_result["attack_result"] in ["2","3"]:
                result += u"\n【%s】死亡！【%s】获得了%d点经验值"%(attacked_person.attrs[name_str_g],self.attrs[name_str_g],attacked_person.attrs[die_experience_str_g])
                result += u"，%d%s"%(self.attrs[die_gold_str_g],currency_name_str_g)
            if attack_result["attack_result"] == "3":
                result += u"\n恭喜【%s】升级了~"%(self.attrs[name_str_g])
        return result, attack_result["attack_result"]


    def attack2die(self,attacked_person):

        result = super(Person,self).attack2die(attacked_person)
        """
        result = {"attack_count":attack_count, "is_die": is_die, "attacked_is_die": attacked_is_die, "lose_health":lose_health, "attacked_lose_health": attacked_lose_health, "is_up_level": is_up_level, "no_die":no_die}
        """

        return_result = u"【%s】与【%s】一共对打了%d次\n"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],result["attack_count"])
        return_result += u"【%s】失去了%d血\n"%(self.attrs[name_str_g],result["lose_health"])
        return_result += u"【%s】失去了%d血\n"%(attacked_person.attrs[name_str_g],result["attacked_lose_health"])
        if result["is_die"]:
            return_result += u"【%s】死亡,【%s】获得了%d经验，%s金币\n"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],self.attrs[die_experience_str_g],self.attrs[die_gold_str_g])
        elif result["attacked_is_die"]:
            return_result += u"【%s】死亡,【%s】获得了%d经验，%s金币\n"%(attacked_person.attrs[name_str_g],self.attrs[name_str_g],attacked_person.attrs[die_experience_str_g],attacked_person.attrs[die_gold_str_g])
            if result["is_up_level"]:
                return_result += u"恭喜【%s】升级了！\n"%(self.attrs[name_str_g])

        if result["no_die"]:
            return_result += u"这两个家伙的实力似乎旗鼓相当呐！,两位都坚挺的活了下来！\n"

        return return_result

    
    def get_state(self):

        result = u"【%s】的状态：\n"%(self.attrs[name_str_g])
        result += u"%s：%d\n"%(currency_name_str_g,self.attrs[gold_str_g])
        result += u"生命值：%d/%d,"%(self.attrs[health_str_g],self.attrs[health_limit_str_g])
        result += u"魔法值：%d/%d\n"%(self.attrs[mana_str_g],self.attrs[mana_limit_str_g])
        result += u"攻击力：%d ~ %d"%(self.attrs[min_attack_force_str_g],self.attrs[max_attack_force_str_g])
        result += u",防御力：%d\n"%(self.attrs[defensive_str_g])
        level = self.attrs[level_str_g]
        level_name = self.get_level_name(level)
        result += u"当前等级：%d (%s)\n"%(level, level_name)
        result += u"经验值：%d/%d\n"%(self.attrs[experience_str_g],self.attrs[up_experience_str_g])

        return result
    
    def get_level_name(self,level):
        
        level_name = ""
        for i in self.level_list:
            if level >= i[1]:
                level_name = i[0]
            else:
                break
        return level_name
            

    def use_goods(self,goods_name,num):

        use_failed = u"【%s】没有此道具，无法使用"%(self.attrs[name_str_g])
        goods_tag = store.get_goods_tag_by_name(goods_name)
        if not goods_tag:
            return use_failed

        use_result = super(Person,self).use_goods(goods_tag,num)
        goods = goods_base.all_goods_dic[goods_tag]

        if 0 == use_result:
            result = u"【%s】使用了%s"%(self.attrs[name_str_g],goods.attrs[name_str_g])
            return result
        elif -1 == use_result:
            return use_failed
        elif -2 == use_result:
            return u"【%s】的 %s 不足 %d，使用失败"%(self.attrs[name_str_g],goods.attrs[name_str_g],num)
        elif -3 == use_result:
            return u"使用物品数量太大，无法使用！"


    def get_things_list(self,category):
        """
        @param category:"g" goods, "e" equip, "m" magic
        """

        things_list = []
        if category == "g":
            things_list = self.goods_list
            result = u"物品栏：\n"
        elif category == "e":
            things_list = self.equip_list
            result = u"装备栏：\n"
        elif category == "m":
            things_list = self.magic_list
            result = u"我的技能：\n"

        for thing in things_list:
            # thing = [tag,num,category]
            thing_tag = thing[0]
            thing_name = goods_base.all_goods_dic[thing_tag].attrs[name_str_g]
            result += u"【%s】数量：%d\n"%(thing_name,thing[1])

        return result

    def resurgence(self):

        if self.attrs[is_die_str_g] == 0:

            return u"麻烦您先死掉再来复活，OK？"

        need_gold = self.resurgence_gold * self.attrs[level_str_g]

        if self.attrs[gold_str_g] < need_gold:
            return u"【%s】的%s不足%d，无法复活"%(self.attrs[name_str_g], currency_name_str_g, need_gold)
        super(Person,self).resurgence()
        self.attrs[gold_str_g] -= need_gold

        return u"【%s】已经复活！"%(self.attrs[name_str_g])

    def use_magic(self,magic_name,aim_person):

        magic_tag = store.get_goods_tag_by_name(magic_name)
        error = u"抱歉，您没有 %s 这项技能"%(magic_name)
        if not magic_tag:
            return error

        magic_tag_list = [magic[0] for magic in self.magic_list]
#        print magic_tag_list
        if magic_tag not in magic_tag_list:
#            print magic_tag
#            print "magic not in "
            return error
        magic_obj = goods_base.all_goods_dic[magic_tag]
        result = super(Person,self).use_magic(magic_obj,aim_person)
        if result == -2:
            return u"魔法值不够，无法使用 %s 这项技能"%(magic_name)

        return result
            




if "__main__" == __name__:

    p1 = Person("q2")
    p2 = Person("q")
    print p1.get_state()
    print p2.get_state()
    print p1.get_things_list("g")
    print p1.get_things_list("e")
    
#    p1.resurgence()
#    p2.resurgence()
#    print p1.get_knapsack(ktype="goods")
    for i in range(7):
#        print p1.attack(p2)
#        print u"\n【%s】反击："%(p2.attrs[name_str_g])
        print p2.attack(p1)[1]


=======
#-*- coding: UTF-8 -*-

import goods_base
import person_base
import store
from rpg_global_values import *

store = store.Store()

class Person(person_base.PersonBase):

    def __init__(self,tag):

        super(Person,self).__init__(tag)
        self.level_list = [(u"初学弟子",1),(u"初入江湖",10),(u"江湖新秀",20),(u"江湖少侠",30),(u"江湖大侠",40),(u"江湖豪侠",50),(u"一派掌门 ",60),(u"一代宗师 ",70),(u"武林盟主",80),(u"独孤求败",90),(u"隐退江湖",100)]
#        PersonBase.__init__(self,tag)
        self.resurgence_gold = 10


    """
    def get_knapsack(self,ktype):
#        @param: ktype:背包类型，"goods" ,"equip"
#        @type: string
#        @return: 背包内容
#        @rtype: string

        super(Person,self).read_knapsack()
        if "goods" == ktype:
            result = u"我的物品:\n"
            things_list = self.goods_list
        elif "equip" == ktype:
            result = u"我的装备:\n"
            things_list = self.equip_list
        elif category == "m":
            things_list = self.magic_list
            result = u"我的技能：\n"
        for thing in things_list:
            thing_name = GoodsBase(thing[0])
            result += "%s,数量%d\n"%(thing[-1])
       
        return result
    """

    def attack(self,attacked_person):

        attack_result = super(Person,self).attack(attacked_person)
        if attack_result["attack_result"] == "-1":
            result = u"【%s】您已经死掉了，无法进行攻击"%self.attrs[name_str_g]
        elif attack_result["attack_result"] == "0":
            result = u"【%s】已经早就死翘翘了，你还攻击他，那么喜欢鞭尸呀！"%attacked_person.attrs[name_str_g]
        elif attack_result["attack_result"] in ["1","2","3"]:
            result = u"【%s】对【%s】进行攻击，【%s】失去了%d点血"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],attacked_person.attrs[name_str_g],attack_result["attacked_person_losed_health"])
            if attack_result["attack_result"] in ["2","3"]:
                result += u"\n【%s】死亡！【%s】获得了%d点经验值"%(attacked_person.attrs[name_str_g],self.attrs[name_str_g],attacked_person.attrs[die_experience_str_g])
                result += u"，%d%s"%(self.attrs[die_gold_str_g],currency_name_str_g)
            if attack_result["attack_result"] == "3":
                result += u"\n恭喜【%s】升级了~"%(self.attrs[name_str_g])
        return result, attack_result["attack_result"]


    def attack2die(self,attacked_person):

        result = super(Person,self).attack2die(attacked_person)
        """
        result = {"attack_count":attack_count, "is_die": is_die, "attacked_is_die": attacked_is_die, "lose_health":lose_health, "attacked_lose_health": attacked_lose_health, "is_up_level": is_up_level, "no_die":no_die}
        """

        return_result = u"【%s】与【%s】一共对打了%d次\n"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],result["attack_count"])
        return_result += u"【%s】失去了%d血\n"%(self.attrs[name_str_g],result["lose_health"])
        return_result += u"【%s】失去了%d血\n"%(attacked_person.attrs[name_str_g],result["attacked_lose_health"])
        if result["is_die"]:
            return_result += u"【%s】死亡,【%s】获得了%d经验，%s金币\n"%(self.attrs[name_str_g],attacked_person.attrs[name_str_g],self.attrs[die_experience_str_g],self.attrs[die_gold_str_g])
        elif result["attacked_is_die"]:
            return_result += u"【%s】死亡,【%s】获得了%d经验，%s金币\n"%(attacked_person.attrs[name_str_g],self.attrs[name_str_g],attacked_person.attrs[die_experience_str_g],attacked_person.attrs[die_gold_str_g])
            if result["is_up_level"]:
                return_result += u"恭喜【%s】升级了！\n"%(self.attrs[name_str_g])

        if result["no_die"]:
            return_result += u"这两个家伙的实力似乎旗鼓相当呐！,两位都坚挺的活了下来！\n"

        return return_result

    
    def get_state(self):

        result = u"【%s】的状态：\n"%(self.attrs[name_str_g])
        result += u"%s：%d\n"%(currency_name_str_g,self.attrs[gold_str_g])
        result += u"生命值：%d/%d,"%(self.attrs[health_str_g],self.attrs[health_limit_str_g])
        result += u"魔法值：%d/%d\n"%(self.attrs[mana_str_g],self.attrs[mana_limit_str_g])
        result += u"攻击力：%d ~ %d"%(self.attrs[min_attack_force_str_g],self.attrs[max_attack_force_str_g])
        result += u",防御力：%d\n"%(self.attrs[defensive_str_g])
        level = self.attrs[level_str_g]
        level_name = self.get_level_name(level)
        result += u"当前等级：%d (%s)\n"%(level, level_name)
        result += u"经验值：%d/%d\n"%(self.attrs[experience_str_g],self.attrs[up_experience_str_g])

        return result
    
    def get_level_name(self,level):
        
        level_name = ""
        for i in self.level_list:
            if level >= i[1]:
                level_name = i[0]
            else:
                break
        return level_name
            

    def use_goods(self,goods_name,num):

        use_failed = u"【%s】没有此道具，无法使用"%(self.attrs[name_str_g])
        goods_tag = store.get_goods_tag_by_name(goods_name)
        if not goods_tag:
            return use_failed

        use_result = super(Person,self).use_goods(goods_tag,num)
        goods = goods_base.all_goods_dic[goods_tag]

        if 0 == use_result:
            result = u"【%s】使用了%s"%(self.attrs[name_str_g],goods.attrs[name_str_g])
            return result
        elif -1 == use_result:
            return use_failed
        elif -2 == use_result:
            return u"【%s】的 %s 不足 %d，使用失败"%(self.attrs[name_str_g],goods.attrs[name_str_g],num)
        elif -3 == use_result:
            return u"使用物品数量太大，无法使用！"


    def get_things_list(self,category):
        """
        @param category:"g" goods, "e" equip, "m" magic
        """

        things_list = []
        if category == "g":
            things_list = self.goods_list
            result = u"物品栏：\n"
        elif category == "e":
            things_list = self.equip_list
            result = u"装备栏：\n"
        elif category == "m":
            things_list = self.magic_list
            result = u"我的技能：\n"

        for thing in things_list:
            # thing = [tag,num,category]
            thing_tag = thing[0]
            thing_name = goods_base.all_goods_dic[thing_tag].attrs[name_str_g]
            result += u"【%s】数量：%d\n"%(thing_name,thing[1])

        return result

    def resurgence(self):

        if self.attrs[is_die_str_g] == 0:

            return u"麻烦您先死掉再来复活，OK？"

        need_gold = self.resurgence_gold * self.attrs[level_str_g]

        if self.attrs[gold_str_g] < need_gold:
            return u"【%s】的%s不足%d，无法复活"%(self.attrs[name_str_g], currency_name_str_g, need_gold)
        super(Person,self).resurgence()
        self.attrs[gold_str_g] -= need_gold

        return u"【%s】已经复活！"%(self.attrs[name_str_g])

    def use_magic(self,magic_name,aim_person):

        magic_tag = store.get_goods_tag_by_name(magic_name)
        error = u"抱歉，您没有 %s 这项技能"%(magic_name)
        if not magic_tag:
            return error

        magic_tag_list = [magic[0] for magic in self.magic_list]
#        print magic_tag_list
        if magic_tag not in magic_tag_list:
#            print magic_tag
#            print "magic not in "
            return error
        magic_obj = goods_base.all_goods_dic[magic_tag]
        result = super(Person,self).use_magic(magic_obj,aim_person)
        if result == -2:
            return u"魔法值不够，无法使用 %s 这项技能"%(magic_name)

        return result
            




if "__main__" == __name__:

    p1 = Person("q2")
    p2 = Person("q")
    print p1.get_state()
    print p2.get_state()
    print p1.get_things_list("g")
    print p1.get_things_list("e")
    
#    p1.resurgence()
#    p2.resurgence()
#    print p1.get_knapsack(ktype="goods")
    for i in range(7):
#        print p1.attack(p2)
#        print u"\n【%s】反击："%(p2.attrs[name_str_g])
        print p2.attack(p1)[1]


>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/RPG/person.py
