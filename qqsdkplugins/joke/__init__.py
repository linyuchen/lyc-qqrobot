#coding=UTF8

"""
快递查询插件
"""
import joke
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = joke.Joke()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    看笑话
    命令：笑话
    """
    def __init__(self):

        self.name = "joke"
        self.cmd = CMD(u"笑话")

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        if self.cmd.az(msg.msg):
            #param = self.cmd.getParamList()[0]
            #print param
            result = mod.getRandomOne()
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



