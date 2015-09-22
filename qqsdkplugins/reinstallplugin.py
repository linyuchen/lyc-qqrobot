#coding=UTF8

"""
此插件功能：修改插件代码后，可以利用此插件在不需要重启主程序的情况下重新安装所有插件
"""
import time
import thread

import plugin

class Plugin(plugin.QQPlugin):

    def __init__(self):

        self.running = True
        thread.start_new_thread(self.threadFunc,(None,))

    def threadFunc(self,arg):

        while self.running:
            time.sleep(1)
            if self.qqClient.online:
                raw_input("press Enter to reinstall all plugins\n")
                self.qqClient.reInstallPlugins()

    def install(self):

        self.running = True

    def uninstall(self):

        self.running = False


