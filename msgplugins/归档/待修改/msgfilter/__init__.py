<<<<<<< HEAD:qqsdkplugins/待修改/msgfilter/__init__.py
# coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import os

import plugin
import cmdaz

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
SendMsgFilter = webqqsdk.SendMsgFilter
curPath = os.path.dirname(__file__)

CMD = cmdaz.CMD


class MyMsgFilter(SendMsgFilter):

    def __init__(self):
        super(MyMsgFilter, self).__init__()
        self.filterWordList = []
        self.wordPath = curPath + "/word_list.txt"
        self.read_word_list()
        
    def read_word_list(self):
        with open(self.wordPath) as f:
            data = f.read().decode("u8")
            self.filterWordList = [i.strip() for i in data.splitlines()]

            f.close()

    def write_word_list(self):

        data = "\n".join(self.filterWordList)
        with open(self.wordPath, "w") as f:
            f.write(data.encode("u8"))
            f.close()

    def add_word(self, word):

        word = word.strip()
        if word not in self.filterWordList:
            self.filterWordList.append(word)
        self.write_word_list()

    def delWord(self, word):

        word = word.strip()
        self.filterWordList.remove(word)
        self.write_word_list()

    def main(self, msgContent):

        msgContent = msgContent.strip()
        #print msgContent
        #print "\n".join(self.filterWordList)
        for i in self.filterWordList:
            if i in msgContent:
                return False

        return True


class FilterControl(MsgEvent):

    def __init__(self, msgFilter):

        self.msgFilter = msgFilter

    def main(self, msg):

#        print msg.friend.qq
        if msg.friend.qq not in robot_config.admins:
            return


        msgContent = msg.msg

        addFilterWordCmd = CMD(u"加过滤词", hasParam=True)
        delFilterWordCmd = CMD(u"删过滤词", hasParam=True)

        if addFilterWordCmd.az(msgContent):
            param = addFilterWordCmd.get_original_param()
            self.msgFilter.add_word(param)
            msg.reply(u"添加成功")
            msg.destroy()

        elif delFilterWordCmd.az(msgContent):
            param = delFilterWordCmd.get_original_param()
            self.msgFilter.delWord(param)
            msg.reply(u"删除成功")
            msg.destroy()


            



# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):


    def install(self):
        """
        插件安装时会调用此方法
        """

        msgFilter = MyMsgFilter()
        filterControl = FilterControl(msgFilter)
        self.qqClient.addSendMsgFilter(msgFilter) # 添加处理好友消息的事件
        self.qqClient.addFriendMsgEvent(filterControl) 

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件%s被卸载了"%(__file__)



=======
# coding=UTF8

"""
插件开发示例，编写完插件后，需要在PluginList.txt添加插件文件名
"""
import os

import plugin
import cmdaz

QQPlugin = plugin.QQPlugin
webqqsdk = plugin.webqqsdk
MsgEvent = webqqsdk.msgevent.MsgEvent
SendMsgFilter = webqqsdk.SendMsgFilter
curPath = os.path.dirname(__file__)

CMD = cmdaz.CMD


class MyMsgFilter(SendMsgFilter):

    def __init__(self):
        super(MyMsgFilter, self).__init__()
        self.filterWordList = []
        self.wordPath = curPath + "/word_list.txt"
        self.read_word_list()
        
    def read_word_list(self):
        with open(self.wordPath) as f:
            data = f.read().decode("u8")
            self.filterWordList = [i.strip() for i in data.splitlines()]

            f.close()

    def write_word_list(self):

        data = "\n".join(self.filterWordList)
        with open(self.wordPath, "w") as f:
            f.write(data.encode("u8"))
            f.close()

    def add_word(self, word):

        word = word.strip()
        if word not in self.filterWordList:
            self.filterWordList.append(word)
        self.write_word_list()

    def delWord(self, word):

        word = word.strip()
        self.filterWordList.remove(word)
        self.write_word_list()

    def main(self, msgContent):

        msgContent = msgContent.strip()
        #print msgContent
        #print "\n".join(self.filterWordList)
        for i in self.filterWordList:
            if i in msgContent:
                return False

        return True


class FilterControl(MsgEvent):

    def __init__(self, msgFilter):

        self.msgFilter = msgFilter

    def main(self, msg):

#        print msg.friend.qq
        if msg.friend.qq not in robot_config.admins:
            return


        msgContent = msg.msg

        addFilterWordCmd = CMD(u"加过滤词", hasParam=True)
        delFilterWordCmd = CMD(u"删过滤词", hasParam=True)

        if addFilterWordCmd.az(msgContent):
            param = addFilterWordCmd.get_original_param()
            self.msgFilter.add_word(param)
            msg.reply(u"添加成功")
            msg.destroy()

        elif delFilterWordCmd.az(msgContent):
            param = delFilterWordCmd.get_original_param()
            self.msgFilter.delWord(param)
            msg.reply(u"删除成功")
            msg.destroy()


            



# 必须：
#    要有个类，类名是Plugin，且继承于QQPlugin
class Plugin(QQPlugin):


    def install(self):
        """
        插件安装时会调用此方法
        """

        msgFilter = MyMsgFilter()
        filterControl = FilterControl(msgFilter)
        self.qqClient.addSendMsgFilter(msgFilter) # 添加处理好友消息的事件
        self.qqClient.addFriendMsgEvent(filterControl) 

        # 添加其他事件请查看开发文档

        print u"插件%s被安装了"%(__file__)

    def uninstall(self):
        """
        插件被卸载时调用
        """

        print u"插件%s被卸载了"%(__file__)



>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90:qqsdkplugins/待修改/msgfilter/__init__.py
