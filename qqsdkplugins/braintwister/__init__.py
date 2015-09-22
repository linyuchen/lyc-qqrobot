#coding=UTF8

"""
"""
import braintwister
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = braintwister.BrainTwister()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    脑筋急转弯 
    命令：急转弯 或 脑筋急转弯
          急转弯答案 + 空格 + 序号
    """
    def __init__(self):

        self.name = "braintwister"
        self.cmd1 = CMD(u"急转弯")
        self.cmd2 = CMD(u"脑筋急转弯")
        self.cmdAnswer = CMD(u"急转弯答案", hasParam=True)

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmd1.az(msg.msg) or self.cmd2.az(msg.msg):
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



