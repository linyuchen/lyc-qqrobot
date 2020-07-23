# coding=UTF8

import cmdaz
import plugin
import game24point
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


class Game(GroupPointAction, game24point.Game):
    
    def __init__(self):
        super(Game, self).__init__()


class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏：21点
    """
    
    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_gamble"
        self.cmdAnswer = CMD(u"答24点", param_len=1)
        self.cmdStart = CMD(u"24点")
        self.groupInstances = {}  # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def get_game_instance(self, group_qq):

        if group_qq in self.groupInstances:
            group_plugin = self.groupInstances[group_qq]
        else:
            group_plugin = Game()
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
            result += game.start_game(msg.reply)
            result += u"\n\n发送 “答24点 +空格+ 式子” 对24点游戏答题，加减乘除对应 + - * /,支持括号，如答24点 3*8*(2-1)\n"

        elif self.cmdAnswer.az(msg.msg):

            param = self.cmdAnswer.get_original_param()
            result += game.judge(group_qq, member.qq, member.get_name(), param)
 
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"24点群游戏"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME
