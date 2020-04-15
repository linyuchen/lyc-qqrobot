# coding=UTF8

import cmdaz
import plugin
import gamble
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


class Game(GroupPointAction, gamble.Gamble):
    def __init__(self):
        gamble.Gamble.__init__(self)
        GroupPointAction.__init__(self)


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏，赌博
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_gamble"
        self.cmdGamble = CMD(u"赌博", param_len=1)
        self.game = Game()

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember

        result = ""
        if self.cmdGamble.az(msg.msg):
            param = self.cmdGamble.get_param_list()[0]
            result += self.game.gamble(group_qq, member.qq, member.get_name(), param)

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"群内赌博"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



