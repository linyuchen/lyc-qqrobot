# -*- encoding:UTF8 -*-
import threading
import plugin
MsgEvent = plugin.webqqsdk.MsgEvent


class Plugin(plugin.QQPlugin):

    def install(self):

        event = MsgEvent(lambda msg:threading.Thread(target=self.inputVerifyCode).start())
        self.qqClient.addNeedVerifyCodeEvent(event)
        self.qqClient.addLoginSuccessEvent(MsgEvent(self.loginSuccess))
        self.qqClient.addLoginFailedEvent(MsgEvent(self.loginFailed))
        self.qqClient.addLogoutEvent(MsgEvent(self.logout))
        self.qqClient.addFriendMsgEvent(MsgEvent(self.msgFilter))
        self.qqClient.addGroupMsgEvent(MsgEvent(self.msgFilter))
#        self.qqClient.getGroups()
#        print self.qqClient.qqUser.groups
#        print self.qqClient.qqUser.groups[977514971].qq
    
    def msgFilter(self, msg):
        if msg.time < self.qqClient.startTime:
            msg.destroy()

    def inputVerifyCode(self):
        # 输入验证码
        code = raw_input(u"输入验证码:".encode("gbk"))
        self.qqClient.input_verify_code(code)

    def loginSuccess(self, msg):
        print u"登录成功"

    def loginFailed(self, msg):
        print u"登录失败",msg.msg

    def logout(self, msg):
        print u"掉线了"
        print u"进行重新登录"
        self.qqClient.login()
