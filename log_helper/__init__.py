# -*- coding:UTF-8 -*-
__author__ = u'林雨敐的那只神经喵喵'

import logging
import locale
import os
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

local_encoding = locale.getdefaultlocale()[1]


def get_cur_path():
    cur_path = os.path.dirname(__file__) or "."
    cur_path += "/"
    return cur_path


class BaseHandler(object):

    def __init__(self):

        self.datefmt = "%Y-%m-%d %H:%M:%S"
        self.msgfmt = "[%(asctime)s]: %(levelname)s %(pathname)s %(lineno)s \n \t%(message)s\n"
        self.handler_level = None
        self.file_name = ""  # 保存的文件名

    def get_handler(self):
        path = get_cur_path() + self.file_name
        handler = TimedRotatingFileHandler(path, when='midnight', backupCount=5, encoding=local_encoding)
        formatter = logging.Formatter(self.msgfmt, self.datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(self.handler_level)
        return handler


class BaseLogger(object):

    def __init__(self):
        self.logger_name = ""
        self.logging_level = None

    def get_logger(self):
        if self.logger_name not in Logger.manager.loggerDict:
            __logger = logging.getLogger(self.logger_name)
            __logger.setLevel(self.logging_level)
        __logger = logging.getLogger(self.logger_name)
        return __logger

    def add_handler(self, handler):
        """

        :param handler: MyHandler实例
        :return:
        """
        self.get_logger().addHandler(handler.get_handler())


class GeneralHandler(BaseHandler):

    def __init__(self, file_name=""):
        super(GeneralHandler, self).__init__()
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = "all.log"
        self.handler_level = logging.NOTSET


class ErrHandler(BaseHandler):

    def __init__(self, file_name=""):
        super(ErrHandler, self).__init__()
        if file_name:
            self.file_name = file_name
        else:
            self.file_name = "error.log"
        self.handler_level = logging.ERROR


class ErrLogger(BaseLogger):
    """
    只打印ERROR级别的log
    """
    def __init__(self, file_name=""):
        super(ErrLogger, self).__init__()
        self.logging_level = logging.ERROR
        self.logger_name = "error"
        self.add_handler(ErrHandler(file_name))


class GeneralLogger(BaseLogger):
    """
    打印全部log
    error的log会同时被ErrHandler处理
    """
    def __init__(self, file_name="", err_file_name=""):
        super(GeneralLogger, self).__init__()
        self.logging_level = logging.INFO
        self.logger_name = "all"
        self.add_handler(ErrHandler(err_file_name))
        self.add_handler(GeneralHandler(file_name))

err_logger = ErrLogger().get_logger()
logger = GeneralLogger().get_logger()

if __name__ == "__main__":
    logger.info(u"呵呵")
    # err_logger.warning(u"报错")
