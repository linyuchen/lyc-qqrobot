#coding=UTF8

import sys
import os

cur_path = os.path.dirname(__file__) or "."
sys.path.append(cur_path + "/..")
import sqliteclient
DB_PATH = cur_path + "/idioms.db"
sqlite = sqliteclient.Sqlite(DB_PATH)

class IdiomsSolitaireBase(object):

    def __init__(self):

        self.t_word = "word"
        self.current_idiom = ""
        self.exists_idiom_list = []

    def reset_game_info(self):

        self.exists_idiom_list = []

    def get_random_idiom(self):
        
        result = sqlite.query("select word_name from %s order by random() limit 1"%(self.t_word))
        current_idiom = result[0][0]
        if sqlite.query("select word_name from %s where word_name like '%s%%'"%(self.t_word, current_idiom[-1])):
            self.exists_idiom_list.append(current_idiom)
            return current_idiom
        else:
            return self.get_random_idiom()


    def judge(self,idiom):
        """
        @return 0: Not found the idiom
        @return 1: Success
        @return 2: Failed
        @return 3: Idiom is existed
        @return 4: The current idiom is None
        """
        
        result = sqlite.query("select word_name from %s where word_name='%s'"%(self.t_word,idiom))
        if not self.current_idiom:
            return 4

        elif not result:
            return 0
        
        elif idiom in self.exists_idiom_list:
            return 3

        elif idiom[0].replace(",","").replace(u"，","") == self.current_idiom[-1].replace(",","").replace(u"，",""):
            self.current_idiom = idiom
            return 1
            
        else:
            return 2


if "__main__" == __name__:

    test = IdiomsSolitaireBase()
    word = test.get_random_idiom()
    print word
    while True:
        print sqlite.query("select word_name from word where word_name like '%s%%'"%(raw_input("").decode("gbk")[-1]))[0][0]
    print test.judge(raw_input("").decode("gbk"))
