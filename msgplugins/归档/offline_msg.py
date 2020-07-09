#coding=UTF8

"""
离线消息过滤

"""

import time

import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""这是类继承方式的event，墙裂推荐此方式，如果使用此方式，务必填写__doc__属性，好用于生成事件说明文档
    MsgEvent有个self.qqClient实例，此实例拥有大量的QQ API，详情查看开发文档
    """

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在, 注意此方法需存在一个参数用于传入消息实例
        """

        if (time.time() - msg.time) > 10:
            msg.destroy()


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    Name = u"离线消息过滤"

    def install(self):
        # 类继承的方式添加事件
        event = MyEvent()
        self.qqClient.addFriendMsgEvent(event)
        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addRequestJoinGroupEvent(event)
        self.qqClient.addFriendStatusChangeEvent(event)

        print u"插件【%s】被安装了" % self.Name

    def uninstall(self):

        print u"插件【%s】被卸载了" % self.Name



