#coding=UTF8

"""
"""
import riddle
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = riddle.Riddle()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    谜语
    命令：谜语
          谜底 + 空格 + 序号
    """
    def __init__(self):

        self.name = "riddle"
        self.cmd1 = CMD(u"谜语")
        self.cmdAnswer = CMD(u"谜底", hasParam=True)

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmd1.az(msg.msg):
            #print param
            result = mod.getRandomOne()
        elif self.cmdAnswer.az(msg.msg):
            param = self.cmdAnswer.getParamList()[0]
            result = mod.getAnswer(param)
        if result:
            msg.reply(result)
            msg.destroy()

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



