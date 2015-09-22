#coding=UTF8

import groupplugin
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
    群命令开关
    """
    def __init__(self):

        self.name = u"group_cmd_switch"
        self.cmdClose = CMD(u"关闭命令", hasParam = True)
        self.cmdOpen = CMD(u"开启命令", hasParam = True)
        self.cmdGetClosed = CMD(u"已关闭命令")
        self.cmdAddWhite = CMD(u"加命令白名单", hasParam = True)
        self.cmdDelWhite = CMD(u"删命令白名单", hasParam = True)
        self.cmdGetWhite = CMD(u"命令白名单")
        self.cmdShutdown = CMD(u"关机")
        self.cmdStartup = CMD(u"开机")

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember


        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = groupplugin.GroupPlugin(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin

        #groupPlugin.add_point(groupQQ, member.qq, member.getName())
        result = ""
        if self.cmdClose.az(msg.msg):
            if member.isAdmin:
                param = self.cmdClose.getParamList()
                for p in param:
                    result += u"%s 命令已经关闭\n" % (p)
                    groupPlugin.addClosedCmd(p)
            else:
                result += u"%s 您不是管理员，无权操作 \n" % member.getName()

        elif self.cmdOpen.az(msg.msg):
            if member.isAdmin:
                param = self.cmdOpen.getParamList()
                for p in param:
                    result += u"%s 命令已经开启\n" % (p)
                    groupPlugin.delClosedCmd(p)
            else:
                result += u"%s 您不是管理员，无权操作 \n" % member.getName()

        elif self.cmdGetClosed.az(msg.msg):

            result += u"已经被关闭的命令：\n" + "\n".join(groupPlugin.closedCmd)

        # 白名单
        elif self.cmdGetWhite.az(msg.msg):

            result += u"白名单命令：\n" + "\n".join(groupPlugin.whiteCmd)

        elif self.cmdAddWhite.az(msg.msg):

            if member.isAdmin:
                param = self.cmdAddWhite.getParamList()
                for p in param:
                    result += u"%s 命令已加入白名单\n" % (p)
                    groupPlugin.addWhiteCmd(p)

        elif self.cmdDelWhite.az(msg.msg):

            if member.isAdmin:
                param = self.cmdDelWhite.getParamList()
                for p in param:
                    result += u"%s 命令已从白名单中删除\n" % (p)
                    groupPlugin.delWhiteCmd(p)

        # 开关机
        elif self.cmdShutdown.az(msg.msg):
            if member.isAdmin:
                result += u"关机了。。。小的告退了，拜拜\n"
                groupPlugin.setShutdownSwitch(1)
            else:
                result += u"%s 您不是管理员，无权操作 \n" % member.getName()

        elif self.cmdStartup.az(msg.msg):
            if member.isAdmin:
                result += u"噢耶！开机咯~~~\n"
                groupPlugin.setShutdownSwitch(0)
            else:
                result += u"%s 您不是管理员，无权操作 \n" % member.getName()


        # 检测命令
        if not result:
            isWhite = False
            msgContent = msg.msg.strip()
            for w in groupPlugin.whiteCmd:
                if msgContent.startswith(w):
                    isWhite = True
                    break
            if not isWhite:
                if groupPlugin.shutdownSwitch:
                    msg.destroy()
                    return
                for c in groupPlugin.closedCmd:
                    if msgContent.startswith(c):
                        msg.destroy()
                        return
        """
        elif self.nextCmd.az(msg.msg):
            result = zhidao.getNextQuestions()
            
            msg.reply(result + self.note)
            msg.destroy()
        elif self.answerCmd.az(msg.msg):
            result = zhidao.getAnswer(self.answerCmd.getParamList()[0])
        """
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



