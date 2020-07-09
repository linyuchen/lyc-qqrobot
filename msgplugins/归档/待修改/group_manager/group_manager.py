#coding=UTF8

import re
import os
import sys

curPath = os.path.dirname(__file__) or "."
sys.path.append(curPath + "/../sqlite_sserver")
import sqliteSclient
import sqlite_db_config


class GroupManager:

    def __init__(self, groupQQ=None):

        self.dbName = sqlite_db_config.groupmdb_name
        ip = sqlite_db_config.sqlite_server
        port = sqlite_db_config.sqlite_port
        self.sqlite = sqliteSclient.Sqlite(ip, port, self.dbName)
        self.wcTable = "t_warning_count"
        self.sdTable = "t_shuabing_detect"
        self.blTable = "t_black_list"
        self.bsTable = "t_black_switch"
        self.avTable = "t_auto_verify"
        self.wordTypeSen = "sensitive"
        self.wordTypeProh = "prohibited"
        self.shuabingMaxRows = self.defaultShuabingMaxRowsNum = 10
        self.shuabingMaxWords = self.defaultShuabingMaxWordsNum = 200
        self.shuabingMaxContinuous = self.defaultShuabingMaxContinuousNum = 3
        self.autoVerify = 1
        self.blackSwitch = 1
        self.sensitiveWords = []
        self.prohibitedWords = []
        self.shuabingDetect = 1
        self.blackQQ = []

        if groupQQ:
            self.groupQQ = groupQQ

            self.sensitiveWords = self.getSensitiveWords(self.groupQQ)
            self.prohibitedWords = self.getProhibitedWords(self.groupQQ)
            self.shuabingDetect = self.getShuabingDetect(self.groupQQ)
            self.shuabingMaxRows = self.getShuabingMaxRows(self.groupQQ)
            self.shuabingMaxWords = self.getShuabingMaxWords(self.groupQQ)
            self.shuabingMaxContinuous = self.getShuabingMaxContinuous(self.groupQQ)
            self.blackQQ = self.getBlackQQ(self.groupQQ)
            self.autoVerify = self.getAutoVerify(self.groupQQ)
            self.blackSwitch = self.getBlackSwitch(self.groupQQ)

        self.lastSpeaker = None
        self.lastWord = ""
        self.speakerContinuous = 1

    def __getBlackSwitch(self, groupQQ):

        sqlStr = "select switch from %s where group_qq='%s'" % (self.bsTable, groupQQ)
        result = self.sqlite.query(sqlStr)
        return result

    def getBlackSwitch(self, groupQQ):

        result = self.__getBlackSwitch(groupQQ)
        if result == []:
            return 1
        else:
            return result[0][0]

    def setBlackSwitch(self, groupQQ, switch):

        self.blackSwitch = switch
        result = self.__getBlackSwitch(groupQQ)
        if result == []:
            sqlStr = "insert into %s(group_qq, switch) values('%s', %d)" % (self.bsTable, groupQQ, switch)
        else:
            sqlStr = "update %s set switch=%d where group_qq='%s'" % (self.bsTable, switch, groupQQ)
        self.sqlite.non_query(sqlStr)

    
    def getBlackQQ(self, groupQQ):

        sqlStr = "select qq from %s where group_qq='%s'" % (self.blTable, groupQQ)
        result = self.sqlite.query(sqlStr)
        if result:
            result = [i[0] for i in result]
        return result

    def addBlackQQ(self, groupQQ, qq):

        self.blackQQ.append(qq)
        sqlStr = "insert into %s(group_qq, qq) values('%s', '%s')" % (self.blTable, groupQQ, qq)
        self.sqlite.non_query(sqlStr)

    def delBlackQQ(self, groupQQ, qq):

        if qq in self.blackQQ:
            self.blackQQ.remove(qq)
        sqlStr = "delete from %s where group_qq = '%s' and qq = '%s'" % (self.blTable, groupQQ, qq)
        self.sqlite.non_query(sqlStr)

    def getMemberWarningCount(self, groupQQ, memberQQ):
        """
        查到记录返回int
        查不到返回None
        """

        sqlStr = "select warning_count from %s where group_qq = '%s' and member_qq = ?" % (self.wcTable, groupQQ)
        result = self.sqlite.query(sqlStr, (memberQQ, ))
        if not result:
            return None
        else:
            return result[0][0]

    def setMemberWarningCount(self, groupQQ, memberQQ, count, autoAdd=True):
        """
        autoAdd: 在原来的基础上加
        """

        existsCount = self.getMemberWarningCount(groupQQ, memberQQ)
        if existsCount == None:
            sqlStr = "insert into %s(group_qq, member_qq, warning_count) values('%s', '%s', %d)" % (self.wcTable, groupQQ, memberQQ, count)
            self.sqlite.non_query(sqlStr)
        else:
            if autoAdd:
                count += existsCount
            sqlStr = "update %s set warning_count = %d where group_qq='%s' and member_qq='%s'" % (self.wcTable, count, groupQQ, memberQQ)
            self.sqlite.non_query(sqlStr)

    def __getWordTable(self, wordType):
        if self.wordTypeSen == wordType:
            table = "t_sensitive_word"
        elif self.wordTypeProh == wordType:
            table = "t_prohibited_word"
        return table

    def __getWords(self, groupQQ, wordType):

        table = self.__getWordTable(wordType)

        sqlStr = "select word from %s where group_qq = '%s'" % (table, groupQQ)
        result = self.sqlite.query(sqlStr)
        if result:
            return [i[0] for i in result]
        return result

    def __addWord(self, groupQQ, word, wordType):

        table = self.__getWordTable(wordType)

        sqlStr = "insert into %s(group_qq, word) values(%s, ?)" % (table, groupQQ)
        self.sqlite.non_query(sqlStr, (word, ))

    def __delWord(self, groupQQ, word, wordType):

        table = self.__getWordTable(wordType)
        sqlStr = "delete from %s where group_qq = '%s' and word = ?" % (table, groupQQ)
        self.sqlite.non_query(sqlStr, (word, ))

    def addSensitiveWord(self, groupQQ, word):

        self.sensitiveWords.append(word)
        self.__addWord(groupQQ, word, self.wordTypeSen)

    def delSensitiveWord(self, groupQQ, word):

        if word in self.sensitiveWords:
            self.sensitiveWords.remove(word)
        self.__delWord(groupQQ, word, self.wordTypeSen)

    def addProhibitedWord(self, groupQQ, word):

        self.prohibitedWords.append(word)
        self.__addWord(groupQQ, word, self.wordTypeProh)

    def delProhibitedWord(self, groupQQ, word):

        if word in self.prohibitedWords:
            self.prohibitedWords.remove(word)
        self.__delWord(groupQQ, word, self.wordTypeProh)

    def getSensitiveWords(self, groupQQ):

        return self.__getWords(groupQQ, self.wordTypeSen)

    def getProhibitedWords(self, groupQQ):

        return self.__getWords(groupQQ, self.wordTypeProh)


    def __checkWord(self, acceptWord, dbWords):
        """
        acceptWord: str
        dbWords: list, 每个元素是str
        """
        for word in dbWords:
            result = re.match(word, acceptWord) or word in acceptWord
            if result:
                return True

        return False

    def checkSensitiveWord(self, groupQQ, acceptWord):

        return self.__checkWord(acceptWord, self.sensitiveWords)

    def checkProhibitedWord(self, groupQQ, acceptWord):

        return self.__checkWord(acceptWord, self.prohibitedWords)

    def __getShuabingValue(self, groupQQ, key):

        sqlStr = "select %s from %s where group_qq = '%s'" % (key, self.sdTable, groupQQ)
        result = self.sqlite.query(sqlStr)
        return result

    def __setShuabingValue(self, groupQQ, key, value):

        result = self.__getShuabingValue(groupQQ, key)
        if result == []:
            sqlStr = "insert into %s(group_qq, %s) values('%s', ?)" % (self.sdTable, key, groupQQ)
        else:
            sqlStr = "update %s set %s=? where group_qq='%s'" % (self.sdTable, key, groupQQ)

        self.sqlite.non_query(sqlStr, (value, ))

    def __getShuabingDetect(self, groupQQ):

        result = self.__getShuabingValue(groupQQ, "detect")
        return result


    def getShuabingDetect(self, groupQQ):

        result = self.__getShuabingDetect(groupQQ)
        if not result:
            return True
        else:
            result = result[0][0]
            
            if result == 1:
                return True
            else:
                return False

    def setShuabingDetect(self, groupQQ, op):

        self.shuabingDetect = op
        self.__setShuabingValue(groupQQ, "detect", op)


    def getShuabingMaxRows(self, groupQQ):

        result = self.__getShuabingValue(groupQQ, "max_rows")
        if result == []:
            return self.defaultShuabingMaxRowsNum
        else:
            return result[0][0]

    def setShuabingMaxRows(self, groupQQ, num):

        self.shuabingMaxRows = num
        self.__setShuabingValue(groupQQ, "max_rows", num)

    def getShuabingMaxContinuous(self, groupQQ):

        result = self.__getShuabingValue(groupQQ, "max_continuous")
        if result == []:
            return self.defaultShuabingMaxContinuousNum
        else:
            return result[0][0]

    def setShuabingMaxContinuous(self, groupQQ, num):

        self.shuabingMaxContinuous = num
        self.__setShuabingValue(groupQQ, "max_continuous", num)

    def getShuabingMaxWords(self, groupQQ):
        """
        一次性发言最多字数
        """

        result = self.__getShuabingValue(groupQQ, "max_words")
        if result == []:
            return self.defaultShuabingMaxWordsNum
        else:
            return result[0][0]

    def setShuabingMaxWords(self, groupQQ, num):

        self.shuabingMaxWords = num
        self.__setShuabingValue(groupQQ, "max_words", num)

    def checkShuabing(self, memberQQ, word):
        """
        return: True 是刷屏， False 不是刷屏
        """

        lines = word.count("\n") + word.count("\r")
        
        if len(word) >= self.shuabingMaxWords:
            return True

        if lines >= self.shuabingMaxRows - 1:
            return True

        if memberQQ == self.lastSpeaker and word == self.lastWord:
            self.speakerContinuous += 1
            if self.speakerContinuous >= self.shuabingMaxContinuous:
                return True
        else:
            self.speakerContinuous = 1

        self.lastWord = word
        self.lastSpeaker = memberQQ
        
        return False

    def __getAutoVerify(self, groupQQ):

        sqlStr = "select type from %s where group_qq = '%s'" % (self.avTable, groupQQ)
        result = self.sqlite.query(sqlStr)
        return result

    def getAutoVerify(self, groupQQ):

        result = self.__getAutoVerify(groupQQ)
        if result:
            return result[0][0]
        else:
            return 1

    def setAutoVerify(self, groupQQ, verifyType):
        """
        verifyType: 0 自动拒绝， 1 自动同意， 2 自动忽略
        """

        self.autoVerify = verifyType
        result = self.__getAutoVerify(groupQQ)
        if result == []:
            sqlStr = "insert into %s(group_qq, type) values('%s', %d)" % (self.avTable, groupQQ, verifyType)
            self.sqlite.non_query(sqlStr)
        else:
            sqlStr = "update %s set type=%d where group_qq='%s'" % (self.avTable, verifyType, groupQQ)
            self.sqlite.non_query(sqlStr)
        


if __name__ == "__main__":

    test = GroupManager()
    groupQQ = 30115908
    """
    print test.getMemberWarningCount(30115908, 1412971608)
    print test.setMemberWarningCount(30115908, 1412971608, 1, True)
    """
    #print test.addSensitiveWord(30115908, u"'")
    #print test.getSensitiveWords(30115908)
    #print test.checkSensitiveWord(30115908, u"呵呵哈")
    #test.delSensitiveWord(30115908, u"'")
#    print test.getProhibitedWords(30115908)
#    print test.addProhibitedWord(30115908, u"'''")
#    test.delProhibitedWord(30115908, u"'''")
    #print test.getShuabingDetect(30115908)
    #test.setShuabingDetect(30115908, 1)
    #print test.getShuabingMaxRows(30115908)
    #print test.setShuabingMaxRows(30115908, 11)
    #print test.getShuabingMaxContinuous(30115908)
    #print test.setShuabingMaxContinuous(30115908, 4) 
#    print test.getShuabingMaxWords(30115908)
#    print test.setShuabingMaxWords(30115908, ) 
    """
    print test.getBlackQQ(30115908)
    test.addBlackQQ(30115908, 123)
    test.delBlackQQ(30115908, 123)
    """
    print test.getBlackSwitch(groupQQ)
    test.setBlackSwitch(groupQQ, 1)
    """
    print test.getAutoVerify(30115908)
    test.setAutoVerify(30115908, 2)
    """





