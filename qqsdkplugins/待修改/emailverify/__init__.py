<<<<<<< HEAD:qqsdkplugins/待修改/emailverify/__init__.py
#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import thread

import emailclient
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent

#from webqqsdk import entity

send_user = "@qq.com"
send_pwd = ""
smtp_server = "smtp.qq.com"
imap_server = "imap.qq.com"

recv_user = "neverlike@neverlike.net"

class MyEvent(MsgEvent):
    __doc__ = u"""这是类继承方式的event，墙裂推荐此方式，如果使用此方式，务必填写__doc__属性，好用于生成事件说明文档
    MsgEvent有个self.qqClient实例，此实例拥有大量的QQ API，详情查看开发文档
    """
    
    def event(self,msg):
        """
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        self.email = emailclient.Email(smtp_server, imap_server, send_user, send_pwd)
        self.email.sendMail(send_user,[recv_user],u"需要验证码",u"回复vc+空格+验证码",["verfiycode.jpg"])
        """
        while True:
            mailList = self.email.recvNewMail()
#            print mailList
            if mailList:
                mailId = mailList[-1]
                self.email.setMailSeen([mailId])
                content = self.email.readMail(mailId)[0].lower()
                vc = re.findall("vc (.+)",content)
#                print vc
                if vc:
                    vc = vc[0].strip()
#                    print vc
                    self.qqClient.inputVerifyCode(vc)
                    break
            time.sleep(5)
        """

    def main(self,msg):

        if self.qqClient.loginSucCount >= 1:
            thread.start_new_thread(self.event,(msg,))

        

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def loginSuccess(self,msg):
        if self.qqClient.loginSucCount >= 1:
            emailclient.Email(smtp_server, imap_server, send_user, send_pwd).sendMail(send_user, [recv_user], u"登录成功", "")

    def loginFailed(self,msg):
        emailclient.Email(smtp_server, imap_server, send_user, send_pwd).sendMail(send_user, [recv_user], u"登录失败", "")
        print u"登录失败",msg


    def install(self):


        # 类继承的方式添加事件
        event = MyEvent()
        self.qqClient.addNeedVerifyCodeEvent(event)

        # 登录相关事件

        self.qqClient.addLoginSuccessEvent(MsgEvent(self.loginSuccess))

        self.qqClient.addLoginFailedEvent(MsgEvent(self.loginFailed))

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



=======
#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import thread

import emailclient
import plugin

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent

#from webqqsdk import entity

send_user = "@qq.com"
send_pwd = ""
smtp_server = "smtp.qq.com"
imap_server = "imap.qq.com"

recv_user = "neverlike@neverlike.net"

class MyEvent(MsgEvent):
    __doc__ = u"""这是类继承方式的event，墙裂推荐此方式，如果使用此方式，务必填写__doc__属性，好用于生成事件说明文档
    MsgEvent有个self.qqClient实例，此实例拥有大量的QQ API，详情查看开发文档
    """
    
    def event(self,msg):
        """
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

        self.email = emailclient.Email(smtp_server, imap_server, send_user, send_pwd)
        self.email.sendMail(send_user,[recv_user],u"需要验证码",u"回复vc+空格+验证码",["verfiycode.jpg"])
        """
        while True:
            mailList = self.email.recvNewMail()
#            print mailList
            if mailList:
                mailId = mailList[-1]
                self.email.setMailSeen([mailId])
                content = self.email.readMail(mailId)[0].lower()
                vc = re.findall("vc (.+)",content)
#                print vc
                if vc:
                    vc = vc[0].strip()
#                    print vc
                    self.qqClient.inputVerifyCode(vc)
                    break
            time.sleep(5)
        """

    def main(self,msg):

        if self.qqClient.loginSucCount >= 1:
            thread.start_new_thread(self.event,(msg,))

        

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):

    def loginSuccess(self,msg):
        if self.qqClient.loginSucCount >= 1:
            emailclient.Email(smtp_server, imap_server, send_user, send_pwd).sendMail(send_user, [recv_user], u"登录成功", "")

    def loginFailed(self,msg):
        emailclient.Email(smtp_server, imap_server, send_user, send_pwd).sendMail(send_user, [recv_user], u"登录失败", "")
        print u"登录失败",msg


    def install(self):


        # 类继承的方式添加事件
        event = MyEvent()
        self.qqClient.addNeedVerifyCodeEvent(event)

        # 登录相关事件

        self.qqClient.addLoginSuccessEvent(MsgEvent(self.loginSuccess))

        self.qqClient.addLoginFailedEvent(MsgEvent(self.loginFailed))

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/emailverify/__init__.py
