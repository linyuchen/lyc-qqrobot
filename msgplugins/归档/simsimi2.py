#coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import json
import re
import plugin
webqqsdk = plugin.webqqsdk # webqqsdk模块

from webqqsdk import utils

QQPlugin = plugin.QQPlugin
MsgEvent = webqqsdk.msgevent.MsgEvent

from webqqsdk import entity
FontStyle = entity.FontStyle


class TalkEvent(MsgEvent):
    __doc__ = u"小黄鸡聊天接口，请把此插件放到插件列表最后"

    def __init__(self):
        self.words = [u"加微信",u"新微信",u"微信号",u"Wei信",u"wei信",u"做爱",u"吃逼",u"咪咪",u"草你",u"操你",u"帮你舔",u"好大",u"小穴",u"操烂",u"啊!",u"啊~",u"鸡巴",u"脑残",u"傻逼",u"嫖妓",u"嫖娼"]
        self.m_words = ["webqqsdk","entity","plugin","message","utils","webqqclient","msgevent"]

    def main(self,msg):
        """
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        if msg.msg.startswith(u"@小D机器人") or msg.msg.startswith(u"#"):
            gmsg = msg.msg.replace(u"@小D机器人","").replace(u"#","").strip()
            if gmsg.startswith(u"dir("):
                dirm_result = self.dirm(gmsg)
#                print dirm_result
                msg.reply(dirm_result ,FontStyle(fontName=u"黑体",fontSize=10,color=0x800080))
#                msg.reply(dirm_result)
                msg.destroy()
                return
            if gmsg == "":
                msg.reply(u"对我没话说么？",FontStyle(fontName=u"黑体",fontSize=12,color=0x800080))
                msg.destroy()
                return
            talkResult = self.talk(gmsg)
            if talkResult:
                talkword = talkResult.replace(" ","").replace(">","").replace("<","").replace("^","")
                for i in self.words:
                    if i in talkword:
                        msg.reply(u"哎呀，不行的啦",FontStyle(fontName=u"黑体",fontSize=12,color=0x800080))
                        msg.destroy()
                        return
                msg.reply(talkResult,FontStyle(fontName=u"黑体",fontSize=12,color=0x800080))
                msg.destroy()

    def talk(self,content):

        content = content.encode("u8")
        __http = utils.httpserver.Http(False)
        content = __http.quote(content)
        __http.add_header("X-Requested-With", "XMLHttpRequest")
        __http.add_header("Accept-Encoding", "gzip, deflate")
        __http.add_header("Cookie", "Filtering=0.0; isFirst=1; simsimi_uid=50604967; teach_btn_url=talk; selected_nc=ch; menuType=web; __utma=119922954.1340887141.1394896689.1396276647.1396451589.3; __utmb=119922954.4.8.1396451689947; __utmc=119922954; __utmz=119922954.1394896690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)")
        __http.add_header("Referer", "http://www.simsimi.com/talk.htm?lc=zh")
        url = "http://www.simsimi.com/func/reqN?lc=ch&ft=0.0&fl=http%3A%2F%2Fwww.simsimi.com%2Ftalk.htm&req="

        url += content
        data = __http.connect(url, timeout=45)
        error = u"哎呀呀~  听不懂你在说什么"
        if not data:
            #return ""
            return error
        data = json.loads(data)
#        print data
        """
        {"result":200,"sentence_link_id":25729085,"slang":false,"sentence_teach_uid":0," msg":"OK","sentence_resp":"大家"}
        """
        if data["result"] != 200:
            #return ""
            return error
        data = data["sentence_resp"]
        return data

    def dirm(self,content):
        m_m = re.search(r"dir\(([\.\w\s]+)\)", content)
        if m_m:
            if m_m.group(1).count("__") > 1:
                return u"不能查询私有属性"
            m_list = m_m.group(1).encode("utf-8").split(".")
            if m_list[0] in self.m_words:
                return u"没有找到%s模块" % m_list[0]
            try:
                temp = __import__(m_list[0])
            except Exception, e:
                if e.message.find("No module named") >= 0:
                    return self.exec_dir(m_list)
                else:
                    return u"加载%s模块时出错" % m_list[0]
            return self.exec_dir(m_list, temp)
        else:
            if self.get_text(content,"dir(", ")").strip() == u"小D机器人":
                return u"['一个有爱的智能机器人']"
            return u"没有可用的dir参数"

    def exec_dir(self, m_list, mod=None):
        if m_list[0] == "self" or m_list[0] == "main":
            return u"你想干什么？"
        result = ""
        try:
            if mod:
                if len(m_list) > 1:
                    exec "result = dir(mod.%s)" % (".".join(m_list[1:]))
                else:
                    result = dir(mod)
            else:
                exec "result = dir(%s)" % (".".join(m_list))
            return unicode(result)
        except Exception, e:
            if e.message.find("object has no attribute") >= 0:
                return u"此对象没有%s属性" % self.get_text(e.message, "object has no attribute '", "'")
            elif e.message.find("is not defined") >= 0:
                return u"没有%s模块或属性" % m_list[0]
            elif e.message.find("type object '%s' has no attribute"%m_list[0]) >= 0:
                return u"%s类型没有%s属性" % (m_list[0],self.get_text(e.message, "has no attribute '", "'"))
            else:
                return u"加载%s模块时出错" % m_list[0]

    def get_text(self, data, left = "", right = "", startpos = 0):
        """取中间字符"""
        if startpos > 0:
            data = data[startpos:]
        leftpos = (data.find(left) if left != "" else -1)
        leftpos = (leftpos  + len(left) if leftpos != -1 else -1)
        if right != "":
            if leftpos != -1:
                rightpos = data[leftpos:].find(right)
            else:
                rightpos = data.find(right)
        else:
            rightpos = -1
        if leftpos == -1 and rightpos == -1:
            return data
        elif leftpos == -1:
            return data[:rightpos]
        elif rightpos == -1:
            return data[leftpos:]
        else:
            return data[leftpos:rightpos + leftpos]

class friendTalkEvent(MsgEvent):
    __doc__ = u"小黄鸡聊天接口，请把此插件放到插件列表最后"

    def main(self,msg):
        """
        main方法必须存在,注意此方法需存在一个参数用于传入消息实例
        """
        gmsg = msg.msg.strip()
        talkResult = self.talk(gmsg)
        if talkResult:
            msg.reply(talkResult)
            msg.destroy()


    def talk(self,content):
        
        content = content.encode("u8")
        __http = utils.httpserver.Http(False)
        content = __http.quote(content)
        __http.add_header("X-Requested-With", "XMLHttpRequest")
        __http.add_header("Accept-Encoding", "gzip, deflate")
        __http.add_header("Cookie", "Filtering=0.0; isFirst=1; simsimi_uid=50604967; teach_btn_url=talk; selected_nc=ch; menuType=web; __utma=119922954.1340887141.1394896689.1396276647.1396451589.3; __utmb=119922954.4.8.1396451689947; __utmc=119922954; __utmz=119922954.1394896690.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)")
        __http.add_header("Referer", "http://www.simsimi.com/talk.htm?lc=zh")
        url = "http://www.simsimi.com/func/reqN?lc=ch&ft=0.0&fl=http%3A%2F%2Fwww.simsimi.com%2Ftalk.htm&req="

        url += content
        data = __http.connect(url, timeout=45)
        error = u"机器人的官方网站：http://www.neverlike.net\n回复“菜单”获取机器人命令列表"
        if not data:
            return ""
            return error
        data = json.loads(data)
#        print data
        """
        {"result":200,"sentence_link_id":25729085,"slang":false,"sentence_teach_uid":0," msg":"OK","sentence_resp":"大家"}
        """
        if data["result"] != 200:
            return ""
            return error
        data = data["sentence_resp"]
        return data


# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):



    def install(self):


        # 类继承的方式添加事件
        fevent = friendTalkEvent()
        gevent = TalkEvent()
        self.qqClient.addFriendMsgEvent(fevent)
        self.qqClient.addGroupMsgEvent(gevent)


        print u"插件%s被安装了"%(__file__)

    def uninstall(self):

        print u"插件%s被卸载了"%(__file__)



