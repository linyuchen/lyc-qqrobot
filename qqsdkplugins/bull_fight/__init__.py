# coding=UTF8

import cmdaz
import plugin
import bullfight
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


class BullGame(GroupPointAction, bullfight.BullFight):

    def __init__(self, group_qq, qq_client):
        bullfight.BullFight.__init__(self, group_qq, qq_client)
        GroupPointAction.__init__(self)


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏：斗牛
    """
    
    def __init__(self):
        super(MyEvent, self).__init__()
        self.name = u"group_gamble"
        self.cmdStart = CMD(u"斗牛", param_len=1)
        self.groupInstances = {}  # key groupQQ, value instance

        # 不同的QQ群用不同的实例， 因为一个人可以在多个群里

    def get_game_instance(self, group_qq):

        if group_qq in self.groupInstances:
            group_plugin = self.groupInstances[group_qq]
        else:
            group_plugin = BullGame(group_qq, self.qqClient)
            self.groupInstances[group_qq] = group_plugin

        return group_plugin

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember

        __game = self.get_game_instance(group_qq)

        result = ""
        if self.cmdStart.az(msg.msg):
            param = self.cmdStart.get_param_list()[0]
            result += __game.start_game(member.qq, member.getName(), msg.reply, param)

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"斗牛群游戏"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME



