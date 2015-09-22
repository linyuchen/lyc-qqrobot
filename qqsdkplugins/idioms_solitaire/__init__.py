#coding=UTF8

import idiomssolitaire
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
    成语接龙，只能群里使用
    """
    def __init__(self):

        self.name = u"group_point"
        self.cmdStart = CMD(u"成语接龙")
        self.cmdJoin = CMD(u"接龙", hasParam = True)

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
            groupPlugin = idiomssolitaire.IdiomsSolitaire()
            self.groupInstances[groupQQ] = groupPlugin

        result = ""
        if self.cmdStart.az(msg.msg):
            result = groupPlugin.start_game(groupQQ, msg.reply)

        elif self.cmdJoin.az(msg.msg):
            result = groupPlugin.judge_idiom(groupQQ, member.qq, member.getName(), self.cmdJoin.getOriginalParam())


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



