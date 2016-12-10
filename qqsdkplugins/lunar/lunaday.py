# -*- encoding:UTF8 -*-
import time
import luna


class LunaDay:

    def __init__(self):
        pass

    def __call__(self):

        return time.strftime("%Y-%m-%d %A  %H:%M:%S") + \
               u"\n农历：%d年%d月%d日" % luna.getLunaDay(time.localtime()[0], time.localtime()[1], time.localtime()[2])
