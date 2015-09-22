# coding=UTF8

import sys
import traceback
import time
import os

from qqclient import QQClient

cur_path = os.path.dirname(__file__) or "."


class Main(QQClient):  #  得继承QQClient
    """
    self.startTime: int, 程序启动的时间戳
    """

    def __init__(self, port):
        super(Main, self).__init__(port)
        self.startTime = time.time()

        self.pluginsPath = cur_path + "/../qqsdkplugins"
        self.pluginListPath = self.pluginsPath + "/PluginList.txt"
        sys.path.append(self.pluginsPath)

        self.pluginNames = []  # 每项元素是插件所在的文件的文件名
        self.pluginModules = []  # 每项元素是插件模块
        self.plugins = []  # 每项元素是Plugin实例


    def main(self):

        self.readPlugins()
        self.installPlugins()
        self.start()
        # self.login()
#        self.debug()

    def reInstallPlugins(self):

        self.uninstallPlugins()
        self.readPlugins()

        for module in self.pluginModules:
            reload(module)

        self.installPlugins()
        for plugin in self.plugins:
            plugin.reinstall()

    def readPlugins(self):

        self.pluginModules = []
        self.pluginNames = []
        with open(self.pluginListPath) as f:
            data = f.readlines()

        pluginNames = [i.strip() for i in data if (not (i.strip().startswith("#")) and i.strip())]
        for i in pluginNames:
            self.pluginNames.append(i)
            try:
                self.pluginModules.append(__import__(i))
            except:
                traceback.print_exc()

        
#        print self.pluginNames

    def installPlugins(self):

#        print self.pluginModules
        for plugin in self.pluginModules:
            try:
                p = plugin.Plugin()
                p.setupQQInstance(self)
                p.install()
                self.plugins.append(p)
            except:
                traceback.print_exc()
#        print u"main",self.friendMsgEvents

    def uninstallPlugins(self):
        """
        卸载所有插件，实际上调用的是插件的uninstall方法
        """
        for plugin in self.plugins:
            try:
                plugin.uninstall()
            except:
                traceback.print_exc()

        self.clearEvents()
        self.clearSendMsgFilter()
        self.plugins = []


