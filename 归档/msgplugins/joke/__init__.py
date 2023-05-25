# coding=UTF8

"""
快递查询插件
"""
import joke
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = joke.Joke()


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    看笑话
    命令：笑话
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = "joke"
        self.cmd = CMD(u"笑话")

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        if self.cmd.az(msg.msg):
            result = mod.get_random_one()
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"笑话"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
