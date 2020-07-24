# coding=UTF8

import os
import random
from typing import List
from dataclasses import dataclass

PATH_CURRENT = os.path.dirname(__file__)
PATH_DATA_DIR = os.path.join(PATH_CURRENT, "概率")
PATH_扩充装备概率 = os.path.join(PATH_DATA_DIR, "扩充装备.txt")


@dataclass
class Equipment:
    probability: float
    type_name: str
    star: int
    name: str


class TextParser:
    def __init__(self, path: str):
        with open(path, "rb") as f:
            for line in f.readlines():
                line = line.decode("utf8")
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                elif line.startswith("!"):
                    self.parse_category(line)
                else:
                    self.parse_item(line)

    def parse_category(self, line: str):
        raise NotImplementedError

    def parse_item(self, item: str):
        raise NotImplementedError


class EquipmentParser(TextParser):

    def __init__(self, path: str):
        self.current_star = 0
        self.current_type = None
        self.current_probability = 0
        self.equipments = []
        super(EquipmentParser, self).__init__(path)

    def parse_category(self, line: str):
        line = line[1: -1]  # 去掉头部!号和尾部%号
        line_tuple = line.split()
        self.current_star = int(line_tuple[0][0])  # 星级
        self.current_type = line_tuple[1]  # 类型
        self.current_probability = float(line_tuple[2])  # 概率

    def parse_item(self, item: str):
        _e = Equipment(probability=self.current_probability, type_name=self.current_type, star=self.current_star,
                       name=item)
        self.equipments.append(_e)


p = EquipmentParser(PATH_扩充装备概率)
print(p.equipments)
