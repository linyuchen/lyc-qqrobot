<<<<<<< HEAD:qqsdkplugins/待修改/group_manager/__init__.py
#coding=UTF8

import cmdaz
import group_manager
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
GroupManager = group_manager.GroupManager

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群管理：
        群发言检测
        群黑名单
        加群审核
        
    """
    def __init__(self):

        self.name = u"groupmsg_check"
        self.cmdKick = CMD(u"踢", hasParam=True)
        self.cmdClrScreen = CMD(u"清屏")
        self.cmdMyWarningCount = CMD(u"我的警告次数")
        self.cmdOtherWarningCount = CMD(u"他的警告次数", hasParam=True)
        self.cmdClearWarningCount = CMD(u"清警告次数", hasParam=True)

        self.cmdGetSensitiveWords = CMD(u"敏感词")
        self.cmdGetProhibitedWords = CMD(u"违禁词")
        self.cmdAddSensitiveWords = CMD(u"加敏感词", hasParam=True)
        self.cmdAddProhibitedWords = CMD(u"加违禁词", hasParam=True)
        self.cmdDelSensitiveWords = CMD(u"删敏感词", hasParam=True)
        self.cmdDelProhibitedWords = CMD(u"删违禁词", hasParam=True)

        self.cmdOpenShuabingDetect = CMD(u"开启刷屏检测")
        self.cmdCloseShuabingDetect = CMD(u"关闭刷屏检测")
        self.cmdShuabingStatus = CMD(u"刷屏检测状态")

        self.cmdSetShuabingMaxRows = CMD(u"设置刷屏行数", hasParam=True)
        self.cmdSetShuabingMaxWords = CMD(u"设置刷屏字数", hasParam=True)
        self.cmdSetShuabingMaxContinuous = CMD(u"设置刷屏连续次数", hasParam=True)
        self.maxWarningCount = 3

        self.cmdOpenBlackQQ = CMD(u"开启黑名单")
        self.cmdCloseBlackQQ = CMD(u"关闭黑名单")
        self.cmdAddBlackQQ = CMD(u"加黑", hasParam=True)
        self.cmdDelBlackQQ = CMD(u"解黑", hasParam=True)
        self.cmdGetBlackQQ = CMD(u"黑名单")

        self.cmdAutoAllow = CMD(u"加群自动同意")
        self.cmdAutoReject = CMD(u"加群自动拒绝")
        self.cmdAutoIgnore = CMD(u"加群自动忽略")
        self.cmdGetVerifyType = CMD(u"加群审核方式")
        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def checkWarningCount(self, groupManager, groupQQ, member):

        result = ""
        count = groupManager.getMemberWarningCount(groupQQ, member.qq)
        if count >= self.maxWarningCount:
            result += u"%s 超过警告次数%d次, 正在执行裁决......\n" % (member.get_name(), self.maxWarningCount)
            result += self.qqClient.delete_group_member(groupQQ, member.qq)
            result += "\n"

        return result

    def getGroupManger(self, groupQQ):

        if self.groupInstances.has_key(groupQQ):
            groupManager = self.groupInstances[groupQQ]
        else:
            groupManager = GroupManager(groupQQ)
            self.groupInstances[groupQQ] = groupManager
        return groupManager

    def handleRequestJoinMsg(self, msg):

        groupQQ = msg.group.qq
        memberName = msg.requestName
        memberQQ = msg.requestQQ
        groupManager = self.getGroupManger(groupQQ)
        if str(memberQQ) in groupManager.blackQQ and groupManager.balckSwitch:
            msg.reject(u"你在本群黑名单之上，禁止加入")
            self.qqClient.send_group_msg(groupQQ, u"%s(%s)企图加入本群，但由于此人乃黑名单上之物，已拒绝之！" % (memberName, memberQQ))
        else:
            if groupManager.autoVerify == 1:
                msg.allow()
            elif groupManager.autoVerify == 0:
                msg.reject()

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember

        groupManager = self.getGroupManger(groupQQ)

        """
        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = groupplugin.GroupPlugin(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin
        """

        result = ""

        if groupManager.checkShuabing(member.qq, msg.msg) and groupManager.shuabingDetect and not member.isAdmin:
            result += u"%s 刷屏， 警告一次！警告超过%d次将被踢出本群\n" % (member.get_name(), self.maxWarningCount)
            groupManager.setMemberWarningCount(groupQQ, member.qq, 1, True)
            result += self.checkWarningCount(groupManager, groupQQ, member)

        if groupManager.checkSensitiveWord(groupQQ, msg.msg) and not member.isAdmin:
            result += u"%s 发言有敏感词， 警告一次！警告超过%d次将被踢出本群\n" % (member.get_name(), self.maxWarningCount)
            groupManager.setMemberWarningCount(groupQQ, member.qq, 1, True)
            result += self.checkWarningCount(groupManager, groupQQ, member)

        if groupManager.checkProhibitedWord(groupQQ, msg.msg) and not member.isAdmin:
            result += u"%s 发言有违禁词，正在执行裁决......\n " % member.get_name()
            result += self.qqClient.delete_group_member(groupQQ, member.qq)
        
        #命令判断
        if self.cmdClrScreen.az(msg.msg):
            if member.isAdmin:
                result += u"- \t\n\n\t -"*800 + u"清屏完毕~\n"
            else:
                result += u"%s 您不是管理员，无权操作！\n" % (member.get_name())
        elif self.cmdKick.az(msg.msg):
            if member.isAdmin:
                param = self.cmdKick.get_param_list()[0]
                if param.isdigit():
                    result += self.qqClient.delete_group_member(groupQQ, int(param))
                    #print result
                else:
                    result += u"QQ号不正确，踢人失败!\n"
            else:
                result += u"%s 您不是管理员，无法踢人！\n" % (member.get_name())
        elif self.cmdMyWarningCount.az(msg.msg):
            count = groupManager.getMemberWarningCount(groupQQ, member.qq)
            if count == None:
                warningCount = 0
            else:
                warningCount = count
            result += u"%s (%d)的警告次数为 %d\n" % (member.get_name(), member.qq, warningCount)

        elif self.cmdGetSensitiveWords.az(msg.msg):
            result += u"当前敏感词：\n"
            words = groupManager.getSensitiveWords(groupQQ)
            words = "\n".join(words)
            result += words

        elif self.cmdGetProhibitedWords.az(msg.msg):
            result += u"当前违禁词：\n"
            words = groupManager.getProhibitedWords(groupQQ)
            words = "\n".join(words)
            result += words

        elif self.cmdAddSensitiveWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdAddSensitiveWords.get_param_list()
                for word in params:
                    groupManager.addSensitiveWord(groupQQ, word)
                result += u"敏感词添加完成\n"
            else:
                result += u"%s 您不是管理员，无法添加敏感词！\n" % (member.get_name())

        elif self.cmdDelSensitiveWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdDelSensitiveWords.get_param_list()
                for word in params:
                    groupManager.delSensitiveWord(groupQQ, word)
                result += u"敏感词删除完成\n"
            else:
                result += u"%s 您不是管理员，无法删除敏感词！\n" % (member.get_name())

        elif self.cmdAddProhibitedWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdAddProhibitedWords.get_param_list()
                for word in params:
                    groupManager.addProhibitedWord(groupQQ, word)
                result += u"违禁词添加完成\n"
            else:
                result += u"%s 您不是管理员，无法添加违禁词！\n" % (member.get_name())

        elif self.cmdDelProhibitedWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdDelProhibitedWords.get_param_list()
                for word in params:
                    groupManager.delProhibitedWord(groupQQ, word)
                result += u"违禁词删除完成\n"
            else:
                result += u"%s 您不是管理员，无法删除违禁词！\n" % (member.get_name())

        elif self.cmdOtherWarningCount.az(msg.msg):
            if member.isAdmin:
                param = self.cmdOtherWarningCount.get_param_list()[0]
                warningCount = groupManager.getMemberWarningCount(groupQQ, param)
                result += u"%s 的警告次数为 %d\n" % (param, warningCount)
            else:
                result += u"%s 您不是管理员，无权查看!\n" % (member.get_name())

        elif self.cmdClearWarningCount.az(msg.msg):
            if member.isAdmin:
                param = self.cmdClearWarningCount.get_param_list()[0]
                warningCount = groupManager.getMemberWarningCount(groupQQ, param)
                #print warningCount
                if warningCount:
                    groupManager.setMemberWarningCount(groupQQ, param, 0, False)
                result += u"%s的警告次数已经清零\n" % (param)
            else:
                result += u"%s 您不是管理员，无权清零警告次数!\n" % (member.get_name())

        elif self.cmdOpenShuabingDetect.az(msg.msg):
            if member.isAdmin:
                groupManager.setShuabingDetect(groupQQ, 1)
                result += u"刷屏检测已开启\n"
            else:
                result += u"%s 您不是管理员，无权开启刷屏检测!\n" % (member.get_name())
        elif self.cmdCloseShuabingDetect.az(msg.msg):
            if member.isAdmin:
                groupManager.setShuabingDetect(groupQQ, 0)
                result += u"刷屏检测已关闭\n"
            else:
                result += u"%s 您不是管理员，无权关闭刷屏检测!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxRows.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxRows.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏行数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxRows(groupQQ, int(param))
                    result += u"刷屏行数设置成功!\n"

            else:
                result += u"%s 您不是管理员，无权设置刷屏行数!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxWords.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxWords.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏字数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxWords(groupQQ, int(param))
                    result += u"刷屏字数设置成功!"

            else:
                result += u"%s 您不是管理员，无权设置刷屏字数!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxContinuous.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxContinuous.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏连续次数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxContinuous(groupQQ, int(param))
                    result += u"刷屏连续次数设置成功!"
            else:
                result += u"%s 您不是管理员，无权设置刷屏连续次数!\n" % (member.get_name())

        elif self.cmdShuabingStatus.az(msg.msg):
            if member.isAdmin:
                status = u"开启" if groupManager.shuabingDetect else u"关闭"
                result += u"刷屏检测状态：%s \n发言行数达到%d行视为刷屏\n发言字数达到%d字视为刷屏\n同一人连续发言相同内容%d次视为刷屏\n" % (status, groupManager.shuabingMaxRows, groupManager.shuabingMaxWords, groupManager.shuabingMaxContinuous)
            else:
                result += u"%s 您不是管理员，无权查看刷屏检测状态!\n" % (member.get_name())

        # 黑名单
        elif self.cmdAddBlackQQ.az(msg.msg):

            if member.isAdmin:
                param = self.cmdAddBlackQQ.get_param_list()[0]
                if not param.isdigit():
                    result += u"QQ号只能为数字!\n"
                else:
                    groupManager.addBlackQQ(groupQQ, param)
                    result += u"加黑QQ%s成功!" % param
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())
                
        elif self.cmdDelBlackQQ.az(msg.msg):

            if member.isAdmin:
                param = self.cmdDelBlackQQ.get_param_list()[0]
                if not param.isdigit():
                    result += u"QQ号只能为数字!\n"
                else:
                    groupManager.delBlackQQ(groupQQ, param)
                    result += u"解黑QQ%s成功!" % param
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdGetBlackQQ.az(msg.msg):

            if member.isAdmin:
                blackList = groupManager.getBlackQQ(groupQQ)

                result += u"当前黑名单：\n" + "\n".join(blackList)
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())
        
        # 加群审核
        elif self.cmdAutoAllow.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 1)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdAutoReject.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 0)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdAutoIgnore.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 2)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdGetVerifyType.az(msg.msg):

            if member.isAdmin:
                result += u"当前加群审核方式："
                if groupManager.autoVerify == 0:
                    result += u"自动拒绝"
                elif groupManager.autoVerify == 1:
                    result += u"自动同意"
                elif groupManager.autoVerify == 2:
                    result += u"自动忽略"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdOpenBlackQQ.az(msg.msg):

            if member.isAdmin:
                groupManager.setBlackSwitch(groupQQ, 1)
                result += u"黑名单已开启"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdCloseBlackQQ.az(msg.msg):

            if member.isAdmin:
                groupManager.setBlackSwitch(groupQQ, 0)
                result += u"黑名单已关闭"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())



        if result:
            msg.reply(result)
            msg.destroy()



# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addRequestJoinGroupEvent(MsgEvent(event.handleRequestJoinMsg))

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



=======
#coding=UTF8

import cmdaz
import group_manager
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
GroupManager = group_manager.GroupManager

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群管理：
        群发言检测
        群黑名单
        加群审核
        
    """
    def __init__(self):

        self.name = u"groupmsg_check"
        self.cmdKick = CMD(u"踢", hasParam=True)
        self.cmdClrScreen = CMD(u"清屏")
        self.cmdMyWarningCount = CMD(u"我的警告次数")
        self.cmdOtherWarningCount = CMD(u"他的警告次数", hasParam=True)
        self.cmdClearWarningCount = CMD(u"清警告次数", hasParam=True)

        self.cmdGetSensitiveWords = CMD(u"敏感词")
        self.cmdGetProhibitedWords = CMD(u"违禁词")
        self.cmdAddSensitiveWords = CMD(u"加敏感词", hasParam=True)
        self.cmdAddProhibitedWords = CMD(u"加违禁词", hasParam=True)
        self.cmdDelSensitiveWords = CMD(u"删敏感词", hasParam=True)
        self.cmdDelProhibitedWords = CMD(u"删违禁词", hasParam=True)

        self.cmdOpenShuabingDetect = CMD(u"开启刷屏检测")
        self.cmdCloseShuabingDetect = CMD(u"关闭刷屏检测")
        self.cmdShuabingStatus = CMD(u"刷屏检测状态")

        self.cmdSetShuabingMaxRows = CMD(u"设置刷屏行数", hasParam=True)
        self.cmdSetShuabingMaxWords = CMD(u"设置刷屏字数", hasParam=True)
        self.cmdSetShuabingMaxContinuous = CMD(u"设置刷屏连续次数", hasParam=True)
        self.maxWarningCount = 3

        self.cmdOpenBlackQQ = CMD(u"开启黑名单")
        self.cmdCloseBlackQQ = CMD(u"关闭黑名单")
        self.cmdAddBlackQQ = CMD(u"加黑", hasParam=True)
        self.cmdDelBlackQQ = CMD(u"解黑", hasParam=True)
        self.cmdGetBlackQQ = CMD(u"黑名单")

        self.cmdAutoAllow = CMD(u"加群自动同意")
        self.cmdAutoReject = CMD(u"加群自动拒绝")
        self.cmdAutoIgnore = CMD(u"加群自动忽略")
        self.cmdGetVerifyType = CMD(u"加群审核方式")
        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def checkWarningCount(self, groupManager, groupQQ, member):

        result = ""
        count = groupManager.getMemberWarningCount(groupQQ, member.qq)
        if count >= self.maxWarningCount:
            result += u"%s 超过警告次数%d次, 正在执行裁决......\n" % (member.get_name(), self.maxWarningCount)
            result += self.qqClient.delete_group_member(groupQQ, member.qq)
            result += "\n"

        return result

    def getGroupManger(self, groupQQ):

        if self.groupInstances.has_key(groupQQ):
            groupManager = self.groupInstances[groupQQ]
        else:
            groupManager = GroupManager(groupQQ)
            self.groupInstances[groupQQ] = groupManager
        return groupManager

    def handleRequestJoinMsg(self, msg):

        groupQQ = msg.group.qq
        memberName = msg.requestName
        memberQQ = msg.requestQQ
        groupManager = self.getGroupManger(groupQQ)
        if str(memberQQ) in groupManager.blackQQ and groupManager.balckSwitch:
            msg.reject(u"你在本群黑名单之上，禁止加入")
            self.qqClient.send_group_msg(groupQQ, u"%s(%s)企图加入本群，但由于此人乃黑名单上之物，已拒绝之！" % (memberName, memberQQ))
        else:
            if groupManager.autoVerify == 1:
                msg.allow()
            elif groupManager.autoVerify == 0:
                msg.reject()

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember

        groupManager = self.getGroupManger(groupQQ)

        """
        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = groupplugin.GroupPlugin(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin
        """

        result = ""

        if groupManager.checkShuabing(member.qq, msg.msg) and groupManager.shuabingDetect and not member.isAdmin:
            result += u"%s 刷屏， 警告一次！警告超过%d次将被踢出本群\n" % (member.get_name(), self.maxWarningCount)
            groupManager.setMemberWarningCount(groupQQ, member.qq, 1, True)
            result += self.checkWarningCount(groupManager, groupQQ, member)

        if groupManager.checkSensitiveWord(groupQQ, msg.msg) and not member.isAdmin:
            result += u"%s 发言有敏感词， 警告一次！警告超过%d次将被踢出本群\n" % (member.get_name(), self.maxWarningCount)
            groupManager.setMemberWarningCount(groupQQ, member.qq, 1, True)
            result += self.checkWarningCount(groupManager, groupQQ, member)

        if groupManager.checkProhibitedWord(groupQQ, msg.msg) and not member.isAdmin:
            result += u"%s 发言有违禁词，正在执行裁决......\n " % member.get_name()
            result += self.qqClient.delete_group_member(groupQQ, member.qq)
        
        #命令判断
        if self.cmdClrScreen.az(msg.msg):
            if member.isAdmin:
                result += u"- \t\n\n\t -"*800 + u"清屏完毕~\n"
            else:
                result += u"%s 您不是管理员，无权操作！\n" % (member.get_name())
        elif self.cmdKick.az(msg.msg):
            if member.isAdmin:
                param = self.cmdKick.get_param_list()[0]
                if param.isdigit():
                    result += self.qqClient.delete_group_member(groupQQ, int(param))
                    #print result
                else:
                    result += u"QQ号不正确，踢人失败!\n"
            else:
                result += u"%s 您不是管理员，无法踢人！\n" % (member.get_name())
        elif self.cmdMyWarningCount.az(msg.msg):
            count = groupManager.getMemberWarningCount(groupQQ, member.qq)
            if count == None:
                warningCount = 0
            else:
                warningCount = count
            result += u"%s (%d)的警告次数为 %d\n" % (member.get_name(), member.qq, warningCount)

        elif self.cmdGetSensitiveWords.az(msg.msg):
            result += u"当前敏感词：\n"
            words = groupManager.getSensitiveWords(groupQQ)
            words = "\n".join(words)
            result += words

        elif self.cmdGetProhibitedWords.az(msg.msg):
            result += u"当前违禁词：\n"
            words = groupManager.getProhibitedWords(groupQQ)
            words = "\n".join(words)
            result += words

        elif self.cmdAddSensitiveWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdAddSensitiveWords.get_param_list()
                for word in params:
                    groupManager.addSensitiveWord(groupQQ, word)
                result += u"敏感词添加完成\n"
            else:
                result += u"%s 您不是管理员，无法添加敏感词！\n" % (member.get_name())

        elif self.cmdDelSensitiveWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdDelSensitiveWords.get_param_list()
                for word in params:
                    groupManager.delSensitiveWord(groupQQ, word)
                result += u"敏感词删除完成\n"
            else:
                result += u"%s 您不是管理员，无法删除敏感词！\n" % (member.get_name())

        elif self.cmdAddProhibitedWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdAddProhibitedWords.get_param_list()
                for word in params:
                    groupManager.addProhibitedWord(groupQQ, word)
                result += u"违禁词添加完成\n"
            else:
                result += u"%s 您不是管理员，无法添加违禁词！\n" % (member.get_name())

        elif self.cmdDelProhibitedWords.az(msg.msg):
            if member.isAdmin:
                params = self.cmdDelProhibitedWords.get_param_list()
                for word in params:
                    groupManager.delProhibitedWord(groupQQ, word)
                result += u"违禁词删除完成\n"
            else:
                result += u"%s 您不是管理员，无法删除违禁词！\n" % (member.get_name())

        elif self.cmdOtherWarningCount.az(msg.msg):
            if member.isAdmin:
                param = self.cmdOtherWarningCount.get_param_list()[0]
                warningCount = groupManager.getMemberWarningCount(groupQQ, param)
                result += u"%s 的警告次数为 %d\n" % (param, warningCount)
            else:
                result += u"%s 您不是管理员，无权查看!\n" % (member.get_name())

        elif self.cmdClearWarningCount.az(msg.msg):
            if member.isAdmin:
                param = self.cmdClearWarningCount.get_param_list()[0]
                warningCount = groupManager.getMemberWarningCount(groupQQ, param)
                #print warningCount
                if warningCount:
                    groupManager.setMemberWarningCount(groupQQ, param, 0, False)
                result += u"%s的警告次数已经清零\n" % (param)
            else:
                result += u"%s 您不是管理员，无权清零警告次数!\n" % (member.get_name())

        elif self.cmdOpenShuabingDetect.az(msg.msg):
            if member.isAdmin:
                groupManager.setShuabingDetect(groupQQ, 1)
                result += u"刷屏检测已开启\n"
            else:
                result += u"%s 您不是管理员，无权开启刷屏检测!\n" % (member.get_name())
        elif self.cmdCloseShuabingDetect.az(msg.msg):
            if member.isAdmin:
                groupManager.setShuabingDetect(groupQQ, 0)
                result += u"刷屏检测已关闭\n"
            else:
                result += u"%s 您不是管理员，无权关闭刷屏检测!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxRows.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxRows.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏行数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxRows(groupQQ, int(param))
                    result += u"刷屏行数设置成功!\n"

            else:
                result += u"%s 您不是管理员，无权设置刷屏行数!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxWords.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxWords.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏字数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxWords(groupQQ, int(param))
                    result += u"刷屏字数设置成功!"

            else:
                result += u"%s 您不是管理员，无权设置刷屏字数!\n" % (member.get_name())

        elif self.cmdSetShuabingMaxContinuous.az(msg.msg):

            if member.isAdmin:
                param = self.cmdSetShuabingMaxContinuous.get_param_list()[0]
                if not param.isdigit():
                    result += u"刷屏连续次数只能设置为数字!\n"
                else:
                    groupManager.setShuabingMaxContinuous(groupQQ, int(param))
                    result += u"刷屏连续次数设置成功!"
            else:
                result += u"%s 您不是管理员，无权设置刷屏连续次数!\n" % (member.get_name())

        elif self.cmdShuabingStatus.az(msg.msg):
            if member.isAdmin:
                status = u"开启" if groupManager.shuabingDetect else u"关闭"
                result += u"刷屏检测状态：%s \n发言行数达到%d行视为刷屏\n发言字数达到%d字视为刷屏\n同一人连续发言相同内容%d次视为刷屏\n" % (status, groupManager.shuabingMaxRows, groupManager.shuabingMaxWords, groupManager.shuabingMaxContinuous)
            else:
                result += u"%s 您不是管理员，无权查看刷屏检测状态!\n" % (member.get_name())

        # 黑名单
        elif self.cmdAddBlackQQ.az(msg.msg):

            if member.isAdmin:
                param = self.cmdAddBlackQQ.get_param_list()[0]
                if not param.isdigit():
                    result += u"QQ号只能为数字!\n"
                else:
                    groupManager.addBlackQQ(groupQQ, param)
                    result += u"加黑QQ%s成功!" % param
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())
                
        elif self.cmdDelBlackQQ.az(msg.msg):

            if member.isAdmin:
                param = self.cmdDelBlackQQ.get_param_list()[0]
                if not param.isdigit():
                    result += u"QQ号只能为数字!\n"
                else:
                    groupManager.delBlackQQ(groupQQ, param)
                    result += u"解黑QQ%s成功!" % param
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdGetBlackQQ.az(msg.msg):

            if member.isAdmin:
                blackList = groupManager.getBlackQQ(groupQQ)

                result += u"当前黑名单：\n" + "\n".join(blackList)
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())
        
        # 加群审核
        elif self.cmdAutoAllow.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 1)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdAutoReject.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 0)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdAutoIgnore.az(msg.msg):

            if member.isAdmin:
                groupManager.setAutoVerify(groupQQ, 2)
                result += u"设置成功!"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdGetVerifyType.az(msg.msg):

            if member.isAdmin:
                result += u"当前加群审核方式："
                if groupManager.autoVerify == 0:
                    result += u"自动拒绝"
                elif groupManager.autoVerify == 1:
                    result += u"自动同意"
                elif groupManager.autoVerify == 2:
                    result += u"自动忽略"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdOpenBlackQQ.az(msg.msg):

            if member.isAdmin:
                groupManager.setBlackSwitch(groupQQ, 1)
                result += u"黑名单已开启"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())

        elif self.cmdCloseBlackQQ.az(msg.msg):

            if member.isAdmin:
                groupManager.setBlackSwitch(groupQQ, 0)
                result += u"黑名单已关闭"
            else:
                result += u"%s 您不是管理员，无权操作!\n" % (member.get_name())



        if result:
            msg.reply(result)
            msg.destroy()



# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addRequestJoinGroupEvent(MsgEvent(event.handleRequestJoinMsg))

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/group_manager/__init__.py
