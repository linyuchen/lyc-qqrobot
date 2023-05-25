#coding=UTF8
import sys
import os

cur_path = os.path.dirname(__file__)
cur_path = cur_path or "."
sys.path.append(cur_path + "/../sqlite_sserver/")

import sqliteSclient
import sqlite_db_config

class Manager:

    def __init__(self, groupQQ=None):

        self.dbName = sqlite_db_config.groupmdb_name
        ip = sqlite_db_config.sqlite_server
        port = sqlite_db_config.sqlite_port
        self.sqlite = sqliteSclient.Sqlite(ip, port, self.dbName)
        self.jnTable = "t_join_note"
        self.enTable = "t_exit_note"
        self.acnTable = "t_admin_change_note"
        self.knTable = "t_kick_note"
        self.defaultJoinNote = u"欢迎{name}({qq})加群本群!\n大家鼓掌欢迎！欢迎欢迎热烈欢迎~~~"
        self.defaultExitNote = u"{name}({qq})从本群消失了！大家默哀三秒钟！"
        self.defaultAdminChangeNote = u"{name}({qq})被{type}了管理员"
        self.defaultKickNote = u"{name}({qq})被{admin_name}({admin_qq})一脚踢出了本群"
        if groupQQ:
            self.groupQQ = groupQQ
            self.joinNote = self.getJoinNote(groupQQ)
            self.joinNoteSwitch = self.getJoinNoteSwitch(groupQQ)
            self.exitNote = self.getExitNote(groupQQ)
            self.exitNoteSwitch = self.getExitNoteSwitch(groupQQ)
            self.kickNote = self.getKickNote(groupQQ)
            self.kickNoteSwitch = self.getKickNoteSwitch(groupQQ)
            self.adminChangeNote = self.getAdminChangeNote(groupQQ)
            self.adminChangeNoteSwitch = self.getAdminChangeNoteSwitch(groupQQ)


    def __getValue(self, tbName, groupQQ, key):

        return self.sqlite.query("select %s from %s where group_qq='%s'" % (key, tbName, groupQQ)) 

    def __setValue(self, tbName, groupQQ, key, value):

        __value = self.__getValue(tbName, groupQQ, key)
        if __value == []:
            sqlStr = "insert into %s(group_qq, %s) values('%s', ?)" % (tbName, key,  groupQQ)
            self.sqlite.non_query(sqlStr, (value, ))
        else:
            sqlStr = "update %s set %s=? where group_qq='%s'" % (tbName, key, groupQQ)
            self.sqlite.non_query(sqlStr, (value, ))


    def getJoinNote(self, groupQQ):
        """
        新成员提示
        """

        note = self.__getValue(self.jnTable, groupQQ, "note")
        if note == []:
            return self.defaultJoinNote
        else:
            note = note[0][0]
            if not note:
                return self.defaultJoinNote
            else:
                return note

    def setJoinNote(self, groupQQ, note):

        self.joinNote = note
        self.__setValue(self.jnTable, groupQQ, "note", note)

    def getJoinNoteSwitch(self, groupQQ):

        switch = self.__getValue(self.jnTable, groupQQ, "switch")
        if switch == []:
            return 1
        else:
            return switch[0][0]

    def setJoinNoteSwitch(self, groupQQ, switch):

        self.joinNoteSwitch = switch
        self.__setValue(self.jnTable, groupQQ, "switch", switch)

    def getExitNote(self, groupQQ):
        """
        群成员退群提示
        """

        note = self.__getValue(self.enTable, groupQQ, "note")
        if note == []:
            return self.defaultExitNote
        else:
            note = note[0][0]
            if not note:
                return self.defaultExitNote
            else:
                return note

    def setExitNote(self, groupQQ, note):

        self.exitNote = note
        self.__setValue(self.enTable, groupQQ, "note", note)

    def getExitNoteSwitch(self, groupQQ):

        switch = self.__getValue(self.enTable, groupQQ, "switch")
        if switch == []:
            return 1
        else:
            return switch[0][0]

    def setExitNoteSwitch(self, groupQQ, switch):

        self.exitNoteSwitch = switch
        self.__setValue(self.enTable, groupQQ, "switch", switch)

    def getKickNote(self, groupQQ):
        """
        群踢人提示
        """

        note = self.__getValue(self.knTable, groupQQ, "note")
        if note == []:
            return self.defaultKickNote
        else:
            note = note[0][0]
            if not note:
                return self.defaultKickNote
            else:
                return note

    def setKickNote(self, groupQQ, note):

        self.exitNote = note
        self.__setValue(self.knTable, groupQQ, "note", note)

    def getKickNoteSwitch(self, groupQQ):

        switch = self.__getValue(self.knTable, groupQQ, "switch")
        if switch == []:
            return 1
        else:
            return switch[0][0]

    def setKickNoteSwitch(self, groupQQ, switch):

        self.kickNoteSwitch = switch
        self.__setValue(self.knTable, groupQQ, "switch", switch)


    def getAdminChangeNote(self, groupQQ):
        """
        管理变更提示
        """

        note = self.__getValue(self.acnTable, groupQQ, "note")
        if note == []:
            return self.defaultAdminChangeNote
        else:
            note = note[0][0]
            if not note:
                return self.defaultAdminChangeNote
            else:
                return note

    def setAdminChangeNote(self, groupQQ, note):

        self.__setValue(self.acnTable, groupQQ, "note", note)


    def getAdminChangeNoteSwitch(self, groupQQ):

        switch = self.__getValue(self.acnTable, groupQQ, "switch")
        if switch == []:
            return 1
        else:
            return switch[0][0]

    def setAdminChangeNoteSwitch(self, groupQQ, switch):

        self.adminChangeNoteSwitch = switch
        self.__setValue(self.acnTable, groupQQ, "switch", switch)


if __name__ == "__main__":

    groupQQ = 30115908
    test = Manager(groupQQ)
    """
    print test.joinNote
    print test.joinNoteSwitch
    test.setJoinNote(groupQQ, u"{name}")
    test.setJoinNoteSwitch(groupQQ, 0)
    """
    """
    print test.exitNote
    print test.exitNoteSwitch
    test.setExitNote(groupQQ, u"{name}不见了")
    test.setExitNoteSwitch(groupQQ, 0)
    """
    print test.kickNote
    print test.kickNoteSwitch
    test.setKickNote(groupQQ, u"踢了")
    test.setKickNoteSwitch(groupQQ, 0)
    #print test.exitNote
    """
    print test.adminChangeNoteSwitch
    test.setAdminChangeNoteSwitch(groupQQ, 0)
    """




