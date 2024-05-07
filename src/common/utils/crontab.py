import datetime
import sched
import time
import traceback
from typing import Union
from threading import Thread


class Crontab(Thread):

    def __init__(self, minute: int | None = 0,
                 hour: int | None = None,
                 day_of_month: int | None = None,
                 month: int | None = None,
                 day_of_week: int | None = None,
                 func: Union[callable, None] = None):
        """
        :param minute: None 表示每分钟执行
        :param hour: None 表示每小时执行
        :param day_of_month: None 表示每天执行
        :param month: None 表示每月执行
        :param day_of_week: None 表示每周执行
        :param func: 要执行的函数
        """
        super().__init__()
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.func = func

    def job(self):
        # 在这里执行你的任务操作
        pass

    def __calc_next(self):
        next_time = self.calculate_next_execution(self.minute, self.hour, self.day_of_month, self.month,
                                                  self.day_of_week)
        return next_time.timestamp()

    def run(self):
        s = sched.scheduler(time.time, time.sleep)

        def run_job():
            try:
                if self.func:
                    self.func()
                else:
                    self.job()
            except:
                traceback.print_exc()
            s.enterabs(self.__calc_next(), 1, run_job)  # 设置下一次执行时间

        # 设置第一次执行的定时器
        s.enterabs(self.__calc_next(), 1, run_job)

        # 启动定时器
        s.run()

    @staticmethod
    def calculate_next_execution(minute: int | None = 0,
                                 hour: int | None = None,
                                 day_of_month: int | None = None,
                                 month: int | None = None,
                                 day_of_week: int | None = None):
        now = datetime.datetime.now()
        next_exec_time = now.replace(second=0, microsecond=0)

        if minute is not None:
            if minute < next_exec_time.minute:
                next_exec_time += datetime.timedelta(hours=1)
            next_exec_time = next_exec_time.replace(minute=minute)
        if hour is not None:
            if hour < next_exec_time.hour:
                next_exec_time += datetime.timedelta(days=1)
            next_exec_time = next_exec_time.replace(hour=hour)

        if day_of_week is not None:
            # 周几生效时，日月失效
            duration_day = day_of_week - next_exec_time.isoweekday()
            if duration_day < 0:
                duration_day += 7
            next_exec_time += datetime.timedelta(days=duration_day)
        else:
            # 日月生效
            if day_of_month is not None:
                # next_exec_time = next_exec_time.replace(day=day_of_month)
                if day_of_month < next_exec_time.day:
                    next_month = now.month + 1
                    if next_month > 12:
                        next_month = 1
                        next_exec_time = next_exec_time.replace(year=now.year + 1)
                    next_exec_time = next_exec_time.replace(month=next_month)
                next_exec_time = next_exec_time.replace(day=day_of_month)

            if month is not None:
                # next_exec_time = next_exec_time.replace(month=month)
                if month < next_exec_time.month:
                    next_exec_time = next_exec_time.replace(year=now.year + 1)
                next_exec_time = next_exec_time.replace(month=month)

        if next_exec_time < now:
            next_exec_time += datetime.timedelta(minutes=1)
        return next_exec_time


if __name__ == '__main__':
    def job():
        print("定时任务执行", datetime.datetime.now())


    t = Crontab.calculate_next_execution(minute=0, hour=8)
    print(t)
    Crontab(minute=None, func=job).start()
