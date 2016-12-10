# coding=UTF8

import cmdaz
import idiomssolitaire
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    成语接龙，只能群里使用
    """
    
    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_point"
        self.cmdStart = CMD(u"成语接龙")
        self.cmdJoin = CMD(u"接龙", param_len=1)

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {}  # key qq, value instance

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember

        if group_qq in self.groupInstances:
            group_plugin = self.groupInstances[group_qq]
        else:
            group_plugin = idiomssolitaire.IdiomsSolitaire()
            self.groupInstances[group_qq] = group_plugin

        result = ""
        if self.cmdStart.az(msg.msg):
            result = group_plugin.start_game(group_qq, msg.reply)

        elif self.cmdJoin.az(msg.msg):
            result = group_plugin.judge_idiom(group_qq, member.qq, member.getName(), self.cmdJoin.get_original_param())

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"猜谜游戏"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



