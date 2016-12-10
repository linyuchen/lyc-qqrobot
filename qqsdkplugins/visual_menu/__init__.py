# coding=UTF8

"""
可视化菜单
当前目录下的所有txt(utf8编码)都是菜单
txt文件名即菜单绑定的命令
"""
import os
import plugin
import cmdaz
import visualmenu
import robot_config
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
curPath = os.path.dirname(__file__)


class MenuEvent(MsgEvent, visualmenu.VisualMenu):

    def __init__(self):

        super(MenuEvent, self).__init__()
        visualmenu.VisualMenu.__init__(self)

    def main(self, msg):

        msg_content = msg.msg.strip()
        menu = self.allMenu.copy()
        if isinstance(msg, webqqsdk.message.GroupMsg):
            menu.update(self.groupMenu.items())
        elif isinstance(msg, webqqsdk.message.FriendMsg):
            if msg.friend.qq in robot_config.admins:
                menu.update(self.adminMenu.items())

        for i in self.cmdNameList:

            if msg_content == i:
                result = menu.get(i, None)
                if result:
                    msg.reply(result)
                    msg.destroy()
                break


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"可视化菜单"

    def __init__(self):

        super(Plugin, self).__init__()

    def install(self):
        """
        插件安装时会调用此方法
        """

        # 直接实例化方式新建事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        
        event = MenuEvent()
        self.qqClient.addFriendMsgEvent(event)  # 添加处理好友消息的事件
        self.qqClient.addGroupMsgEvent(event) 

        # 添加其他事件请查看开发文档

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件【%s】被卸载了" % self.Name
