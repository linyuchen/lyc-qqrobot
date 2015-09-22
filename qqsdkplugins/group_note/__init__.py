#coding=UTF8

import note_manager
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群提示：
        新人提示
        退群提示
        管理变更提示
    """
    def __init__(self):

        self.name = u"group_note"
        self.cmdGetJoinNote = CMD(u"查看入群提醒")
        self.cmdOpenJoinNote = CMD(u"开启入群提醒")
        self.cmdCloseJoinNote = CMD(u"关闭入群提醒")
        self.cmdSetJoinNote = CMD(u"设置入群提醒", hasParam=True)

        self.cmdGetExitNote = CMD(u"查看退群提醒")
        self.cmdOpenExitNote = CMD(u"开启退群提醒")
        self.cmdCloseExitNote = CMD(u"关闭退群提醒")
        self.cmdSetExitNote = CMD(u"设置退群提醒", hasParam=True)

        self.cmdGetKickNote = CMD(u"查看踢人提醒")
        self.cmdOpenKickNote = CMD(u"开启踢人提醒")
        self.cmdCloseKickNote = CMD(u"关闭踢人提醒")
        self.cmdSetKickNote = CMD(u"设置踢人提醒", hasParam=True)

        self.cmdGetAdminChangeNote = CMD(u"查看管理变更提醒")
        self.cmdOpenAdminChangeNote = CMD(u"开启管理变更提醒")
        self.cmdCloseAdminChangeNote = CMD(u"关闭管理变更提醒")
        #self.cmdMyPoint = CMD(u"我的活跃度")
        #self.cmdTransferPoint = CMD(u"转活跃度", hasParam=True)
        #self.cmdPointRank = CMD(u"活跃度排名")

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def getGroupPlugin(self, groupQQ):

        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = note_manager.Manager(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin

        return groupPlugin

    def sendJoinNote(self, msg):

        group = msg.group
        member = msg.groupMember

        groupPlugin = self.getGroupPlugin(group.qq)
        note = groupPlugin.joinNote
        if groupPlugin.joinNoteSwitch:
            note = note.replace("{name}", member.getName()).replace("{qq}", str(member.qq))
            self.qqClient.sendMsg2Group(group.qq, note)
    
    def sendExitNote(self, msg):

        group = msg.group

        groupPlugin = self.getGroupPlugin(group.qq)
        note = groupPlugin.exitNote
        if groupPlugin.exitNoteSwitch:
            note = note.replace("{name}", msg.memberName).replace("{qq}", str(msg.memberQQ))
            self.qqClient.sendMsg2Group(group.qq, note)

    def sendAdminChangeNote(self, msg):

        group = msg.group
        member = msg.groupMember

        groupPlugin = self.getGroupPlugin(group.qq)
        #note = groupPlugin.
        if groupPlugin.adminChangeNoteSwitch:
            #note = note.replace("{name}", member.getName()).replace("{qq}", str(member.qq))
            note = u"%s(%d)被%s了管理员" % (member.getName(), member.qq, u"设置成" if member.isAdmin else u"取消")
            self.qqClient.sendMsg2Group(group.qq, note)

    def sendKickNote(self, msg):

        group = msg.group
        admin = msg.groupAdmin

        groupPlugin = self.getGroupPlugin(group.qq)
        note = groupPlugin.kickNote
        if groupPlugin.kickNoteSwitch:
            note = note.replace("{name}", msg.memberName).replace("{qq}", str(msg.memberQQ))
            note = note.replace("{admin_name}", admin.getName()).replace("{admin_qq}", str(admin.qq))
            self.qqClient.sendMsg2Group(group.qq, note)


    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember


        groupPlugin = self.getGroupPlugin(groupQQ)

        result = ""
        if self.cmdGetJoinNote.az(msg.msg):
            result += u"当前新人入群提醒状态: %s" % ( u"开启" if groupPlugin.joinNoteSwitch else u"关闭")
            result += u"\n入群提示语：%s \n" % groupPlugin.joinNote
        elif self.cmdOpenJoinNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setJoinNoteSwitch(groupQQ, 1)
                result += u"新人入群提醒已开启！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdCloseJoinNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setJoinNoteSwitch(groupQQ, 0)
                result += u"新人入群提醒已关闭！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdSetJoinNote.az(msg.msg):
            if member.isAdmin:
                param = self.cmdSetJoinNote.getOriginalParam()
                groupPlugin.setJoinNote(groupQQ, param)
                result += u"新人入群语设置完成"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        # 退群
        if self.cmdGetExitNote.az(msg.msg):
            result += u"当前成员退群提醒状态: %s" % (u"开启" if groupPlugin.exitNoteSwitch else u"关闭")
            result += u"\n入群提示语：%s \n" % groupPlugin.exitNote

        elif self.cmdOpenExitNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setExitNoteSwitch(groupQQ, 1)
                result += u"成员退群提醒已开启！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdCloseExitNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setExitNoteSwitch(groupQQ, 0)
                result += u"成员退群提醒已关闭！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdSetExitNote.az(msg.msg):
            if member.isAdmin:
                param = self.cmdSetExitNote.getOriginalParam()
                groupPlugin.setExitNote(groupQQ, param)
                result += u"成员退群语设置完成"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        # 踢人
        if self.cmdGetKickNote.az(msg.msg):
            result += u"当前踢人提醒状态: %s" % (u"开启" if groupPlugin.kickNoteSwitch else u"关闭")
            result += u"\n踢人提示语：%s \n" % groupPlugin.kickNote

        elif self.cmdOpenKickNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setKickNoteSwitch(groupQQ, 1)
                result += u"踢人提醒已开启！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdCloseKickNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setKickNoteSwitch(groupQQ, 0)
                result += u"踢人提醒已关闭！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdSetKickNote.az(msg.msg):
            if member.isAdmin:
                param = self.cmdSetKickNote.getOriginalParam()
                groupPlugin.setKickNote(groupQQ, param)
                result += u"踢人提示语设置完成"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        # 管理变成提醒
        if self.cmdGetAdminChangeNote.az(msg.msg):
            result += u"当前管理变更提醒状态: %s" % (u"开启" if groupPlugin.adminChangeNoteSwitch else u"关闭")

        elif self.cmdOpenAdminChangeNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setAdminChangeNoteSwitch(groupQQ, 1)
                result += u"管理变更提醒已开启！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())

        elif self.cmdCloseAdminChangeNote.az(msg.msg):
            if member.isAdmin:
                groupPlugin.setAdminChangeNoteSwitch(groupQQ, 0)
                result += u"管理变更提醒已关闭！"
            else:
                result += u"%s 您不是管理员，无权设置" % (member.getName())


        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addNewGroupMemberEvent(MsgEvent(event.sendJoinNote))
        self.qqClient.addGroupMemberExitEvent(MsgEvent(event.sendExitNote))
        self.qqClient.addGroupRemoveMemberEvent(MsgEvent(event.sendKickNote))
        self.qqClient.addGroupAdminChangeEvent(MsgEvent(event.sendAdminChangeNote))

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



