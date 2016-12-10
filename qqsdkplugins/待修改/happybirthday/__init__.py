#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import os
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent

import sys
cur_path = os.path.dirname(__file__)
module_path = cur_path + ".." + r"\menucmd\commands\group\groupplugins"
sys.path.append(module_path)
import grouppluginbase

#from webqqsdk import entity


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def __init__(self):

        self.cmd = u"生日快乐"
        self.path = cur_path + "/qqlist.txt"
        self.qqlist = []
        self.readQQList()
        self.groupPlugin = grouppluginbase.GroupPluginBase()

    def readQQList(self):
        with open(self.path) as f:
            self.qqlist = f.readlines()
            f.close()
        self.qqlist = map(int, self.qqlist)

    def writeQQList(self):
        qqList = map(str, self.qqlist)
        data = "\n".join(qqList)
        with open(self.path, "w") as f:
            f.write(data)
            f.close()

    def happybirthday(self,msg):
        """
        msg 是接收到的消息实例
        """
        if self.cmd in msg.msg:
            group = msg.group
            groupMember = msg.groupMember
            memberQQ = groupMember.qq
            msg.reply(u"O(∩_∩)O谢谢 %s 的祝福~， 很开心， 虽然今天没有蛋糕， 但是已经习惯了" % groupMember.getName())
            if memberQQ not in self.qqlist:
                self.qqlist.append(memberQQ)
                self.writeQQList()
                point = 888000000000000000000000000000000000000000000000000000000000000
                self.groupPlugin._add_point(group.qq, memberQQ, "", point)

            msg.destroy()
                

        


    def install(self):
        """
        插件安装时会调用此方法
        """

        # 直接实例化方式新建事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        
        event = MsgEvent(self.happybirthday)
        self.qqClient.addGroupMsgEvent(event) # 添加处理好友消息的事件

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件%s被卸载了"%(__file__)



