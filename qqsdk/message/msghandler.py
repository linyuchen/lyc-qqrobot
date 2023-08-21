# coding=utf8
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple, Type, ClassVar

from common.logger import logger
from .friendmsg import FriendMsg
from .groupmsg import GroupMsg

GeneralMsg = Type[GroupMsg | FriendMsg]

config_path = Path(__file__).parent / "cmd_config.json"


def read_config():
    if not config_path.exists():
        return {}
    try:
        data = json.load(config_path.open("r", encoding="utf8"))
    except Exception as e:
        logger.error(f"读取命令开关配置失败：{e}")
        return {}
    return data


config_data = read_config()  # {"name": {"enabled": True, "exclude_groups": []}


def save_config():
    try:
        json.dump(config_data, config_path.open("w", encoding="utf8"), ensure_ascii=False)
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
    __enabled = True

    def __init__(self, **kwargs):
        self.instances.append(self)
        data = get_config(kwargs.get("name", self.name))
        self.__enabled = data["enabled"]
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
            self.__enabled = enabled
        data["enabled"] = self.__enabled
        save_config()

    def check_enabled(self, group_qq: str = ""):
        enabled = self.__enabled
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
        return isinstance(msg, self.bind_msg_types)

    def handle(self, msg: GeneralMsg):
        pass

    def get_module_name(self):
        return self.__module__.split(".")[1]


def set_msg_handler_enabled(name: str, enabled: bool, group_qq: str = ""):
    for handler in MsgHandler.get_handlers(name):
        handler.set_enabled(enabled, group_qq)
