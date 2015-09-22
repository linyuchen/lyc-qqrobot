#coding=UTF-8
import os
cur_path = os.path.dirname(__file__)
cur_path = cur_path or "."
db_path_str_g = cur_path + "/rpgdata.db"

table_name_str_g = "table_name" 

things_func_dict_g = {} # 物品功能函数字典

currency_name_str_g = u"金币" # 货币名称

####
# 基本事物字段字符串
####

tag_str_g = "tag" # 唯一的标识符
name_str_g = "name" # 事物名字
level_str_g = "level" # 等级
health_str_g = "health"# 当前血量
health_limit_str_g = "health_limit"# 满血量
mana_str_g = "mana" # 当前魔法值
mana_limit_str_g = "mana_limit"# 满魔量

min_attack_force_str_g = "min_attack_force" # 最小攻击力
max_attack_force_str_g = "max_attack_force" # 最大攻击力
defensive_str_g = "defensive" # 防御力
price_str_g = "price" # 价格
summary_str_g = "summary" # 介绍

####
# 人物字段字符串
####
person_table_name_str_g = "t_person" # 人物表名
power_str_g = "power" # 体力
level_health_str_g = "level_health" # 每级增加的血量
level_mana_str_g = "level_mana"  # 每级增加的魔法值
level_attack_force_str_g = "level_attack_force" # 每级增加的攻击力
level_defensive_str_g = "level_defensive" # 每级增加的防御力
level_die_gold_str_g = "level_die_gold" # 每级增加死亡掉落的财富
gold_str_g = "gold" # 拥有的财富
experience_str_g = "experience"# 当前经验值
die_experience_str_g = "die_experience" # 死亡掉落的经验值
die_gold_str_g = "die_gold" # 死亡掉落的财富 
up_experience_str_g = "up_experience"# 下一级所需的经验值
up_experience_percentage_str_g = "up_experience_percentage"# 下一级所需经验值为上一级的百分比
equip_list_str_g = "equip_list" # 装备列表
goods_list_str_g = "goods_list" # 物品列表
is_die_str_g = "is_die" # 是否已经死亡


######
# 物品字段
######
goods_table_name_str_g = "t_goods" # 物品表名

hlth_wt_w_tag_str_g = "hlth_wt_w" # 微型生命药水 tag
hlth_wt_x_tag_str_g = "hlth_wt_x" # 小型生命药水 tag
hlth_wt_z_tag_str_g = "hlth_wt_z" # 中型生命药水 tag
hlth_wt_d_tag_str_g = "hlth_wt_d" # 大型生命药水 tag

mana_wt_w_tag_str_g = "mana_wt_w" # 微型魔法药水 tag

hlth_stone_tag_str_g = "hlth_stone" # 生命宝石 tag
mana_stone_tag_str_g = "mana_stone" # 魔法宝石 tag
experience_book_tag_str_g = "experience_book" 

resurrection_stone_tag_str_g = "resurrection_stone" # 复活石 tag
#####
# 装备字段
#####

cat_sword_tag_str_g = "cat_sword"
cat_shield_tag_str_g = "cat_shield"

#七星宝剑
seven_star_sword_tag_str_g = "seven_star_sword"
#雷神之盾
thunder_shield_tag_str_g = "thunder_shield"
#####
# 背包
#####
knapsack_table_name_str_g = "t_knapsack" # 背包表名

####
# 物品分类
category_str_g = "category"
goods_category_str_g = "goods_category"
equip_category_str_g = "equip_category"
magic_category_str_g = "magic_category"


