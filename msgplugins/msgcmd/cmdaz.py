# coding=UTF8

"""
命令解析模块
"""
import re
import threading
from typing import Callable, Type

from qqsdk.message import BaseMsg, GroupMsg, FriendMsg, MsgHandler
from .permission import CMDPermissions, CMDPermissionGroup, check_permission


class CMD(object):

    def __init__(self, cmd_name, sep=" ", int_param_index: list[int] = (), param_len=0, handle_func=None,
                 alias: list[str] = (), ignores: list[str] = ()):
        """
        sep: 命令与参数的分隔符，同时也是多个参数之间的分隔符
            如果为None 或者 False则不分割
        int_param_index:[int, ...]，第几个参数是数字, 如果不符合，不会调用handle_func
        handle_func: 处理命令的函数,
            如果有参数：handle_func(*参数)
        param_len: 参数个数, -1表示不限制
        """

        self.cmd_name = cmd_name
        self.alias = alias
        self.param_sep = sep
        self.int_param_index = int_param_index
        self.handle_func = handle_func
        self.params = []
        self.param_length = param_len

        self.input_text = ""
        self.input_param_text = ""
        self.ignores = ignores

    def az(self, input_text):
        """
        解析命令
        成功返回参数列表
        失败返回False
        """
        if not self.cmd_name:
            return True
        self.input_text = input_text
        input_text = input_text.strip()

        for i in self.ignores:
            if input_text.startswith(i):
                return False
        cmd_name = ""
        cmds = list(self.alias) + [self.cmd_name]

        def _sort_key(x):
            if isinstance(x, str):
                return len(x)
            else:
                return 0
        cmds.sort(key=_sort_key, reverse=True)
        # 检查输入是不是以命令开头
        for i in cmds:
            if isinstance(i, str):
                if input_text.startswith(i):
                    cmd_name = i
                    break
            elif isinstance(i, re.Pattern):
                r = re.findall(i, input_text)
                if r:
                    cmd_name = r[0]
                    break
        if not cmd_name:
            return False

        # 切割参数
        params_str = input_text[len(cmd_name):]
        # 检查是参数是否是对应的分隔符开头
        if self.param_sep and self.param_length != 0:
            if not params_str and self.param_length == -1:
                pass
            elif not params_str.startswith(self.param_sep):
                return False
        params_str = params_str.strip()
        self.input_param_text = params_str
        if self.param_length > 0:
            params = params_str.split(self.param_sep or None, maxsplit=self.param_length - 1)
            if len(params) < self.param_length:
                return False
            self.params = params[:self.param_length]

        else:
            self.params = params_str.split(self.param_sep or None)

        if self.param_length == 0:
            return self.params == [""]
        return self.params

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

        return list(filter(bool, self.params))

    def get_original_param(self):
        """
        :return: 除了命令部分剩下的参数字符串
        """
        return self.input_param_text


def on_command(cmd_name,
               sep=" ",
               int_param_index: list[int] = (),
               param_len=0,
               alias: tuple[str | re.Pattern, ...] = (),
               ignores: tuple[str] = (),
               bind_msg_type: tuple[Type[GroupMsg | FriendMsg | BaseMsg], ...] = (GroupMsg, FriendMsg),
               desc: str = "",
               at_sep: str = "",
               auto_destroy: bool = True,
               cmd_group_name: str = "",
               permission: CMDPermissions | CMDPermissionGroup = None,
               is_async: bool = False,
               priority: int = 1,
               ignore_at_other: bool = True,
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
    :param auto_destroy: 是否自动销毁消息
    :param cmd_group_name: 命令组名
    :param permission: 命令权限
    :param is_async: 是否异步
    :param priority: 优先级, 数字越大优先级越高
    :param ignore_at_other: 是否忽略at其他人的消息
    :return:
    """
    if not cmd_group_name:
        cmd_group_name = cmd_name

    def decorator(func: Callable[[BaseMsg, list[str]], None]):
        def handle(self, msg: GroupMsg | FriendMsg):
            cmd = CMD(cmd_name,
                      at_sep if isinstance(msg, GroupMsg) and msg.is_at_me else sep,
                      int_param_index,
                      param_len,
                      alias=list(alias),
                      ignores=list(ignores),
                      )
            if not (cmd.az(msg.msg.strip()) is False):
                if permission:
                    if not check_permission(msg, permission):
                        return msg.reply(f"您没有权限使用 {cmd_name} 命令")
                if auto_destroy and cmd_name:
                    msg.destroy()
                if ignore_at_other and isinstance(msg, GroupMsg) and msg.is_at_other:
                    return
                if is_async:
                    threading.Thread(target=func, args=(msg, cmd.get_param_list()), daemon=True).start()
                else:
                    func(msg, cmd.get_param_list())

        _class = type(func.__name__, (MsgHandler,), {
            'desc': desc,
            'is_async': is_async,
            'bind_msg_types': bind_msg_type,
            'handle': handle,
            'name': cmd_group_name,
            'priority': priority,
        })

        return _class

    return decorator
