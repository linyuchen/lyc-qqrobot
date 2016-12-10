# coding=UTF8

"""
翻译插件
"""
import baidutranslator
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = baidutranslator.Translator()


class MyEvent(MsgEvent):
    __doc__ = u"""
    翻译
    命令：译成中 +空格+ 原文
          译成英 +空格+ 原文
          译成日 +空格+ 原文
          译成法 +空格+ 原文
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"翻译"
        self.cmdTr2zh = CMD(u"译成中", param_len=1)
        self.cmdTr2en = CMD(u"译成英", param_len=1)
        self.cmdTr2jp = CMD(u"译成日", param_len=1)
        self.cmdTr2fr = CMD(u"译成法", param_len=1)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmdTr2zh.az(msg.msg):
            param = self.cmdTr2zh.get_original_param()
            result = mod(param, "zh")
        elif self.cmdTr2fr.az(msg.msg):
            param = self.cmdTr2fr.get_original_param()
            result = mod(param, "fra")
        elif self.cmdTr2en.az(msg.msg):
            param = self.cmdTr2en.get_original_param()
            result = mod(param, "en")
        elif self.cmdTr2jp.az(msg.msg):
            param = self.cmdTr2jp.get_original_param()
            result = mod(param, "jp")

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"翻译"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
