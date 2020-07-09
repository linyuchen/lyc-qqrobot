#coding=UTF8

"""
快递查询插件
"""
import ID
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk  # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
ID = ID.ID()

# from webqqsdk import entity

# 新建个事件类，继承于MsgEvent


class MyEvent(MsgEvent):
    __doc__ = u"""
    身份证号码查询
    命令：身份证 +空格+ 号码
    """

    def __init__(self):
        super(MyEvent, self).__init__()

        self.name = "idcard"
        self.cmd = CMD(u"身份证", param_len=1, handle_func=ID)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = self.cmd.handle(msg.msg)
        if result:
            msg.reply(result)
            msg.destroy()

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin


class Plugin(QQPlugin):
    NAME = u"身份证查询"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



