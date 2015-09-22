#coding=UTF8

"""
短网址插件
"""
import sinashorturl
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = sinashorturl.ShortUrl()

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    新浪短网址生成与还原
    命令：短网址 + 空格 + 长网址(或短网址)
    """
    def __init__(self):

        self.name = u"新浪短网址"
        self.cmd= CMD(u"短网址", hasParam=True)

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmd.az(msg.msg):
            param = self.cmd.getParamList()[0]
            if param.startswith("http://t.cn"):
                result = u"短网址还原结果："
                result += mod.expand(param)
            else:
                result = u"短网址生成结果："
                result += mod.make(param)

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



