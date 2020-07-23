# coding=UTF8

"""
数码查询插件
"""
import baidusoftware
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = baidusoftware.Software()


class MyEvent(MsgEvent):
    __doc__ = u"""
    软件下载
    命令：电脑软件 +空格+ 关键字
          安卓软件 +空格+ 关键字
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"软件下载"
        self.cmdWindows = CMD(u"电脑软件", param_len=1)
        self.cmdAndroid = CMD(u"安卓软件", param_len=1)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""

        if self.cmdWindows.az(msg.msg):
            param = self.cmdWindows.get_original_param()
            result = mod.windows(param)
        elif self.cmdAndroid.az(msg.msg):
            param = self.cmdAndroid.get_original_param()
            result = mod.android(param)
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"软件下载"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
