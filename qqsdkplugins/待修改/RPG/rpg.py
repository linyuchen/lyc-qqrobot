<<<<<<< HEAD:qqsdkplugins/待修改/RPG/rpg.py
#coding=UTF8

import random
import sys

rpg_path = ".."
sys.path.append(rpg_path)
#sys.path.append("../myclass")

import store
import db_server
from person import Person
from rpg_global_values import *
sqlite = db_server.sqlite
store = store.Store()

class RPG:

    def __init__(self):

        RPG.persons = {}
        self.current_person = None
        self.not_exist_person_error = u"没有找到【%s】这个人"

        self.monster_dic = {"mouse":u"嗜血老鼠",u"bat":u"吸血蝙蝠","die_knight":u"亡灵骑士","devil":u"无踪恶魔","forest_hunter":u"森林猎人","inkfish":u"会飞的乌贼","crazy_susiliks":u"疯狂的地鼠","goblin":u"地精", u"slime": u"史莱姆", u"bear":u"迷你熊"}

        self.current_person = None

    def get_person(self,person_tag):

        """
        if RPG.persons.has_key(person_tag):
            person = RPG.persons[person_tag]
        else:
            person = Person(person_tag)

            RPG.persons[person_tag] = person
        """
        person = Person(person_tag)

        return person

    def create_person(self,person_tag,person_name):

        if not self.exist_person(person_tag):
            person = Person(person_tag)
            person.attrs[name_str_g] = person_name
            person.save()

    def change_current_person(self, person_tag, name):

        self.current_person = self.get_person(person_tag)
        self.current_person.attrs[name_str_g] = name
#        self.current_person = Person(person_tag)
    
    def use_magic(self,param):
        
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = param.split()
        magic_name = param[0]
        if len(param) < 2:
            aim_person_tag = self.current_person.attrs[tag_str_g]
        else:
            aim_person_tag = param[1]

        if not self.exist_person(aim_person_tag):
            return self.not_exist_person_error % aim_person_tag
        
        aim_person = self.get_person(aim_person_tag)
        result = self.current_person.use_magic(magic_name,aim_person)
        self.current_person.save()
        if aim_person_tag != self.current_person.attrs[tag_str_g]:
            aim_person.save()

        return result

    def __check_attacked_person_by_tag(self,person_tag):

        if not self.exist_person(person_tag):
            return self.not_exist_person_error % person_tag
        if person_tag == self.current_person.attrs[tag_str_g]:
            return u"自己攻击自己，【%s】你有病啊！+_+"%(self.current_person.attrs[name_str_g])


    def attack(self,person_tag):

        check_result = self.__check_attacked_person_by_tag(person_tag)
        if check_result:
            return check_result

        attacked_person = self.get_person(person_tag)
        return_result = ""
        attack_result = self.current_person.attack(attacked_person)
        return_result += attack_result[0]
        if attack_result[1] not in ["-1","0"]:
            attacked_result = attacked_person.attack(self.current_person)[0]
            return_result += u"\n\n【%s】反击：\n"%(attacked_person.attrs[name_str_g])
            return_result += attacked_result

        self.current_person.save()
        attacked_person.save()

        return return_result

    def attack2die(self,person_tag):

        check_result = self.__check_attacked_person_by_tag(person_tag)
        if check_result:
            return check_result
        attacked_person = self.get_person(person_tag)
        if attacked_person.attrs[is_die_str_g]:
            return u"【%s】已经死亡了，就不要再虐人家了嘛~"%(attacked_person.attrs[name_str_g])
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】您已经挂掉了！快快去复活！"%(self.current_person.attrs[name_str_g])
        result = self.current_person.attack2die(attacked_person)
        self.current_person.save()
        attacked_person.save()
        return result


    def exist_person(self,person_tag):

        sql_string = "select * from %s where tag='%s'"%(person_table_name_str_g,person_tag)
        result = sqlite.query(sql_string)
        if not result:
            return False
        else:
            return True

    def __analys_param(self,param):
        """
        @return False: num is error
        @return: goods_name,num
        @rtype:tuple
        """
        param = param.split()
        goods_name = param[0]
        
        if len(param) < 2:
            num = 1
        else:
            num = param[1]
            if not num.isdigit():
                return False
            num = int(num)

        return goods_name,num
    
    def use_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 
        result = self.current_person.use_goods(param[0], param[1])
        self.current_person.save()

        return result

    def shop_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 

        result = store.shop_goods(self.current_person, param[0], param[1])
        self.current_person.save()

        return result

    def sell_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 

        result = store.sell_goods(self.current_person, param[0], param[1])
        self.current_person.save()
        
        return result
    
    def shop_magic(self,magic_name):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        result = store.shop_magic(self.current_person, magic_name)
        self.current_person.save()

        return result


    def get_state(self):

        return self.current_person.get_state()

    def get_knapsacks(self,knapsacks_type):
        """
        @param knapsacks_type: "g" goods, "e" equip, "m" magic
        """

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        result = self.current_person.get_things_list(knapsacks_type)

        return result

    def show_store_goods_list(self,category):
        """
        @param category: "g" goods, "e" equip, "m" magic
        """

        result = store.show_goods_list(category)

        return result



    def resurgence(self):

        result = self.current_person.resurgence()
        self.current_person.save()
        return result

    def get_living_person_list(self):

        sql_string = "select tag,name from %s where is_die = 0"%(person_table_name_str_g)
        result = sqlite.query(sql_string)
        living_list = []
        for i in result:
            living_list.append(i[0])

        return living_list

    def random_attack2die(self):

        living_list = self.get_living_person_list()
        current_tag = self.current_person.attrs[tag_str_g]
        if current_tag in living_list:
            living_list.remove(current_tag)
        if not living_list:
            return u"唉哟我去！这世界上除了你，都死光了！！！"
        aim_tag = random.choice(living_list)
#        print aim_tag
        result = self.attack2die(aim_tag)
        return result

    def leveling(self):
        
        percentage = random.choice([0.3,0.4,0.5,0.6,0.7,0.9,0.94,0.98,0.99,1,1.2,1.3])
        monster_tag = random.choice(self.monster_dic.keys())
        monster = Person(monster_tag)
        monster.attrs[name_str_g] = self.monster_dic[monster_tag]
        if self.current_person.attrs[max_attack_force_str_g] < self.current_person.attrs[defensive_str_g]:
            monster.attrs[max_attack_force_str_g] = int(self.current_person.attrs[defensive_str_g]) + self.current_person.attrs[min_attack_force_str_g]
            monster.attrs[min_attack_force_str_g] = self.current_person.attrs[min_attack_force_str_g]
            monster.attrs[defensive_str_g] = int(self.current_person.attrs[max_attack_force_str_g] * percentage)

        else:
            monster.attrs[max_attack_force_str_g] = int(self.current_person.attrs[max_attack_force_str_g] * percentage)
            monster.attrs[min_attack_force_str_g] = monster.attrs[max_attack_force_str_g]
            monster.attrs[defensive_str_g] = int(self.current_person.attrs[defensive_str_g] * percentage)
        monster.attrs[health_str_g] = self.current_person.attrs[health_limit_str_g] 
        monster.attrs[die_gold_str_g] = random.randint(10,self.current_person.attrs[die_gold_str_g])
        monster.attrs[die_experience_str_g] = random.randint(3,self.current_person.attrs[die_experience_str_g])
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】您已经挂掉了！快快去复活！"%(self.current_person.attrs[name_str_g])
        if random.random() < 0.5:
            result = self.current_person.attack2die(monster)
        else:
            result = monster.attack2die(self.current_person)
        self.current_person.save()
        return result

    def level_summary(self):

        result = u"争霸等级说明\n"

        for level in self.current_person.level_list:
            result += u"%s：%d级\n"%(level[0], level[1])

        return result

    def level_rank(self):

        sql_string = "select name,tag,level from %s order by level desc limit 10"%(person_table_name_str_g)

        level_list = sqlite.query(sql_string)
        result = ""
        rank = 1
        for i in level_list:
            result += u"第%d名【%s】(%s)等级·%d(%s)\n"%(rank,i[0],i[1],i[2],self.current_person.get_level_name(i[2]))
            rank += 1

        return result







if "__main__" == __name__:

    test = RPG()
#    test.change_current_person("p1","name")
    test.create_person("p1","name")
    test.get_person()
    print test.get_state()
#    print test.get_living_person_list()
#    print test.level_rank()
=======
#coding=UTF8

import random
import sys

rpg_path = ".."
sys.path.append(rpg_path)
#sys.path.append("../myclass")

import store
import db_server
from person import Person
from rpg_global_values import *
sqlite = db_server.sqlite
store = store.Store()

class RPG:

    def __init__(self):

        RPG.persons = {}
        self.current_person = None
        self.not_exist_person_error = u"没有找到【%s】这个人"

        self.monster_dic = {"mouse":u"嗜血老鼠",u"bat":u"吸血蝙蝠","die_knight":u"亡灵骑士","devil":u"无踪恶魔","forest_hunter":u"森林猎人","inkfish":u"会飞的乌贼","crazy_susiliks":u"疯狂的地鼠","goblin":u"地精", u"slime": u"史莱姆", u"bear":u"迷你熊"}

        self.current_person = None

    def get_person(self,person_tag):

        """
        if RPG.persons.has_key(person_tag):
            person = RPG.persons[person_tag]
        else:
            person = Person(person_tag)

            RPG.persons[person_tag] = person
        """
        person = Person(person_tag)

        return person

    def create_person(self,person_tag,person_name):

        if not self.exist_person(person_tag):
            person = Person(person_tag)
            person.attrs[name_str_g] = person_name
            person.save()

    def change_current_person(self, person_tag, name):

        self.current_person = self.get_person(person_tag)
        self.current_person.attrs[name_str_g] = name
#        self.current_person = Person(person_tag)
    
    def use_magic(self,param):
        
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = param.split()
        magic_name = param[0]
        if len(param) < 2:
            aim_person_tag = self.current_person.attrs[tag_str_g]
        else:
            aim_person_tag = param[1]

        if not self.exist_person(aim_person_tag):
            return self.not_exist_person_error % aim_person_tag
        
        aim_person = self.get_person(aim_person_tag)
        result = self.current_person.use_magic(magic_name,aim_person)
        self.current_person.save()
        if aim_person_tag != self.current_person.attrs[tag_str_g]:
            aim_person.save()

        return result

    def __check_attacked_person_by_tag(self,person_tag):

        if not self.exist_person(person_tag):
            return self.not_exist_person_error % person_tag
        if person_tag == self.current_person.attrs[tag_str_g]:
            return u"自己攻击自己，【%s】你有病啊！+_+"%(self.current_person.attrs[name_str_g])


    def attack(self,person_tag):

        check_result = self.__check_attacked_person_by_tag(person_tag)
        if check_result:
            return check_result

        attacked_person = self.get_person(person_tag)
        return_result = ""
        attack_result = self.current_person.attack(attacked_person)
        return_result += attack_result[0]
        if attack_result[1] not in ["-1","0"]:
            attacked_result = attacked_person.attack(self.current_person)[0]
            return_result += u"\n\n【%s】反击：\n"%(attacked_person.attrs[name_str_g])
            return_result += attacked_result

        self.current_person.save()
        attacked_person.save()

        return return_result

    def attack2die(self,person_tag):

        check_result = self.__check_attacked_person_by_tag(person_tag)
        if check_result:
            return check_result
        attacked_person = self.get_person(person_tag)
        if attacked_person.attrs[is_die_str_g]:
            return u"【%s】已经死亡了，就不要再虐人家了嘛~"%(attacked_person.attrs[name_str_g])
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】您已经挂掉了！快快去复活！"%(self.current_person.attrs[name_str_g])
        result = self.current_person.attack2die(attacked_person)
        self.current_person.save()
        attacked_person.save()
        return result


    def exist_person(self,person_tag):

        sql_string = "select * from %s where tag='%s'"%(person_table_name_str_g,person_tag)
        result = sqlite.query(sql_string)
        if not result:
            return False
        else:
            return True

    def __analys_param(self,param):
        """
        @return False: num is error
        @return: goods_name,num
        @rtype:tuple
        """
        param = param.split()
        goods_name = param[0]
        
        if len(param) < 2:
            num = 1
        else:
            num = param[1]
            if not num.isdigit():
                return False
            num = int(num)

        return goods_name,num
    
    def use_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 
        result = self.current_person.use_goods(param[0], param[1])
        self.current_person.save()

        return result

    def shop_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 

        result = store.shop_goods(self.current_person, param[0], param[1])
        self.current_person.save()

        return result

    def sell_goods(self,param):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        param = self.__analys_param(param)
        if not param:
            return u"数量有误！" 

        result = store.sell_goods(self.current_person, param[0], param[1])
        self.current_person.save()
        
        return result
    
    def shop_magic(self,magic_name):

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        result = store.shop_magic(self.current_person, magic_name)
        self.current_person.save()

        return result


    def get_state(self):

        return self.current_person.get_state()

    def get_knapsacks(self,knapsacks_type):
        """
        @param knapsacks_type: "g" goods, "e" equip, "m" magic
        """

        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】你已经死了，别诈尸做多余的事情"%(self.current_person.attrs[name_str_g])
        result = self.current_person.get_things_list(knapsacks_type)

        return result

    def show_store_goods_list(self,category):
        """
        @param category: "g" goods, "e" equip, "m" magic
        """

        result = store.show_goods_list(category)

        return result



    def resurgence(self):

        result = self.current_person.resurgence()
        self.current_person.save()
        return result

    def get_living_person_list(self):

        sql_string = "select tag,name from %s where is_die = 0"%(person_table_name_str_g)
        result = sqlite.query(sql_string)
        living_list = []
        for i in result:
            living_list.append(i[0])

        return living_list

    def random_attack2die(self):

        living_list = self.get_living_person_list()
        current_tag = self.current_person.attrs[tag_str_g]
        if current_tag in living_list:
            living_list.remove(current_tag)
        if not living_list:
            return u"唉哟我去！这世界上除了你，都死光了！！！"
        aim_tag = random.choice(living_list)
#        print aim_tag
        result = self.attack2die(aim_tag)
        return result

    def leveling(self):
        
        percentage = random.choice([0.3,0.4,0.5,0.6,0.7,0.9,0.94,0.98,0.99,1,1.2,1.3])
        monster_tag = random.choice(self.monster_dic.keys())
        monster = Person(monster_tag)
        monster.attrs[name_str_g] = self.monster_dic[monster_tag]
        if self.current_person.attrs[max_attack_force_str_g] < self.current_person.attrs[defensive_str_g]:
            monster.attrs[max_attack_force_str_g] = int(self.current_person.attrs[defensive_str_g]) + self.current_person.attrs[min_attack_force_str_g]
            monster.attrs[min_attack_force_str_g] = self.current_person.attrs[min_attack_force_str_g]
            monster.attrs[defensive_str_g] = int(self.current_person.attrs[max_attack_force_str_g] * percentage)

        else:
            monster.attrs[max_attack_force_str_g] = int(self.current_person.attrs[max_attack_force_str_g] * percentage)
            monster.attrs[min_attack_force_str_g] = monster.attrs[max_attack_force_str_g]
            monster.attrs[defensive_str_g] = int(self.current_person.attrs[defensive_str_g] * percentage)
        monster.attrs[health_str_g] = self.current_person.attrs[health_limit_str_g] 
        monster.attrs[die_gold_str_g] = random.randint(10,self.current_person.attrs[die_gold_str_g])
        monster.attrs[die_experience_str_g] = random.randint(3,self.current_person.attrs[die_experience_str_g])
        if self.current_person.attrs[is_die_str_g]:
            return u"【%s】您已经挂掉了！快快去复活！"%(self.current_person.attrs[name_str_g])
        if random.random() < 0.5:
            result = self.current_person.attack2die(monster)
        else:
            result = monster.attack2die(self.current_person)
        self.current_person.save()
        return result

    def level_summary(self):

        result = u"争霸等级说明\n"

        for level in self.current_person.level_list:
            result += u"%s：%d级\n"%(level[0], level[1])

        return result

    def level_rank(self):

        sql_string = "select name,tag,level from %s order by level desc limit 10"%(person_table_name_str_g)

        level_list = sqlite.query(sql_string)
        result = ""
        rank = 1
        for i in level_list:
            result += u"第%d名【%s】(%s)等级·%d(%s)\n"%(rank,i[0],i[1],i[2],self.current_person.get_level_name(i[2]))
            rank += 1

        return result







if "__main__" == __name__:

    test = RPG()
#    test.change_current_person("p1","name")
    test.create_person("p1","name")
    test.get_person()
    print test.get_state()
#    print test.get_living_person_list()
#    print test.level_rank()
>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/RPG/rpg.py
