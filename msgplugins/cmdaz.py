# coding=UTF8

"""
命令解析模块
"""

from typing import Callable, Type

from qqsdk.message import BaseMsg, GroupMsg, FriendMsg


class CMD(object):

    def __init__(self, cmd_name, sep=" ", int_param_index: list[int] = (), param_len=0, handle_func=None,
                 alias: list[str] = (), ignores: list[str] = ()):
        """
        sep: 命令与参数的分隔符，同时也是多个参数之间的分隔符
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
        self.params = []
        self.param_length = param_len

        self.original_cmd = ""
        self.original_param = ""
        self.ignores = ignores

    def az(self, original_cmd):
        """
        解析命令
        成功返回True，反之False
        """

        self.original_cmd = original_cmd
        original_cmd = original_cmd.strip()

        for i in self.ignores:
            if original_cmd.startswith(i):
                return False
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
                self.params = original_cmd.split()
            elif self.param_sep:
                self.params = original_cmd.split(self.param_sep)

            if self.params:
                cmd_name = self.params[0]
                self.params.pop(0)
                if not self.params:
                    return False
                self.original_param = self.param_sep.join(self.params)

            if not self.param_sep:  # 无分隔符
                self.params = [original_cmd[cmd_name_length:].strip()]
                # cmd_name = original_cmd[:cmd_name_length]
                self.original_param = self.params[0]
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
        if len(self.params) < self.param_length:
            return "命令不完整"

        for int_index in self.int_param_index:
            param = self.params[int_index]
            if not param.isdigit():
                return "命令第%d个参数必须是数字" % (int_index + 1)
            else:
                self.params[int_index] = int(param)

        if self.handle_func:
            if self.param_length:
                return self.handle_func(*self.params[:self.param_length])
            else:
                return self.handle_func()

    def get_param_list(self):
        """
        :return: 参数列表
        """

        return self.params

    def get_original_param(self):
        """
        :return: 除了命令部分剩下的参数字符串
        """
        return self.original_param

    def get_original_param_list(self):
        return self.original_param.split(self.param_sep or None, maxsplit=self.param_length)


def on_command(cmd_name,
               sep=" ",
               int_param_index: list[int] = (),
               param_len=0,
               alias: tuple[str, ...] = (),
               ignores: tuple[str] = (),
               bind_msg_type: tuple[Type[GroupMsg | FriendMsg], ...] = (GroupMsg,),
               desc: str = "",
               at_sep: str = ""
               ):
    """
    装饰器，用于注册命令
    :param cmd_name: 命令名
    :param sep: 命令与参数的分隔符，同时也是多个参数之间的分隔符
        如果为None 或者 False则不分割
    :param int_param_index: [int, ...]，第几个参数是数字, 如果不符合，不会调用handle_func
    :param param_len: 参数个数
    :param alias: 别名
    :param ignores: 忽略的命令
    :param bind_msg_type: 绑定的消息类型
    :param desc: 命令描述
    :param at_sep: at之后的命令分隔符
    :return:
    """

    from qqsdk.message import MsgHandler

    def decorator(func: Callable[[BaseMsg, list[str]], None]):
        def handle(self, msg: GroupMsg | FriendMsg):
            cmd = CMD(cmd_name,
                      at_sep if isinstance(msg, GroupMsg) and msg.is_at_me else sep,
                      int_param_index,
                      param_len,
                      alias=list(alias),
                      ignores=list(ignores))
            if cmd.az(msg.msg.strip()):
                msg.destroy()
                return func(msg, cmd.get_original_param_list())

        _class = type(func.__name__, (MsgHandler,), {
            'desc': desc,
            'is_sync': True,
            'bind_msg_types': bind_msg_type,
            'handle': handle,
        })

        return _class

    return decorator


if "__main__" == __name__:
    def handle_test(*args):
        return ",".join(args)


    test_cmd = CMD("天气", param_len=1, int_param_index=[], handle_func=handle_test)
    print(test_cmd.handle("天气 上海"))
    test_cmd = CMD("#", sep="", param_len=1, ignores=["#include"])
    print(test_cmd.az("#include <iostream>"))


    @on_command("test")
    def test(msg):
        print(msg)


    print(test)
