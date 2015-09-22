#coding=UTF8

import lyrics
import cmdaz
import plugin
QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk # webqqsdk模块
MsgEvent = webqqsdk.msgevent.MsgEvent
CMD = cmdaz.CMD
mod = lyrics.Lyrics

#from webqqsdk import entity

#新建个事件类，继承于MsgEvent
class MyEvent(MsgEvent):
    __doc__ = u"""
    歌词查询
    命令：
        搜索歌词: 歌词 + 空格 + 关键字
        查看歌词： 看歌词 + 空格 + 序号
        查看lrc歌词： 看lrc歌词 + 空格 + 序号
    """
    def __init__(self):

        self.name = u"歌词查询"
        self.inquireCmd = CMD(u"歌词", hasParam=True)
        self.readCmd= CMD(u"看歌词", hasParam=True)
        self.readLrcCmd = CMD(u"看lrc歌词", hasParam=True)
        self.note = u"""

发送“看歌词+空格+序号”看歌词，如：看歌词 1
发送“看lrc歌词+空格+序号”看lrc格式的歌词，如：看lrc歌词 1
            """

        # 不同的QQ和群用不同的实例， 因为每个人想要的数据都不一样
        self.friendInstances = {} # key qq, value instance
        self.groupInstances = {} # key qq, value instance

    def main(self,msg):
        """
        此方法是用于处理事件接收到的消息
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        
        if isinstance(msg, webqqsdk.message.GroupMsg):
            modInstances = self.groupInstances
            qq = msg.group.qq
        elif isinstance(msg, webqqsdk.message.FriendMsg):
            modInstances = self.friendInstances
            qq = msg.friend.qq

        if modInstances.has_key(qq):
            modInstance = modInstances[qq]
        else:
            modInstance = mod()
            modInstances[qq] = modInstance

        if self.inquireCmd.az(msg.msg):
            result = modInstance.get_lyrics(self.inquireCmd.getOriginalParam())
            msg.reply(result + self.note)
            msg.destroy()
        elif self.readCmd.az(msg.msg):
            result = modInstance.get_lyric(self.readCmd.getParamList()[0])
            msg.reply(result)
            msg.destroy()
        elif self.readLrcCmd.az(msg.msg):
            result = modInstance.get_lyric(self.readLrcCmd.getParamList()[0], 4)
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



