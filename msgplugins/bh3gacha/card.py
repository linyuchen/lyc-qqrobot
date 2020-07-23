# coding=UTF8
from dataclasses import dataclass


class CardType:
    ROLE = "角色"
    CHIP = "角色碎片"
    EQUIPMENT = "装备"  # 武器或者圣痕
    MATERIAL = "材料"  # 吼姆宝藏、秘银、碎片、装备升级材料


@dataclass
class Card:

    """
    可抽取的东西
    """
    name: str = ""
    file_name: str = ""
    card_type: str = ""  # CardType

    def get_file_name(self):
        if not self.file_name:
            return f"{self.name}.png"


class RoleCardLevel:
    A = "a"
    B = "b"
    S = "s"


@dataclass
class RoleCard(Card):
    """
    角色卡
    """
    card_type = CardType.ROLE
    level: str = RoleCardLevel.S


@dataclass
class RoleChipCard(Card):
    """
    角色碎片
    """



@dataclass
class EquipmentCard(Card):
    level: int = 4  # 星级 只能是3或者4


@dataclass
class MaterialCard(Card):
    """
    材料固定3星
    """


# 所有S角色的名字
class SRoleNames:
    白骑士月光 = "白骑士·月光"


# 所有四星武器名字
class Star4WeaponNames:
    天殛之钥 = "天殛之钥"


# 所有4星圣痕名字
class Star4SHNames:
    贝纳勒斯上 = "贝纳勒斯上"


# 所有三星武器名字
class Star4WeaponNames:
    水妖精I型 = "水妖精I型"


# 所有3星圣痕名字
class Star3SHNames:
    阿提拉上 = "阿提拉上"

