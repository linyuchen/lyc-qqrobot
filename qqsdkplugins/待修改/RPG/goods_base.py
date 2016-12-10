# -*- coding: UTF-8 -*-


import db_server
from things_base import *
sqlite = db_server.sqlite

all_goods_dic = {}



class GoodsBase(ThingsBase):

    def __init__(self,tag):

        super(GoodsBase,self).__init__(tag)

        self.table_name = goods_table_name_str_g
        self.attrs[category_str_g] = ""
#        self.create_table()
        self.read()

sql_string = "select tag from %s"%(goods_table_name_str_g)
result = sqlite.query(sql_string)
#print result
for goods_tag in result:
    goods_tag = goods_tag[0]
    all_goods_dic[goods_tag] = GoodsBase(goods_tag)

#print all_goods_dic


if "__main__" == __name__:


    test = GoodsBase("goods_test")
    #test.save()
