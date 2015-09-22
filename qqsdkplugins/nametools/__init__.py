#coding=UTF8

"""

"""
import nametools
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = nametools.Tools()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    姓名测试与姓名配对
    命令：姓名测试 +空格+ 姓名
          配对（或姓名配对） + 空格 + 姓名 + 空格 + 姓名
    """
    def __init__(self):

        self.name = u"姓名工具"
        self.cmdNameTest = CMD(u"姓名测试", hasParam=True)
        self.cmdNamePairing1 = CMD(u"姓名配对", hasParam=True)
        self.cmdNamePairing2 = CMD(u"配对", hasParam=True)

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmdNameTest.az(msg.msg):
            param = self.cmdNameTest.getOriginalParam()
            result = mod.test(param)
        elif self.cmdNamePairing1.az(msg.msg) or self.cmdNamePairing2.az(msg.msg):

            param = self.cmdNamePairing1.getOriginalParam()
            result = mod.pairing(param)

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



