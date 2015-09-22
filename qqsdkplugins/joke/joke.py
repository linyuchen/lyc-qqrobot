# -*- encoding:UTF8 -*-

import os
from sqliteclient import Sqlite_Safe

class Joke:

    def __init__(self):

        cur_path = os.path.dirname(__file__)
        self.cur_path = cur_path or "."
        self.JOKE_DB_PATH = self.cur_path + "/jokes.db"

    def getRandomOne(self):

        result = Sqlite_Safe(self.JOKE_DB_PATH).query("select content from jokes order by RANDOM() limit 1")
        joke = result[0][0]
        
        return joke

