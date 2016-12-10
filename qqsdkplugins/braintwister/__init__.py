#coding=UTF8

"""
"""
import braintwister
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk  # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = braintwister.BrainTwister()


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    脑筋急转弯 
    命令：急转弯 或 脑筋急转弯
          急转弯答案 + 空格 + 序号
    """

    def __init__(self):
        super(MyEvent, self).__init__()
        self.name = "braintwister"
        self.cmds = [
            CMD(u"急转弯", handle_func=mod.getRandomOne),
            CMD(u"脑筋急转弯", handle_func=mod.getRandomOne),
            CMD(u"急转弯答案", param_len=1, handle_func=mod.getAnswer)
        ]

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        for cmd in self.cmds:
            result = cmd.handle(msg.msg)
            if result:
                msg.reply(result)
                msg.destroy()
                break


#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"脑筋急转弯"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



