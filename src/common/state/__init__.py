# -*- encoding:UTF8 -*-

import time

import psutil

start_time = time.time()


def state():
    t = time.time() - start_time
    hour = t / 3600
    minute = t % 3600 / 60
    second = t % 60
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    state_str = "开始运行于%s\n已经运行了%d小时%d分%d秒" % (start_time_str, hour, minute, second)
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    state_str += f"\nCPU使用率：{cpu_percent}%\n内存使用率：{memory.percent}%\n"
    return state_str


__all__ = ['state']
