# -*- encoding:UTF8 -*-

import os
from sqliteclient import Sqlite_Safe

class Riddle:

    def __init__(self):

        cur_path = os.path.dirname(__file__)
        self.cur_path = cur_path or "."
        self.RIDDLE_DB_PATH = cur_path+ "/riddle.db"


    def getRandomOne(self):

        dbCon = Sqlite_Safe(self.RIDDLE_DB_PATH)
        riddle = dbCon.query("select * from riddle order by RANDOM() limit 1")
        riddle = riddle[0]
        riddle_id = riddle[0]
        riddle_question = riddle[1]

        return u"序号:%d"%riddle_id + riddle_question + u"\n\n"

        
    def getAnswer(self,riddle_id):

        error = u"命令有误"
        if not riddle_id.isdigit():

            return error

        dbCon = Sqlite_Safe(self.RIDDLE_DB_PATH)
        riddle = dbCon.query("select question,answer,tip from riddle where id = %s"%riddle_id)

        if not riddle :

            return error

        riddle_question = riddle[0][0]
        riddle_answer = riddle[0][1]
        riddle_tip = riddle[0][2]

        return riddle_question + "\n" + riddle_tip + "\n" + riddle_answer

