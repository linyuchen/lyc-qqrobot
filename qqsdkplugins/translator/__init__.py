#coding=UTF8

"""
翻译插件
"""
import baidutranslator
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = baidutranslator.Translator()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    翻译
    命令：译成中 +空格+ 原文
          译成英 +空格+ 原文
          译成日 +空格+ 原文
          译成法 +空格+ 原文
    """
    def __init__(self):

        self.name = u"翻译"
        self.cmdTr2zh = CMD(u"译成中", hasParam=True)
        self.cmdTr2en = CMD(u"译成英", hasParam=True)
        self.cmdTr2jp = CMD(u"译成日", hasParam=True)
        self.cmdTr2fr = CMD(u"译成法", hasParam=True)

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmdTr2zh.az(msg.msg):
            param = self.cmdTr2zh.getOriginalParam()
            result = mod(param, "zh")
        elif self.cmdTr2fr.az(msg.msg):
            param = self.cmdTr2fr.getOriginalParam()
            result = mod(param, "fra")
        elif self.cmdTr2en.az(msg.msg):
            param = self.cmdTr2en.getOriginalParam()
            result = mod(param, "en")
        elif self.cmdTr2jp.az(msg.msg):
            param = self.cmdTr2jp.getOriginalParam()
            result = mod(param, "jp")

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



