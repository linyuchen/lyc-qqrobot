#coding=UTF8

"""
插件开发示例2，编写完插件后，需要在PluginList.txt添加插件文件名
"""

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
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        print msg
        print dir(msg)
        self.qqClient.sendMsg2Buddy(msg.friend.uin, msg.msg)

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def showMsg(self,msg):

        print u"实例化方式的event"
        print msg
        print dir(msg)

    def inputVerifyCode(self,msg):
        # 输入验证码
        code = raw_input("input verify code:")
        self.qqClient.inputVerifyCode(code)

    def loginSuccess(self,msg):
        print u"登录成功"

    def loginFailed(self,msg):
        print u"登录失败",msg


    def install(self):

        # 方法二：
        # 直接实例化方式添加事件
        # 注意传入的函数必须仅有一个参数,用于传入消息实例
        event = MsgEvent(self.inputVerifyCode)
        self.qqClient.addNeedVerifyCodeEvent(event)

        # 类继承的方式添加事件
        event = MyEvent()
        self.qqClient.addFriendMsgEvent(event)

        # 登录相关事件

        self.qqClient.addLoginSuccessEvent(MsgEvent(self.loginSuccess))

        self.qqClient.addLoginFailedEvent(MsgEvent(self.loginFailed))

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



