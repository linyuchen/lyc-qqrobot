# -*- encoding:UTF8 -*-
import os
from sqliteclient import Sqlite_Safe


class BrainTwister:

    def __init__(self):

        cur_path = os.path.dirname(__file__)
        self.cur_path = cur_path or "."
        self.BRAINTWISTS_DB_PATH = self.cur_path + "/braintwists.db"

    def getRandomOne(self):

        braintwists = Sqlite_Safe(self.BRAINTWISTS_DB_PATH).query("select * from braintwists order by RANDOM() limit 1")
        braintwists = braintwists[0]
        braintwists_id = braintwists[0]
        braintwists_question = braintwists[1]
        braintwists_answer = braintwists[2]
        return u"序号:%d\n" % braintwists_id + braintwists_question

    def getAnswer(self,braintwists_id):

        error = u"命令有误"
        if not braintwists_id.isdigit():

            return error

        braintwists = Sqlite_Safe(self.BRAINTWISTS_DB_PATH).query(
            "select question,answer from braintwists where id = %s" % braintwists_id)

        if not braintwists :

            return error

        braintwists_question = braintwists[0][0]
        braintwists_answer = braintwists[0][1]

        return braintwists_question + "\n\n" + braintwists_answer
