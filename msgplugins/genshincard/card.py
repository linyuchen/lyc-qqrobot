# coding=UTF8
import uuid
import random
import os
from PIL import Image

root_path = os.path.dirname(__file__)


def create_slot(filename: str):
    p_str = filename.split(".")[0]
    p_attr = p_str.split("_")
    star = p_attr[0]
    c_or_e = p_attr[1]
    category = p_attr[2]
    name = p_attr[3]

    i_slot = Image.open(root_path + "/img/slot.png")

    i_content_resize = (184, 665)
    i_content_region = (10, 55)
    # 粘贴人物或者装备
    i_content = Image.open(root_path + "/img/池子/" + filename)
    if c_or_e == "e":
        if category == "法器":
            i_content_resize = (184, 184)
            i_content_region = (10, 295)
        else:
            i_content_resize = (184, 590)
            i_content_region = (10, 95)

    i_content = i_content.resize(i_content_resize)
    i_slot.paste(i_content, box=i_content_region, mask=i_content)

    # 粘贴星级
    i_star = Image.open(f"{root_path}/img/星级/{star}.png")
    i_slot.paste(i_star, box=((i_slot.size[0] - i_star.size[0]) // 2, 720), mask=i_star)

    # 粘贴属性
    i_attr = Image.open(f"{root_path}/img/分类/{category}.png")
    i_slot.paste(i_attr, box=(49, 601), mask=i_attr)
    return i_slot


slots = random.choices(os.listdir(f"{root_path}/img/池子"), k=10)


def sorted_key(a):
    star = int(a[0])
    if a[2] == "c":
        star += 2
    return star


# slots = sorted(slots, key=sorted_key, reverse=True)

# 所有卡总共分成一千份
# 有6份是五星物品
# 51份是四星物品
# 941份是三星物品
slots_ints = [5] * 6 + [4] * 51 + [3] * 941

star_5_slots = [i for i in os.listdir(f"{root_path}/img/池子") if i[0] == "5"]
star_4_slots = [i for i in os.listdir(f"{root_path}/img/池子") if i[0] == "4"]
star_3_slots = [i for i in os.listdir(f"{root_path}/img/池子") if i[0] in "321"]


def gacha_once():
    return random.choice(slots_ints)


def gacha():
    root = Image.open(f"{root_path}/img/背景.png")
    slot1_x = 279
    slot1_y = 435
    results = [gacha_once() for i in range(10)]

    # 十连保底
    if 4 not in results and 5 not in results:
        _4_or_5_slots_ints = [5] + [4] * 9
        results[0] = random.choice(_4_or_5_slots_ints)

    tmp_slots = []
    for star_int in results:
        if star_int == 5:
            _slots = star_5_slots
        elif star_int == 4:
            _slots = star_4_slots
        else:
            _slots = star_3_slots
        tmp_slots.append(random.choice(_slots))
    tmp_slots = sorted(tmp_slots, key=sorted_key, reverse=True)
    for s in tmp_slots:
        slot = create_slot(s)
        root.paste(slot, box=(slot1_x, slot1_y), mask=slot)
        slot1_x += 200

    result_path = f"{root_path}/results/{uuid.uuid4()}.jpg"
    root = root.convert("RGB")
    root.save(result_path, "jpeg", quality=60)
    return result_path


gacha()
