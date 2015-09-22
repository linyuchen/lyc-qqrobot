#coding=UTF8

import baiduzhidao
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    百度知道查询
    命令：
        搜索问题: 知道 + 空格 + 关键字
        翻下一页问题： 知道下一页
        查询答案： 问题 + 空格 + 序号
    """
    def __init__(self):

        self.name = u"百度知道"
        self.zdCmd = CMD(u"知道", hasParam=True)
        self.nextCmd= CMD(u"知道下一页")
        self.answerCmd = CMD(u"问题", hasParam=True)
        self.note = u"""

发送“知道下一页”查看下一页问题列表
发送“问题+空格+序号”查看答案：如“问题 1”
            """

        # 不同的QQ和群用不同的实例， 因为每个人想要的数据都不一样
        self.zhidaoFriendInstances = {} # key qq, value instance
        self.zhidaoGroupInstances = {} # key qq, value instance

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        if isinstance(msg, webqqsdk.message.GroupMsg):
            instances = self.zhidaoGroupInstances
            qq = msg.group.qq
        elif isinstance(msg, webqqsdk.message.FriendMsg):
            instances = self.zhidaoFriendInstances
            qq = msg.friend.qq

        if instances.has_key(qq):
            zhidao = instances[qq]
        else:
            zhidao = baiduzhidao.ZhiDao()
            instances[qq] = zhidao

        if self.zdCmd.az(msg.msg):
            result = zhidao.getQuestions(self.zdCmd.getOriginalParam())
            msg.reply(result + self.note)
            msg.destroy()
        elif self.nextCmd.az(msg.msg):
            result = zhidao.getNextQuestions()
            
            msg.reply(result + self.note)
            msg.destroy()
        elif self.answerCmd.az(msg.msg):
            result = zhidao.getAnswer(self.answerCmd.getParamList()[0])
            msg.reply(result)
            msg.destroy()

# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):

        event = MyEvent()

        self.qqClient.addGroupMsgEvent(event)
        self.qqClient.addFriendMsgEvent(event)

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



