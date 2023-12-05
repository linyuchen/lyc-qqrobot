# coding=utf8
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple, Type, ClassVar

from common.logger import logger
from .friendmsg import FriendMsg
from .groupmsg import GroupMsg

import config


CONFIG_KEY = "plugin_config"

GeneralMsg = Type[GroupMsg | FriendMsg]

config_data = config.get_config(CONFIG_KEY, {})  # {"name": {"enabled": True, "exclude_groups": []}


def save_config():
    try:
        config.set_config(CONFIG_KEY, config_data)
    except Exception as e:
        logger.error(f"保存命令开关配置失败：{e}")


def get_config(handler_name: str):
    return config_data.setdefault(handler_name, {"enabled": True, "exclude_groups": []})


@dataclass
class MsgHandler:
    name = ""  # 不是唯一的，同类型的可以一样
    desc = ""  # 描述 一般写'发送 xxx 触发xxx'
    qq_client: "qqsdk.qqclient.QQClientBase" = None
    is_async = False  # 为True时，handle函数会在新线程中执行
    bind_msg_types: Tuple[Type[GeneralMsg]] = ()  # 绑定的消息类型
    instances: ClassVar[list['MsgHandler']] = []
    priority = 1  # 优先级，越大越先执行
    # __exclude_groups: list[str] = field(default_factory=list)  # 不处理的群号
    global_enabled = True

    def __init__(self, **kwargs):
        class_name = self.__class__.__name__
        # 如果已经存在同名的插件，就不再添加到instances中
        if not list(filter(lambda i: i.__class__.__name__ == class_name, self.instances)):
            self.instances.append(self)
        name = kwargs.get("name", self.name)
        data = get_config(name)
        self.global_enabled = data["enabled"]
        self.__exclude_groups = data["exclude_groups"]

    @classmethod
    def get_handlers(cls, name):
        return list(filter(lambda i: i.name == name, cls.instances))

    def set_enabled(self, enabled: bool, group_qq: str):
        data = get_config(self.name)
        if group_qq:
            self.set_group_enabled(group_qq, enabled)
            data["exclude_groups"] = self.__exclude_groups
        else:
            self.global_enabled = enabled
        data["enabled"] = self.global_enabled
        save_config()

    def check_enabled(self, group_qq: str = ""):
        enabled = self.global_enabled
        if group_qq:
            enabled = enabled and group_qq not in self.__exclude_groups
        return enabled

    def set_group_enabled(self, group_qq: str, enabled: bool):
        if enabled:
            if group_qq in self.__exclude_groups:
                self.__exclude_groups.remove(group_qq)
        else:
            if group_qq not in self.__exclude_groups:
                self.__exclude_groups.append(group_qq)

    def check_type(self, msg: GeneralMsg):
        return type(msg) in self.bind_msg_types

    def handle(self, msg: GeneralMsg):
        pass

    def get_module_name(self):
        return self.__module__.split(".")[1]


def set_msg_handler_enabled(name: str, enabled: bool, group_qq: str = ""):
    handlers = MsgHandler.get_handlers(name)
    if not handlers:
        raise Exception(f"插件 {name} 不存在")
    for handler in handlers:
        if group_qq:
            if not handler.global_enabled:
                raise Exception(f"插件 {name} 已被机器人主人禁用，无法在群内启用")
        handler.set_enabled(enabled, group_qq)
