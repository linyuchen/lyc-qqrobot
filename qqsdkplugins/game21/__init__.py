# coding=UTF8

import cmdaz
import plugin
import game21point
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
Game21 = game21point.Game


class Game(GroupPointAction, Game21):
    def __init__(self, qq_client):
        GroupPointAction.__init__(self)
        Game21.__init__(self, qq_client)


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏：21点
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_gamble"
        self.cmdStart = CMD(u"21点", param_len=1)
        self.cmdUpdate = CMD(u"21点换牌")
        self.groupInstances = {}  # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def get_game_instance(self, group_qq):

        if group_qq in self.groupInstances:
            group_plugin = self.groupInstances[group_qq]
        else:
            group_plugin = Game(self.qqClient)
            self.groupInstances[group_qq] = group_plugin

        return group_plugin

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember

        game = self.get_game_instance(group_qq)

        result = ""
        if self.cmdStart.az(msg.msg):
            param = self.cmdStart.get_param_list()[0]
            result += game.start_game(group_qq, member.qq, member.get_name(), param, msg.reply)
            result += u"\n\n发送“21点换牌”可以换牌，换牌需要下注的十分之一费用\n"
        elif self.cmdUpdate.az(msg.msg):

            result += game.update_poker_list(group_qq, member.qq, member.get_name())
 
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"21点群游戏"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



