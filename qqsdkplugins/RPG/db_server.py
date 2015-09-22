#coding=UTF-8

import sys
import os
cur_path = os.path.dirname(__file__)
cur_path = cur_path or "."
sys.path.append(cur_path + "/../sqlite_sserver/")

import sqlite_db_config
import sqliteSclient

from rpg_global_values import *
from global_values import *
import rpg_global_values
#print dir(rpg_global_values)


#sqlite = sqliteserver.Sqlite_Safe(rpg_global_values.db_path_str_g)
sqlite = sqliteSclient.Sqlite(sqlite_db_config.sqlite_server, sqlite_db_config.sqlite_port, sqlite_db_config.rpgdb_name)

class Server(object):

    def __init__(self,thing=None):

        self.thing = thing
        
    def set_thing(self,thing):

        self.thing = thing


    def convert_py_obj2sql_obj(self,obj):

        if isinstance(obj,str) or isinstance(obj,unicode):
            return "'%s'"%obj
        elif isinstance(obj,float):
            return "%f"%obj
        elif isinstance(obj,int) or isinstance(obj,long):
            return "%d"%obj
        else:
            return "' '"

    def save(self):

        keys = self.thing.attrs.keys()
        values = self.thing.attrs.values()

        set_string = ",".join(["%s=?"%(key) for key in keys])
        insert_keys_string = ",".join(keys)
        insert_values_string = ",".join("?" * len(values))
#        print insert_keys_string
        values_tuple = tuple(map(unicode,values))
#        print values_tuple

        sql_string = "SELECT * FROM %s WHERE tag = '%s'"%(self.thing.table_name,self.thing.attrs[tag_str_g])

        result = sqlite.query(sql_string)
        if result:
            sql_string = "update %s set %s where tag='%s'"%(self.thing.table_name,set_string,self.thing.attrs[tag_str_g])
        else:
            sql_string = "insert into %s(%s) values(%s)"%(self.thing.table_name,insert_keys_string,insert_values_string)

#        print sql_string

        sqlite.non_query(sql_string,values_tuple)


    def read(self):

        
#        print self.thing.attrs[tag_str_g]
        for key in self.thing.attrs.keys():
#            print key
            sql_string = "select %s from %s where tag='%s'"%(key,self.thing.table_name,self.thing.attrs[tag_str_g])
#            print sql_string
            result = sqlite.query(sql_string)
            if not result:
#                print "No exists"
                break
#            print type(result[0][0])
            value = result[0][0]
#            print type(value), value
#            print value
            if key == "gold": # 由于数字很大，所以用字符串的形式保存
#                print value
                value = int(eval(value))
#                print value
            self.thing.attrs[key] = value


    def create_table(self):

        if self.thing:
            column = ",".join(self.thing.attrs.keys())
#            print column
            sql_string = "CREATE TABLE IF NOT EXISTS %s(id integer primary key autoincrement,%s)"%(self.thing.table_name,column)
#            print sql_string
            sqlite.non_query(sql_string)
