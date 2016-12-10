#coding=UTF8

import admin_plugin
import cmdaz
import plugin
import robot_config

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
adminPlugin = admin_plugin.AdminPlugin
admins = robot_config.admins
#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    机器人管理员工具
    """
    def __init__(self):

        self.name = u"admin_plugin"
        self.cmdSendMsg = CMD(u"发消息", hasParam=True)
        self.cmdSendGroupMsg = CMD(u"发群消息", hasParam=True)
        self.cmdGetPoint = CMD(u"查活跃度", hasParam=True)
        self.cmdAddPoint = CMD(u"加活跃度", hasParam=True)
        self.cmdSetPoint = CMD(u"设活跃度", hasParam=True)
        self.cmdGetRpgData = CMD(u"查争霸数据", hasParam=True)
        self.cmdClearRpgData = CMD(u"清争霸数据", hasParam=True)
        self.cmdJoinGroup = CMD(u"加群", hasParam=True)
        self.cmdQuitGroup = CMD(u"退群", hasParam=True)
        
        self.cmdGetGroups = CMD(u"查群")
        self.cmdSetInviteMe = CMD(u"邀我进群", hasParam=True)

        self.cmdGetClearChance = CMD(u"查清负次数", hasParam=True)
        self.cmdAddClearChance = CMD(u"加清负次数", hasParam=True)
        self.groupInstances = {} # key groupQQ, value instanvc

        # 不同的QQ群用不同的实例， 因为每个人想要的数据都不一样



    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        friendQQ = msg.friend.qq
        

        admin = adminPlugin(self.qqClient)

        result = ""
        #print friendQQ
        if self.cmdSendMsg.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdSendMsg.get_original_param()
            result += admin.sendMsg2Buddy(param)

        elif self.cmdSendGroupMsg.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdSendGroupMsg.get_original_param()
            result += admin.sendMsg2Group(param)

        elif self.cmdGetPoint.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdGetPoint.get_param_list()[0]
            result += admin.get_point(param)

        elif self.cmdAddPoint.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdAddPoint.get_original_param()
            result += admin.add_point(param)

        elif self.cmdSetPoint.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdSetPoint.get_original_param()
            result += admin.set_point(param)

        elif self.cmdGetRpgData.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdGetRpgData.get_param_list()[0]
            result += admin.get_rpg_data(param)

        elif self.cmdClearRpgData.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdClearRpgData.get_param_list()[0]
            result += admin.clear_rpg_data(param)

        elif self.cmdJoinGroup.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdJoinGroup.get_original_param()
            result += admin.joinGroup(param)

        elif self.cmdQuitGroup.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdQuitGroup.get_param_list()[0]
            result += admin.quitGroup(param)

        elif self.cmdGetGroups.az(msg.msg):
            if friendQQ not in admins:
                return
            result += admin.getGroups()

        elif self.cmdSetInviteMe.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdSetInviteMe.get_original_param()
            result += admin.setInviteMeToGroup(param)

        elif self.cmdGetClearChance.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdGetClearChance.get_original_param()
            result += admin.get_clear_point_chance(param)

        elif self.cmdAddClearChance.az(msg.msg):
            if friendQQ not in admins:
                return
            param = self.cmdAddClearChance.get_original_param()
            result += admin.add_clear_point_chance(param)
  
        if result:
            msg.reply(result)
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addFriendMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



