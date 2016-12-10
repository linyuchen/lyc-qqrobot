# -*- coding:UTF-8 -*-

import db_server
from rpg_global_values import *

sqlite = db_server.sqlite

class KnapsackBase(object):

    def __init__(self):
        
        sql_string = "create table if not exists %s(user_tag text PRIMARY KEY,thing_tag text,num integer default 0,category text)"%(knapsack_table_name_str_g)
        sqlite.non_query(sql_string)

    """
    def get_goods_category(self,ting_tag):

        category = None
        if thing_tag in goods_category_list_g:
            category = goods_category_str_g

        return category
    """

    def read(self,person_tag):

        sql_string = "select thing_tag,num,category from %s where user_tag = '%s'"%(knapsack_table_name_str_g,person_tag)
        result = sqlite.query(sql_string)
#        print result

        return map(list,result)

    """
    def add_thing(self,peron_tag,goods_tag,num):

        sql_string = "select num from %s where user_tag = '%s' and goods_tag = '%s'"%(knapsack_table_name_str_g,person_tag,goods_tag)
        result = sqlite.query(sql_string)
        if result:
            num = result[0][0] + num
        
        sql_string = "replace into %s(user_tag,goods_tag,num,category) values('%s','%s',%d,'%s')"%(peron_tag,goods_tag,num,self.get_goods_category(goods_tag))
            
        sqlite.non_query(sql_string)
    """

    def save(self,person_tag,things_list):
        """
        @param goods_list: [[thing_tag,num,category]...]
        """

#        print things_list
        for thing in things_list:

            sql_string = "select * from %s where user_tag='%s' and thing_tag='%s'"%(knapsack_table_name_str_g,person_tag,thing[0])
            if sqlite.query(sql_string):
                sql_string = "update %s set num=%d where user_tag='%s' and thing_tag='%s'"%(knapsack_table_name_str_g,thing[1],person_tag,thing[0])
                sqlite.non_query(sql_string)
            else:
                sql_string = "insert into %s(user_tag,thing_tag,num,category) values('%s','%s',%d,'%s')"%(knapsack_table_name_str_g,person_tag,thing[0],thing[1],thing[2])
#                print sql_string
            
                sqlite.non_query(sql_string)

    def del_thing(self,person_tag,thing_tag):

        sql_string = "delete from %s where user_tag = '%s' and thing_tag = '%s'"%(knapsack_table_name_str_g, person_tag, thing_tag)
        sqlite.non_query(sql_string)










