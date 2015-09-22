#coding=UTF8

import cmdaz
import plugin
import game24point
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
game24 = game24point.Game

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏：21点
    """
    def __init__(self):

        self.name = u"group_gamble"
        self.cmdAnswer = CMD(u"答24点", hasParam=True)
        self.cmdStart = CMD(u"24点")
        self.groupInstances = {} # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def getGameInstance(self, groupQQ):

        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = game24()
            self.groupInstances[groupQQ] = groupPlugin

        return groupPlugin

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember

        game = self.getGameInstance(groupQQ)


        result = ""
        if self.cmdStart.az(msg.msg):
            result += game.start_game(msg.reply)
            result += u"\n\n发送 “答24点 +空格+ 式子” 对24点游戏答题，加减乘除对应 + - * /,支持括号，如答24点 3*8*(2-1)\n"

        elif self.cmdAnswer.az(msg.msg):

            param = self.cmdAnswer.getOriginalParam()
            result += game.judge(groupQQ, member.qq, member.getName(), param)
 
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



