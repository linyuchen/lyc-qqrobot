#coding=UTF8

import os
import sys

curPath = os.path.dirname(__file__) or "."
sys.path.append(curPath + "/../sqlite_sserver")
import sqliteSclient
import sqlite_db_config

class GroupPlugin:

    def __init__(self, groupQQ):

        self.dbName = sqlite_db_config.groupmdb_name
        ip = sqlite_db_config.sqlite_server
        port = sqlite_db_config.sqlite_port
        self.sqlite = sqliteSclient.Sqlite(ip, port, self.dbName)

        self.__getValue = self.sqlite.get_value
        self.__setValue = self.sqlite.set_value

        self.groupQQ = groupQQ

        self.ccTable = "t_closed_cmd"
        self.wcTable = "t_white_cmd"
        self.ssTable = "t_shutdown_switch"
        self.csTable = "t_chat_switch"

        self.closedCmd = self.getClosedCmd()
        self.whiteCmd = self.getWhiteCmd()
        self.shutdownSwitch = self.getShutdownSwitch()
        self.chatSwitch = self.getChatSwitch()


 


    def __delValue(self, table, key, value):

        sqlStr = "delete from %s where group_qq='%s' and %s=?" % (table, self.groupQQ, key)
        self.sqlite.non_query(sqlStr, (value, ))

    # 已关闭命令

    def getClosedCmd(self):

        result = self.__getValue(self.ccTable, ["cmd"],  {"group_qq": self.groupQQ})
        result = [i[0] for i in result]
        return result
    
    def addClosedCmd(self, cmd):

        if cmd not in self.closedCmd:
            self.closedCmd.append(cmd)
        self.__setValue(self.ccTable, {"group_qq": self.groupQQ, "cmd": cmd}, {"group_qq": self.groupQQ, "cmd": cmd})

    def delClosedCmd(self, cmd):

        if cmd in self.closedCmd:
            self.closedCmd.remove(cmd)

        self.__delValue(self.ccTable, "cmd", cmd)

    # 白名单命令

    def getWhiteCmd(self):

        result = self.__getValue(self.wcTable, ["cmd"], {"group_qq": self.groupQQ})
        result = [i[0] for i in result]
        return result
    
    def addWhiteCmd(self, cmd):

        if cmd not in self.whiteCmd:
            self.whiteCmd.append(cmd)
        self.__setValue(self.wcTable, {"group_qq": self.groupQQ, "cmd": cmd}, {"group_qq": self.groupQQ, "cmd": cmd})

    def delWhiteCmd(self, cmd):

        if cmd in self.whiteCmd:
            self.whiteCmd.remove(cmd)

        self.__delValue(self.wcTable, "cmd", cmd)
    
    # 关机开关

    def getShutdownSwitch(self):

        result = self.__getValue(self.ssTable, ["switch"], {"group_qq": self.groupQQ})
        if result == []:
            return 0
        else:
            return result[0][0]

    def setShutdownSwitch(self, switch):
        """
        1 关机
        0 开机
        """

        self.shutdownSwitch = switch
        self.__setValue(self.ssTable, {"group_qq": self.groupQQ, "switch": switch}, {"group_qq": self.groupQQ})

        
    def getChatSwitch(self):

        result = self.__getValue(self.csTable, ["switch"], {"group_qq": self.groupQQ})
        if result == []:
            return 1
        else:
            return result[0][0]

    def setChatSwitch(self, switch):
        """
        1 开启群聊天
        0 关闭群聊天
        """

        self.chatSwitch = switch
        self.__setValue(self.csTable, {"group_qq": self.groupQQ, "switch": switch}, {"group_qq": self.groupQQ})

if __name__ == "__main__":

    test =  GroupPlugin(30115908)
    """
    print test.shutdownSwitch
    test.setShutdownSwitch(1)
    """
    """
    print test.getClosedCmd()
    test.addClosedCmd(u"签到")
    test.addClosedCmd(u"1")
    test.delClosedCmd(u"签到")
    """
    """
    print test.getWhiteCmd()
    test.addWhiteCmd(u"签到")
    test.addWhiteCmd(u"斗牛")
    test.delWhiteCmd(u"签到")
    """
#    print test.getChatSwitch()
    #test.setChatSwitch(1)
