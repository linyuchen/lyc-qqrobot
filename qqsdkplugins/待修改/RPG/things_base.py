<<<<<<< HEAD:qqsdkplugins/待修改/RPG/things_base.py
#coding=UTF8

import db_server
from rpg_global_values import *


class ThingsBase(object):

    def __init__(self,tag):

        self.use_excepted_attr_list = [tag_str_g,"id",summary_str_g,price_str_g]
        self.attrs = {tag_str_g: tag, 
                name_str_g: " ", 
                experience_str_g: 0,
                health_str_g: 20, 
                health_limit_str_g: 20,
                mana_str_g: 5, 
                mana_limit_str_g: 5, 
                min_attack_force_str_g: 4,
                max_attack_force_str_g: 8,
                defensive_str_g: 0, 
                price_str_g: 0, 
                summary_str_g: u" "}

        self.attrs[level_str_g] = 1

        self.table_name = " "

        self.db_server = db_server.Server(thing=self)

    def set_attr(self,attr_key,attr_value):

        self.attrs[arrt_key] = arrt_value

    def read(self):

        self.db_server.read()

    def save(self):

        self.db_server.save()

    def create_table(self):

        self.db_server.create_table()

if __name__ == "__main__":

    test = Things("test_tag")
    test.attrs["table_name"] = "t_person"
    test.create_table()


=======
#coding=UTF8

import db_server
from rpg_global_values import *


class ThingsBase(object):

    def __init__(self,tag):

        self.use_excepted_attr_list = [tag_str_g,"id",summary_str_g,price_str_g]
        self.attrs = {tag_str_g: tag, 
                name_str_g: " ", 
                experience_str_g: 0,
                health_str_g: 20, 
                health_limit_str_g: 20,
                mana_str_g: 5, 
                mana_limit_str_g: 5, 
                min_attack_force_str_g: 4,
                max_attack_force_str_g: 8,
                defensive_str_g: 0, 
                price_str_g: 0, 
                summary_str_g: u" "}

        self.attrs[level_str_g] = 1

        self.table_name = " "

        self.db_server = db_server.Server(thing=self)

    def set_attr(self,attr_key,attr_value):

        self.attrs[arrt_key] = arrt_value

    def read(self):

        self.db_server.read()

    def save(self):

        self.db_server.save()

    def create_table(self):

        self.db_server.create_table()

if __name__ == "__main__":

    test = Things("test_tag")
    test.attrs["table_name"] = "t_person"
    test.create_table()


>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/RPG/things_base.py
