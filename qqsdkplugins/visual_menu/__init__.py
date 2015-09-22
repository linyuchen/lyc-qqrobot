#coding=UTF8

"""
可视化菜单
当前目录下的所有txt(utf8编码)都是菜单
txt文件名即菜单绑定的命令
"""
import os
import time
import plugin
import cmdaz
import visualmenu
import robot_config
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
curPath = os.path.dirname(__file__)
#from webqqsdk import entity


class MenuEvent(MsgEvent, visualmenu.VisualMenu):

    def __init__(self):

        super(MenuEvent, self).__init__()
        visualmenu.VisualMenu.__init__(self)

    def main(self, msg):

        msgContent = msg.msg.strip()
        menu = self.allMenu.copy()
        if isinstance(msg, webqqsdk.message.GroupMsg):
            menu.update(self.groupMenu.items())
        elif isinstance(msg, webqqsdk.message.FriendMsg):
            if msg.friend.qq in robot_config.admins:
                #print "admin"
                menu.update( self.adminMenu.items())

#        print ",".join(menu.keys())
        
        for i in self.cmdNameList:

            if msgContent == i:
                result = menu.get(i, None)
                if result:
#                    print result
                    msg.reply(result)
                    msg.destroy()
                break

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def __init__(self):

        super(Plugin)

    def install(self):
        """
        插件安装时会调用此方法
        """

        # 直接实例化方式新建事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        
        event = MenuEvent()
        self.qqClient.addFriendMsgEvent(event) # 添加处理好友消息的事件
        self.qqClient.addGroupMsgEvent(event) 

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件%s被卸载了"%(__file__)



