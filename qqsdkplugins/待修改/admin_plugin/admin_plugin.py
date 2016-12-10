#coding=UTF8

import os
import sys

cur_path = os.path.dirname(__file__)
cur_path = cur_path or "."
group_path = cur_path + "/../group_point"
sys.path.append(group_path)
sys.path.append(cur_path + "/../RPG")

import grouppluginbase
import 待修改.RPG as rpggame
import sqliteclient



class AdminPlugin:

    def __init__(self, qqClient):

        self.rpg_game = rpggame.RPG()
        self.qqClient = qqClient
        self.sqlite = sqliteclient.Sqlite(cur_path + "/RobotConfig.db")
        self.robotQQ = self.qqClient.qqUser.qq
        self.checkExistDb()

    def checkExistDb(self):

        r = self._getDbValue("qq")
        if not r:
            self.sqlite.non_query("insert into t_config(qq) values(%d)" % self.robotQQ)
        

    def sendMsg2Buddy(self, cmdStr):

        return self.__sendMsg(cmdStr, self.qqClient.sendMsg2Buddy)

    def sendMsg2Group(self, cmdStr):

        return self.__sendMsg(cmdStr, self.qqClient.sendMsg2Group)

    def __convertCmdStr2List(self, cmdStr):
        
        cmdStr = cmdStr.strip()
        cmdList = cmdStr.split()
        return cmdList


    def __sendMsg(self, cmdStr, sendFunc):
        
        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 2:
            return u"参数不对"

        sendFunc(cmdList[0], cmdList[1])
        return "ok"


    def get_point(self,qq_number):

        
        group_plugin = grouppluginbase.GroupPluginBase(None)
        sqlite = group_plugin.sqlite
        result = sqlite.get_value(group_plugin.point_table, ["group_qq", "point"], {"member_qq": qq_number})
        return str(result)

    def add_point(self, cmdStr):

        cmdList = self.__convertCmdStr2List(cmdStr)

        if len(cmdList) < 3:
            return u"参数数量不对"

        group_qq_number = cmdList[0]
        #print "group", group_qq_number
        qq_number = cmdList[1]
        point = cmdList[2]
        point = int(point)

        group_plugin = grouppluginbase.GroupPluginBase(group_qq_number)
        group_plugin._add_point(qq_number, "", point)

        return "ok"

    def set_point(self, cmdStr):

        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 3:
            return u"参数不对"
        group_qq_number = cmdList[0]
        qq_number = cmdList[1]
        point = cmdList[2]
        point = int(point)
        group_plugin = grouppluginbase.GroupPluginBase(group_qq_number)
        group_plugin._set_point(qq_number, point)
        return "ok"


    def get_clear_point_chance(self, cmdStr):
        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 1:
            return u"参数不对"
        qq_number = cmdList[0]
        group_plugin = grouppluginbase.GroupPluginBase("")
        result = group_plugin._get_clear_chance(qq_number)
        return u"%d" % result

    def add_clear_point_chance(self, cmdStr):
        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 2:
            return u"参数不对"

        qq_number = cmdList[0]
        num = cmdList[1]
        num = int(num)
        group_plugin = grouppluginbase.GroupPluginBase("")
        group_plugin._add_clear_chance(qq_number, num)
        return "ok"

    def get_rpg_data(self,qq_number):

        return self.rpg_game.get_person(qq_number).get_state()

    def clear_rpg_data(self,qq_number):

        sql_str = "delete from t_person where tag='%s'"%(qq_number)
        self.rpg_sqlite.non_query(sql_str)
        sql_str = "delete from t_knapsack where user_tag='%s'"%(qq_number)
        self.rpg_sqlite.non_query(sql_str)
        return "ok"


    def joinGroup(self, cmdStr):

        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 2:
            return u"参数错误"

        self.qqClient.joinGroup(cmdList[0], cmdList[1])
        return u"ok"

    def quitGroup(self, cmdStr):

        cmdList = self.__convertCmdStr2List(cmdStr)
        if len(cmdList) < 1:
            return u"参数错误"

        self.qqClient.quitGroup(cmdList[0])
        return u"ok"

    def getGroups(self):

        groups = self.qqClient.qqUser.groups
        num = len(groups)
        data = ""

        for qq, group in groups.items():
            data += u"%s (%d)\n" % (group.name, qq)

        data += u"共 %d 个群" % num

        return data

    def setInviteMeToGroup(self, cmdStr):
        
        cmdList = self.__convertCmdStr2List(cmdStr)
        key = "invite_me_to_group"
        key2 = "reject_invited_reason"

        if len(cmdList) < 1:
            return u"参数错误"

        typs = cmdList[0]

        if typs == u"同意":

            self._setDbValue(key, 1)
            return u"已设置成同意加群"

        elif typs == u"拒绝":

            if len(cmdList) < 2:
                return u"请填写拒绝理由"

            self._setDbValue(key, 0)
            self._setDbValue(key2, cmdList[1])
            return u"已设置成拒绝加群, 拒绝理由: " + self.getInviteMeToGroup()[1]

        else:
            return u"没有此操作方式"
        


    def _setDbValue(self, key, value):

        self.sqlite.non_query("update t_config set %s = ? where qq = %d" % (key, self.robotQQ), (value, ))

    def _getDbValue(self, key):

        return self.sqlite.query("select %s from t_config where qq = %d" % (key, self.robotQQ))

    def getInviteMeToGroup(self):

        type = self._getDbValue("invite_me_to_group")[0][0]
        reject_reason = self._getDbValue("reject_invited_reason")[0][0]

        return type, reject_reason

if __name__ == "__main__":

    class Group:pass

    class QQUser:pass

    class Client:
        def __init__(self):

            self.qqUser = QQUser()
            group = Group()
            group.name = "1234"
            self.qqUser.groups = {123: group}
            self.qqUser.qq = 2333
    test = AdminPlugin(Client())

    print test.setInviteMeToGroup(u"同意")
    print test.setInviteMeToGroup(u"拒绝 加群请联系我的主人")
    print test.setInviteMeToGroup(u"妮妮")
    typ, reason = test.getInviteMeToGroup()
    print typ, reason
    print test.getGroups()
