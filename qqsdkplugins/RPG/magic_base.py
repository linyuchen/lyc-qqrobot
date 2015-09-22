# -*- coding: UTF-8 -*-


from things_base import *

class MagicBase(ThingsBase):

    def __init__(self,tag):

        super(GoodsBase,self).__init__(tag)

        self.table_name = magic_table_name_str_g
        self.attrs[category_str_g] = ""
#        self.create_table()
        self.read()


if "__main__" == __name__:

    test = Goods("goods_test")
    test.save()
