#coding=UTF8

import cmdaz
import plugin
import gamble
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
gamble =gamble.Gamble()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏，赌博
    """
    def __init__(self):

        self.name = u"group_gamble"
        self.cmdGamble = CMD(u"赌博", hasParam=True)

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember



        result = ""
        if self.cmdGamble.az(msg.msg):
            param = self.cmdGamble.getParamList()[0]
            result += gamble.gamble(groupQQ, member.qq, member.getName(), param)

 
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



