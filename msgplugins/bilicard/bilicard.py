import re
import time
import uuid
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from urllib import request

import requests
from PIL import Image, ImageFont, ImageDraw

TITLE_MAX_LEN = 120
TITLE_SPLIT_LEN = 23

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.35 ",
    "Referer": "https://www.bilibili.com/",
    "Accept": "application/json;charset=UTF-8"
}


def get_bv_id(text: str):
    # 正则检查B站视频BV号
    b23tv = re.findall("(?<=b23.tv/)\w*", text)
    if b23tv:
        text = request.urlopen(f"https://b23.tv/{b23tv[0]}").geturl()
    result = re.findall("(?<=BV)\w*", text)
    return result and result[0] or ""


def get_video_info(bv_id: str) -> None | dict:
    response_body = requests.get(f"http://api.bilibili.com/x/web-interface/view?bvid={bv_id}",
                                 headers=headers).json().get("data", {})
    if not response_body:
        return
    video_info = {
        "title": response_body["title"],
        "desc": response_body.get("desc", ""),
        "cover_url": response_body["pic"],
        "upload_time": time.strftime("%Y/%m/%d %H:%M", time.localtime(response_body["pubdate"])),
        "duration":
            f"{response_body['duration'] // 60}:{response_body['duration'] - response_body['duration'] // 60 * 60}",
        "view": response_body["stat"]["view"],
        "danmu": response_body["stat"]["danmaku"],
        "like": response_body["stat"]["like"],
        "coin": response_body["stat"]["coin"],
        "share": response_body["stat"]["share"],
        "favorite": response_body["stat"]["favorite"],
        "owner": f"{response_body['owner']['name']}",
        "owner_face": f"{response_body['owner']['face']}"
    }
    return video_info


def gen_text(bv_id: str) -> str:
    video_info = get_video_info(bv_id)
    if not video_info:
        return ""
    # 利用video_info生成视频简要说明
    title = video_info["title"]
    desc = video_info["desc"]
    duration = video_info["duration"]
    view = video_info["view"]
    danmu = video_info["danmu"]
    like = video_info["like"]
    coin = video_info["coin"]
    share = video_info["share"]
    favorite = video_info["favorite"]
    owner = video_info["owner"]
    upload_time = video_info["upload_time"]
    # desc超过30字则截断
    # if len(desc) > 40:
    #     desc = desc[:40] + "..."
    # 组装成文字
    text = f"标题：{title}\n\n" \
           f"简介：{desc}\n\n" \
           f"时长：{duration:<7}播放：{view:<7}\n" \
           f"弹幕：{danmu:<7}点赞：{like:<7}\n" \
           f"硬币：{coin:<7}收藏：{favorite:<7}\n" \
           f"分享：{share:<7}上传时间：{upload_time}\n作者：{owner}\n"

    return text


def gen_image(bv_id: str) -> str:
    video_info = get_video_info(bv_id)
    if not video_info:
        return ""
    save_path = Path(__file__).parent / f"{uuid.uuid4()}.png"
    image = Image.new("RGB", (530, 620), (245, 243, 243))
    image.paste((220, 220, 220), (0, 480, 530, 620))
    cover = Image.open(BytesIO(
        requests.get(video_info["cover_url"], headers=headers).content)).resize((464, 290), Image.ANTIALIAS)
    cover_size = (34, 34, 34 + cover.width, 34 + cover.height)
    image.paste(cover, cover_size)

    # desc_draw = ImageDraw.Draw(image)
    # 作者信息
    face = Image.open(BytesIO(
        requests.get(video_info["owner_face"], headers=headers).content)).resize((80, 80), Image.ANTIALIAS)
    face_size = (34, 510, 34 + face.width, 510 + face.height)
    face_draw = ImageDraw.Draw(image)

    face_draw.text((face.width + 50, face_size[1] + 10), f"{video_info['owner']}\n{video_info['upload_time']} 上传",
                   fill=(20, 20, 20),
                   font=ImageFont.truetype(str(Path(__file__).parent / "fonts/SourceHanSansSC-Heavy-2.otf"), 21))
    image.paste(face, face_size)

    cover_draw = ImageDraw.Draw(image)
    least_text = video_info["title"][:TITLE_MAX_LEN]
    title = ""
    title_len = len(least_text)
    for i in range(0, title_len, TITLE_SPLIT_LEN):
        title += least_text[i: i + TITLE_SPLIT_LEN] + "\n"

    if len(video_info["title"]) > TITLE_MAX_LEN:
        title += f"..."
    detail_text = f"\n" \
        # f"{video_info['desc'][:30]}\n" \
    detail_text = f"\n" \
                  f"{Decimal(video_info['view'] / 10000).quantize(Decimal('0.0')) if video_info['view'] > 10000 else video_info['view']}" \
                  f"{'w' if video_info['view'] > 10000 else ''}次观看·" \
                  f"{Decimal(video_info['like'] / 10000).quantize(Decimal('0')) if video_info['like'] > 10000 else video_info['like']}" \
                  f"{'w' if video_info['like'] > 10000 else ''}点赞·" \
                  f"{Decimal(video_info['coin'] / 10000).quantize(Decimal('0')) if video_info['coin'] > 1000 else video_info['coin']}" \
                  f"{'w' if video_info['coin'] > 10000 else ''}硬币·" \
                  f"{Decimal(video_info['favorite'] / 10000).quantize(Decimal('0')) if video_info['favorite'] > 10000 else video_info['favorite']}" \
                  f"{'w' if video_info['favorite'] > 10000 else ''}收藏"
    # 标题
    cover_draw.text((cover_size[0], cover_size[3]), title, fill=(20, 20, 20),
                    font=ImageFont.truetype(str(Path(__file__).parent / "fonts/SourceHanSansSC-Heavy-2.otf"), 20))
    # 详情
    cover_draw.text((cover_size[0], 410), detail_text, fill=(50, 50, 50),
                    font=ImageFont.truetype(str(Path(__file__).parent / "fonts/SourceHanSansSC-Heavy-2.otf"), 21))
    image.save(save_path)
    return str(save_path)


if __name__ == "__main__":
    _text = "https://www.bilibili.com/video/BV1814y1V7RS/?spm_id_from=333.1073.channel.secondary_floor_video.click"
    # _text = "https://www.bilibili.com/video/BV1Ps4y1v79v/?spm_id_from=444.41.list.card_archive.click&vd_source=210c4e2f9f0cdc36cd087b10ec64eedc"
    bvid = get_bv_id(_text)
    print(gen_text(bvid))
    # bvid and gen_image(video_info)
