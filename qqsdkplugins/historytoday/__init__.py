#coding=UTF8

"""
快递查询插件
"""
import historytoday
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
historytoday = historytoday.HistoryToday()


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    查询历史今天
    命令：历史今天
    """

    def __init__(self):
        super(MyEvent, self).__init__()

        self.name = "historytoday"
        self.cmd = CMD(u"历史今天")

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        if self.cmd.az(msg.msg):
            result = historytoday()
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"历史今天"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME
