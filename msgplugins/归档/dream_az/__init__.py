# coding=UTF8

"""
"""
import dreams
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = dreams.Dreams()

# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    解梦分析
    命令：解梦
          解梦分析 + 空格 + 序号
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = "dream_analysis"
        self.cmd1 = CMD(u"解梦", param_len=1)
        self.cmdAnswer = CMD(u"解梦分析", param_len=1)
        self.note = u"""
发送 “解梦分析+空格+序号” 查看解梦分析，如：解梦分析 1
        """

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        result = ""
        if self.cmd1.az(msg.msg):
            param = self.cmd1.get_original_param()
            result = mod.ask(param)
            result += self.note
        elif self.cmdAnswer.az(msg.msg):
            param = self.cmdAnswer.get_param_list()[0]
            result = mod.getAnswer(param)
        if result:
            msg.reply(result)
            msg.destroy()

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin


class Plugin(QQPlugin):

    NAME = u"解梦"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



