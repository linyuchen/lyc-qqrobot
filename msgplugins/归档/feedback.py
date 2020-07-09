# coding=UTF8

"""

"""

import plugin
import cmdaz
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"反馈"

    def __init__(self):

        self.cmd = CMD(u"反馈", param_len=1)
        self.adminQQ = 1412971608
        self.feedbackNote = u"反馈成功!"

    def friendFeedback(self, msg):
        """
        msg 是接收到的消息实例
        """
        if self.cmd.az(msg.msg):
            friend = msg.friend
            result = u"%s(%d): %s" % (friend.get_name(), friend.qq, self.cmd.get_original_param())
            self.qqClient.send_buddy_msg(self.adminQQ, result)
            msg.reply(self.feedbackNote)
            msg.destroy()

    def groupFeedback(self, msg):

        if self.cmd.az(msg.msg):
            group = msg.group
            groupMember = msg.groupMember

            result = u"群 %s(%d)：%s(%d): %s" % (group.name, group.qq,
                                               groupMember.get_name(), groupMember.qq, self.cmd.get_original_param())
            
            self.qqClient.send_buddy_msg(self.adminQQ, result)
            msg.reply(self.feedbackNote)
            msg.destroy()


    def install(self):
        """
        插件安装时会调用此方法
        """

        # 直接实例化方式新建事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        
        event = MsgEvent(self.friendFeedback)
        self.qqClient.addFriendMsgEvent(event)  # 添加处理好友消息的事件
        self.qqClient.addGroupMsgEvent(MsgEvent(self.groupFeedback))

        # 添加其他事件请查看开发文档

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件【%s】被卸载了" % self.Name



