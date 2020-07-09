<<<<<<< HEAD:qqsdkplugins/已修改/group_point/__init__.py
#coding=UTF8

import cmdaz
import groupplugin
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群积分，签到之类
    """
    def __init__(self):

        self.name = u"group_point"
        self.cmdSign = CMD(u"签到")
        self.cmdMyPoint = CMD(u"我的活跃度")
        self.cmdTransferPoint = CMD(u"转活跃度", hasParam=True)
        self.cmdPointRank = CMD(u"活跃度排名")
        self.cmdClearPoint = CMD(u"清负活跃度", hasParam=False)
        self.cmdClearOtherPoint = CMD(u"清负他人活跃度", hasParam=True)
        self.cmdGetClearPointChance = CMD(u"清负次数")

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember


        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = groupplugin.GroupPlugin(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin

        groupPlugin.add_point(member.qq, member.get_name())
        result = ""
        if self.cmdSign.az(msg.msg):
            result = groupPlugin.sign(member.qq, member.get_name())

        elif self.cmdMyPoint.az(msg.msg):
            result = groupPlugin.get_point(member.qq, member.get_name())

        elif self.cmdTransferPoint.az(msg.msg):
            param = self.cmdTransferPoint.get_original_param()
            result = groupPlugin.transfer_point(member.qq, member.get_name(), param)

        elif self.cmdPointRank.az(msg.msg):
            result = groupPlugin.get_point_rank()

        elif self.cmdClearPoint.az(msg.msg):
            aim_qq = my_qq = member.qq
            aim_nick = my_nick = member.get_name()
            result = groupPlugin.clear_point(my_qq, my_nick, aim_qq, aim_nick)

        elif self.cmdClearOtherPoint.az(msg.msg):
            param = self.cmdClearOtherPoint.get_param_list()
            my_qq = member.qq
            my_nick = member.get_name()
            aim_qq = param[0]
            aim_nick = str(aim_qq)
            if aim_qq.isdigit():
                result = groupPlugin.clear_point(my_qq, my_nick, aim_qq, aim_nick)
            else:
                result = u"对方QQ号错误"
        elif self.cmdGetClearPointChance.az(msg.msg):
            result = groupPlugin.get_clear_chance(member.qq, member.get_name())

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



=======
#coding=UTF8

import cmdaz
import groupplugin
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    群积分，签到之类
    """
    def __init__(self):

        self.name = u"group_point"
        self.cmdSign = CMD(u"签到")
        self.cmdMyPoint = CMD(u"我的活跃度")
        self.cmdTransferPoint = CMD(u"转活跃度", hasParam=True)
        self.cmdPointRank = CMD(u"活跃度排名")
        self.cmdClearPoint = CMD(u"清负活跃度", hasParam=False)
        self.cmdClearOtherPoint = CMD(u"清负他人活跃度", hasParam=True)
        self.cmdGetClearPointChance = CMD(u"清负次数")

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样
        self.groupInstances = {} # key qq, value instance

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        groupQQ = msg.group.qq
        member = msg.groupMember


        if self.groupInstances.has_key(groupQQ):
            groupPlugin = self.groupInstances[groupQQ]
        else:
            groupPlugin = groupplugin.GroupPlugin(groupQQ)
            self.groupInstances[groupQQ] = groupPlugin

        groupPlugin.add_point(member.qq, member.get_name())
        result = ""
        if self.cmdSign.az(msg.msg):
            result = groupPlugin.sign(member.qq, member.get_name())

        elif self.cmdMyPoint.az(msg.msg):
            result = groupPlugin.get_point(member.qq, member.get_name())

        elif self.cmdTransferPoint.az(msg.msg):
            param = self.cmdTransferPoint.get_original_param()
            result = groupPlugin.transfer_point(member.qq, member.get_name(), param)

        elif self.cmdPointRank.az(msg.msg):
            result = groupPlugin.get_point_rank()

        elif self.cmdClearPoint.az(msg.msg):
            aim_qq = my_qq = member.qq
            aim_nick = my_nick = member.get_name()
            result = groupPlugin.clear_point(my_qq, my_nick, aim_qq, aim_nick)

        elif self.cmdClearOtherPoint.az(msg.msg):
            param = self.cmdClearOtherPoint.get_param_list()
            my_qq = member.qq
            my_nick = member.get_name()
            aim_qq = param[0]
            aim_nick = str(aim_qq)
            if aim_qq.isdigit():
                result = groupPlugin.clear_point(my_qq, my_nick, aim_qq, aim_nick)
            else:
                result = u"对方QQ号错误"
        elif self.cmdGetClearPointChance.az(msg.msg):
            result = groupPlugin.get_clear_chance(member.qq, member.get_name())

        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/已修改/group_point/__init__.py
