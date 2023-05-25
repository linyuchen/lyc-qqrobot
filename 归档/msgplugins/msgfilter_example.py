#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""

import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
SendMsgFilter = webqqsdk.SendMsgFilter

#from webqqsdk import entity



# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def testFilter(self,msgContent):
        """
        """
        print msgContent
        if "1" in msgContent:
            return True
        else:
            return False


    def install(self):
        """
        插件安装时会调用此方法
        """

        
        self.qqClient.addSendMsgFilter(SendMsgFilter(self.testFilter)) # 添加处理好友消息的事件

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件%s被卸载了"%(__file__)



