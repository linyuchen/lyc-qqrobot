# coding=UTF8

"""
"""
import riddle
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = riddle.Riddle()


class MyEvent(MsgEvent):
    __doc__ = u"""
    谜语
    命令：谜语
          谜底 + 空格 + 序号
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = "riddle"
        self.cmd1 = CMD(u"谜语")
        self.cmdAnswer = CMD(u"谜底", param_len=1)

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmd1.az(msg.msg):
            result = mod.get_random_one()
        elif self.cmdAnswer.az(msg.msg):
            param = self.cmdAnswer.get_param_list()[0]
            result = mod.get_answer(param)
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"猜谜"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name
