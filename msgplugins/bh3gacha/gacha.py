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


equipments = []


def read():
    with open(PATH_扩充装备概率, "rb") as f:
        current_star = 0
        current_type = None
        current_probability = 0

        for line in f.readlines():
            line = line.decode("utf8")
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            elif line.startswith("!"):
                line = line[1: -1]  # 去掉头部!号和尾部%号
                line_tuple = line.split(" ")
                current_star = int(line_tuple[0][0])  # 星级
                current_type = line_tuple[1]  # 类型
                current_probability = float(line_tuple[2])  # 概率
            else:
                _e = Equipment(probability=current_probability, type_name=current_type, star=current_star, name=line)
                equipments.append(_e)


read()
pool = []
for e in equipments:
    e: Equipment
    pool.extend([e] * int(e.probability * 1000))


result = random.choice(pool)
print(result)

