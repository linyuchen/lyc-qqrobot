# -*- coding:UTF-8 -*-

import plugin
import super_plugin
from cmdaz import CMD


__author__ = u"linyuchen"
__doc__ = u"插件改为django程序"


class MyEvent(plugin.webqqsdk.msgevent.MsgEvent):

    name = u"super_plugin"

    def main(self, msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        :param msg: Message
        """

        group_action = super_plugin.GroupAction(msg.group.qq, msg.groupMember.qq)
        group_action.group_user.add_point(group_action.group_setting.talk_point)
        result = ""
        if CMD(u"签到").az(msg.msg):
            result = group_action.sign()

        if result:
            msg.reply(result)
            msg.destroy()


class Plugin(plugin.QQPlugin):
    """
    此类必须存在
    """

    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件%s被安装了" % MyEvent.name

    def uninstall(self):

        print u"插件%s被卸载了" % MyEvent.name

