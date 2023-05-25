# -*- encoding:UTF8 -*-

import os
from sqliteclient import Sqlite_Safe

class Dreams:

    def __init__(self):

        cur_path = os.path.dirname(__file__)
        self.cur_path = cur_path or "."
        self.DREAM_DB_PATH = cur_path + "/dreams.db"

    def getAnswer(self,dream_id):

        result = ""
        error = u"命令有误"

        if not dream_id.isdigit():
            return error

        
        result = Sqlite_Safe(self.DREAM_DB_PATH).query("select answer from dreams where id = %s"%dream_id)

        if not result:
            return error

        result = result[0][0]

        return result

    def ask(self,word):
 
        words = word.split()
        result = ""

        for word in words:
#            word = "%".join(list(word))
#            print word
            sql_result = Sqlite_Safe(self.DREAM_DB_PATH).query("select * from dreams where question like \"%%%s%%\""%word)
#            sql_str = "select * from dreams where question like \"%%%s%%\""%word
#            print sql_str
            result = ""
            for i in sql_result:
                result += u"\n%d："%i[0] + i[2]


        if not result:

            return u"没有找到相关梦境解析内容"

        return result


