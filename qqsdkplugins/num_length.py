#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""

import plugin
import cmdaz
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD

#from webqqsdk import entity


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"位数计算"

    def __init__(self):

        super(Plugin, self).__init__()
        self.cmd = CMD(u"位数", param_len=1)

    def calc(self, msg):
        """
        msg 是接收到的消息实例
        """

        msgContent = msg.msg
        msgContent = msgContent.strip()
        result = ""
        if self.cmd.az(msgContent):
            
            param = self.cmd.get_original_param()
#            print param
            param = param.replace(" ", "")
            if not param.isdigit():
                result = u"只能输入数字！"
            else:
                result = u"您要计算的结果为：%d 位" % (len(param))

        if result:
            msg.reply(result)
            msg.destroy()

    def install(self):
        """
        插件安装时会调用此方法
        """

        # 直接实例化方式新建事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        
        event = MsgEvent(self.calc)
        self.qqClient.addFriendMsgEvent(event) # 添加处理好友消息的事件
        self.qqClient.addGroupMsgEvent(event) # 添加处理好友消息的事件

        # 添加其他事件请查看开发文档

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件【%s】被卸载了" % self.Name
