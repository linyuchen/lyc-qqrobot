# coding=UTF8

import cmdaz
import plugin
import rob
from superplugins import GroupPointAction
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


class Rob(GroupPointAction, rob.Rob):

    def __init__(self):
        super(Rob, self).__init__()


rob = rob.Rob()


class MyEvent(MsgEvent):
    __doc__ = u"""
    群游戏，抢劫
    """

    def __init__(self):

        super(MyEvent, self).__init__()
        self.name = u"group_gamble"
        self.cmdRob = CMD(u"抢劫", param_len=1)

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        group_qq = msg.group.qq
        member = msg.groupMember
        result = ""
        if self.cmdRob.az(msg.msg):
            param = self.cmdRob.get_param_list()[0]
            result += rob.rob(group_qq, member.qq, member.getName(), param)

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"群内抢劫"

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name



