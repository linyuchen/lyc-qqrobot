# coding=UTF8
from typing import List

"""
命令解析模块
"""


class CMD(object):

    def __init__(self, cmd_name, sep=" ", int_param_index: list[int] = (), param_len=0, handle_func=None,
                 alias: list[str] = ()):
        """
        paramSep: 命令与参数的分隔符，同时也是多个参数之间的分隔符
            如果为None 或者 False则不分割
        int_param_index:[int, ...]，第几个参数是数字, 如果不符合，不会调用handle_func
        handle_func: 处理命令的函数,
            如果有参数：handle_func(*参数)
        param_len: 参数个数
        """

        self.cmd_name = cmd_name
        self.alias = alias
        self.param_sep = sep
        self.int_param_index = int_param_index
        self.handle_func = handle_func
        self.paramList = []
        self.param_length = param_len

        self.original_cmd = ""
        self.original_param = ""

    def az(self, original_cmd):
        """
        解析命令
        成功返回True，反之False
        """

        self.original_cmd = original_cmd
        original_cmd = original_cmd.strip()
        cmd_name = ""
        cmds = list(self.alias) + [self.cmd_name]
        cmds.sort(key=len)
        for i in cmds:
            if original_cmd.startswith(i):
                cmd_name = i
        if not cmd_name:
            return False

        if self.param_length:  # 需要参数，进行参数分割
            cmd_name_length = len(cmd_name)
            if len(original_cmd) <= cmd_name_length:  # 如果没有参数
                return False

            if self.param_sep == " ":
                self.paramList = original_cmd.split()
            elif self.param_sep:
                self.paramList = original_cmd.split(self.param_sep)

            if self.paramList:
                cmd_name = self.paramList[0]
                self.paramList.pop(0)
                if not self.paramList:
                    return False
                self.original_param = self.param_sep.join(self.paramList)

            if not self.param_sep:  # 无分隔符
                self.paramList = [original_cmd[cmd_name_length:].strip()]
                # cmd_name = original_cmd[:cmd_name_length]
                self.original_param = self.paramList[0]
        else:
            cmd_name = original_cmd

        return cmd_name in self.alias or cmd_name == self.cmd_name

    def handle(self, cmd_content):
        """

        :param cmd_content: str， 命令字符串
        :return:
        """
        if not self.az(cmd_content):
            return
        if len(self.paramList) < self.param_length:
            return "命令不完整"

        for int_index in self.int_param_index:
            param = self.paramList[int_index]
            if not param.isdigit():
                return "命令第%d个参数必须是数字" % (int_index + 1)
            else:
                self.paramList[int_index] = int(param)

        if self.handle_func:
            if self.param_length:
                return self.handle_func(*self.paramList[:self.param_length])
            else:
                return self.handle_func()

    def get_param_list(self):
        """
        :return: 参数列表
        """

        return self.paramList

    def get_original_param(self):
        """
        :return: 除了命令部分剩下的参数字符串
        """
        return self.original_param


if "__main__" == __name__:
    def handle_test(*args):
        return ",".join(args)


    cmd = CMD(u"天气", param_len=1, int_param_index=[], handle_func=handle_test)
    print(cmd.handle(u"天气 上海"))
