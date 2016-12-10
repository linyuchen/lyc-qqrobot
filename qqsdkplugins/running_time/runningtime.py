# -*- encoding:UTF8 -*-

import time


class Time:

    def __init__(self):
        pass

    def __call__(self, start_time):
    
        """
        @param start_time:时间戳
        @type :float
        """

        t = time.time() - start_time
        hour = t / 3600
        minute = t % 3600 / 60
        second = t % 60
        start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        return u"开始运行于%s\n已经运行了%d小时%d分%d秒" % (start_time_str, hour, minute, second)
