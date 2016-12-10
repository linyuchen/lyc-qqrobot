#coding=UTF8

"""
数码查询插件
"""
import phoneimei
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = phoneimei.PhoneImei()


class MyEvent(MsgEvent):
    __doc__ = u"""
    手机串号查询
    命令：手机串号 +空格+ 关键字
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"手机串号"
        self.cmd = CMD(u"手机串号", param_len=1)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        if self.cmd.az(msg.msg):
            param = self.cmd.get_original_param()
            result = mod(param)
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"手机串号"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
