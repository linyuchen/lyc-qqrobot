# coding=UTF8

import cmdaz
import plugin
import lottery
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


class Lottery(GroupPointAction, lottery.Lottery):
    def __init__(self):
        super(Lottery, self).__init__()


lottery = Lottery()


# 新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏，抽奖
    """
    
    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_lottery"
        self.cmdLottery = CMD(u"抽奖", param_len=1)

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember

        result = ""
        if self.cmdLottery.az(msg.msg):
            param = self.cmdLottery.get_param_list()[0]
            result += lottery.lottery(group_qq, member.qq, member.get_name(), param)

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    NAME = u"抽奖群游戏"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.NAME

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.NAME
