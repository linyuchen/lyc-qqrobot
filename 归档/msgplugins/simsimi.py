#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import json
import os
import plugin
import httpclient
webqqsdk = plugin.webqqsdk # webqqsdk模块

QQPlugin = plugin.QQPlugin
MsgEvent = webqqsdk.msgevent.MsgEvent

import sys
cur_path = os.path.dirname(__file__)
module_path = cur_path + "/../group_manager"
sys.path.append(module_path)
from groupplugin import GroupPlugin

#from webqqsdk import entity


class TalkEvent(MsgEvent):
    __doc__ = u"小黄鸡聊天接口，请把此插件放到插件列表最后"

    def main(self,msg):
        """
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """

#        print "simsimi"
        talkResult = self.talk(msg.msg)
        if talkResult:
            msg.reply(talkResult)
            msg.destroy()


    def talk(self,content):
        
        content = content.encode("u8")
        __http = httpclient.Http(False)
        content = __http.quote(content)
        __http.add_header("X-Requested-With", "XMLHttpRequest")
        __http.add_header("Accept-Encoding", "gzip, deflate")
        __http.add_header("Cookie", "Filtering=0.0; isFirst=1; simsimi_uid=50604967; teach_btn_url=talk; selected_nc=zh; menuType=web; __utma=119922954.1340887141.1394896689.1396276647.1396451589.3; __utmb=119922954.4.8.1396451689947; __utmc=119922954; __utmz=119922954.1394896690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)")
        __http.add_header("Referer", "http://www.simsimi.com/talk.htm?lc=zh")
        url = "http://www.simsimi.com/func/reqN?lc=zh&ft=0.0&fl=http%3A%2F%2Fwww.simsimi.com%2Ftalk.htm&req="

        url += content
        data = __http.connect(url, timeout=45)
        error = u"机器人的官方网站：http://www.neverlike.net\n回复“菜单”获取机器人命令列表"
        if not data:
            return error
        data = json.loads(data)
#        print data
        """
        {"result":200,"sentence_link_id":25729085,"slang":false,"sentence_teach_uid":0," msg":"OK","sentence_resp":"大家"}
        
        
        """
        


        if data["result"] != 200:
            return error
        data = data["sentence_resp"]
        return data

class GroupTalkEvent(TalkEvent):

    def __init__(self):
        TalkEvent.__init__(self)

    def main(self,msg):


        talkResult = ""
        msgContent = msg.msg
        myGroupCard = msg.group.getMemberByUin(self.qqClient.qqUser.qq).get_name()
        myGroupCard = u"@" + myGroupCard
#        print myGroupCard
        chating = False
        if msgContent.startswith("#"):
            msgContent = msgContent[1:]
            chating = True
        elif myGroupCard in msgContent:
            msgContent = msgContent.replace(myGroupCard, "")
            chating = True
        if chating:
            chat_open = GroupPlugin(msg.group.qq).getChatSwitch()
            if chat_open  == 1:
                talkResult = self.talk(msgContent)
                msg.reply(talkResult)
            else:
                """
                msg.reply(u"我已经被管理员关闭了聊天功能，不能聊天了诶~")
                msg.destroy()
                """


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):


    def install(self):


        # 类继承的方式添加事件
        event = TalkEvent()
        groupEvent = GroupTalkEvent()
        self.qqClient.addFriendMsgEvent(event)
        self.qqClient.addGroupMsgEvent(groupEvent)


        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



