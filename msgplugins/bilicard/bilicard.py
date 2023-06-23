import re
import time
import uuid
from io import BytesIO
from pathlib import Path
from urllib import request

import requests
from PIL import Image, ImageDraw, ImageFont

from msgplugins.chatgpt.chatgpt import gpt_35

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
        **response_body,
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
        "owner_face": f"{response_body['owner']['face']}",
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


cookies = "buvid3=D8857590-C5C6-43D1-A61C-F18C2C04CCC0167632infoc; LIVE_BUVID=AUTO7516361994818922; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; blackside_state=0; buvid4=E0EA01F3-3299-54F7-8A06-1E15FB7D29A647831-022012619-RYZwLL8nRmXgxAPub0ToFw%3D%3D; buvid_fp_plain=undefined; DedeUserID=6961865; DedeUserID__ckMd5=866e87c0bc335a2a; is-2022-channel=1; b_nut=100; fingerprint3=6edb9feba98f9d0c3cf499ff5fd81847; _uuid=F3FD45DF-3B4B-8D23-AF66-9C3248F75EDD18995infoc; rpdid=|(um|uYYY~)l0J'uYY)Yu)l)k; go_old_video=-1; b_ut=5; home_feed_column=5; i-wanna-go-feeds=-1; nostalgia_conf=-1; CURRENT_PID=8e452430-cd7f-11ed-9bac-0d5b6943bfd2; hit-new-style-dyn=1; hit-dyn-v2=1; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; bp_article_offset_6961865=799955294267375600; fingerprint=e108557d3d7bd729cb1e4fd1184dc209; CURRENT_QUALITY=120; CURRENT_FNVAL=4048; kfcFrom=itemshare; from=itemshare; msource=h5; share_source_origin=QQ; bsource=share_source_qqchat; SESSDATA=fa2711ba%2C1702963527%2Cb96eb%2A62g2NI3aZz7IvKEWBbz19ojEtJFWgmjpe1fKs8G0Byi-7DTG9GiE1gdRttl8a2P-QyFy1ahQAAQQA; bili_jct=5906533e9dcd9b8860118cd388824f7f; sid=6rbzcicr; buvid_fp=e108557d3d7bd729cb1e4fd1184dc209; PVID=1; b_lsid=C1B2E10105_188EA46BA78; bp_video_offset_6961865=810536349680533500"
cookies = re.findall("(.*?)=(.*?); ", cookies)
cookies = dict(cookies)
session = requests.session()
session.cookies.update(cookies)


def get_subtitle(aid, cid):
    url = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"

    res = session.get(url, headers=headers, cookies=cookies).json()
    subtitles = res["data"]["subtitle"]["subtitles"]
    subtitle_urls = []
    for sub_t in subtitles:
        if sub_t["lan"] in ("ai-zh", "zh-Hans"):
            subtitle_urls.append("https:" + sub_t["subtitle_url"])

    subtitle_content = []
    for subtitle_url in subtitle_urls:
        res = requests.get(subtitle_url, headers=headers).json()
        for i in res["body"]:
            subtitle_content.append(i["content"])
    subtitle = "\n".join(subtitle_content)
    return subtitle


def get_video_summary_by_ai(aid, cid) -> str:
    subtitle = get_subtitle(aid, cid)
    if subtitle:
        res = gpt_35("", "#有如下一个视频，请总结他:\n" + subtitle)
        return res
    else:
        return ""


def gen_image(bv_id: str) -> tuple[str, str, str]:
    video_info = get_video_info(bv_id)
    if not video_info:
        return "", "", ""
    base_path = Path(__file__).parent
    # save_path = base_path / f"test.png"
    save_path = base_path / f"{uuid.uuid4()}.png"
    image = Image.new("RGBA", (560, 470), (255, 255, 255, 255))
    # image.paste((220, 220, 220), (0, 480, 530, 620))
    cover = Image.open(BytesIO(
        requests.get(video_info["cover_url"], headers=headers).content)).resize((560, 310), Image.ANTIALIAS)
    cover_size = (0, 0, 560, 310)

    # mask = Image.new("L", image.size, (255, 255, 255))
    # # 创建 draw 对象
    # draw = ImageDraw.Draw(mask)
    # # 绘制圆角矩形
    # draw.rounded_rectangle((0, 0, image.width, image.height), radius=20, fill=0)
    #
    # # 将 mask 应用到 image 上
    # image.putalpha(mask)
    # 创建遮罩层
    # mask = Image.new("L", cover.size, 0)
    # draw = ImageDraw.Draw(mask)
    # # 绘制圆角矩形
    # draw.rounded_rectangle((0, 0, cover.width, cover.height), radius=20, fill=255)
    # # 将遮罩层与 cover 合并
    # cover.putalpha(mask)

    # 将带有圆角的 cover 贴到 image 上
    image.paste(cover, cover_size)

    # 添加一个灰色透明层，用来显示播放数量，弹幕数量和视频时长
    mask = Image.new("RGBA", (560, 50), (150, 150, 150, 170))
    image_play_icon = Image.open(base_path / "icon-play.png").resize((40, 40))
    image.paste(mask, (0, cover.height - 45), mask)

    # 添加播放数量
    image.paste(image_play_icon, (20, cover.height - 45), image_play_icon)
    text_draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(Path(__file__).parent.parent.parent / "common/仓耳今楷01-9128-W05.otf"),
                              20)
    view_count = video_info["view"]
    if view_count >= 10000:
        # 超过一万播放量则显示万,保留一位小数
        view_count = f"{view_count / 10000:.1f}万"
    text_draw.text((70, cover.height - 35), f"{view_count}", font=font)

    # 添加弹幕数量
    image_danmu = Image.open(base_path / "icon-danmu.png").resize((40, 40))
    image.paste(image_danmu, (190, cover.height - 45), image_danmu)
    text_draw = ImageDraw.Draw(image)
    danmu_count = video_info["danmu"]
    text_draw.text((240, cover.height - 35), f"{danmu_count}", font=font)
    # 添加视频时长
    hour, minute = video_info["duration"].split(":")
    text_draw.text((500, cover.height - 35), f"{hour:0>2}:{minute:0>2}", font=font)
    # 添加标题,15个字一行
    line_width = 30
    next_height = cover.height + 10
    for i in range(len(video_info["title"]) // line_width + 1):
        next_height = cover.height + 10 + i * 40
        text_draw.text((20, next_height), f"{video_info['title'][i * line_width:(i + 1) * line_width]}", font=font,
                       fill=(0, 0, 0))

    # 作者信息
    text_draw.text((20, cover.height + 80), f"UP: {video_info['owner']}", font=font, fill=(0, 0, 0))
    # 添加视频上传时间
    text_draw.text((270, cover.height + 80), f"上传时间: {video_info['upload_time']}", font=font, fill=(0, 0, 0))
    image.save(save_path)
    try:
        summary = get_video_summary_by_ai(video_info["aid"], video_info["cid"])
    except:
        summary = ""
    return str(save_path), video_info["desc"], ("AI总结：" + summary) if summary else ""


if __name__ == "__main__":
    _text = "https://www.bilibili.com/video/BV1814y1V7RS/?spm_id_from=333.1073.channel.secondary_floor_video.click"
    _text = "https://www.bilibili.com/video/BV1Ps4y1v79v/?spm_id_from=444.41.list.card_archive.click&vd_source=210c4e2f9f0cdc36cd087b10ec64eedc"
    _text = "https://www.bilibili.com/video/BV1Ss4y1b7r9/?spm_id_from=333.1007.partition_recommend.content.click"

    # 白色背景封面
    _text = "https://www.bilibili.com/video/BV1sP411g7PZ/?spm_id_from=333.337.search-card.all.click&vd_source=210c4e2f9f0cdc36cd087b10ec64eedc"

    # _text = "https://www.bilibili.com/video/BV1Nm4y1q7rT"
    bvid = get_bv_id(_text)
    # print(gen_text(bvid))
    # gen_image(bvid)
    video_info = get_video_info(bvid)
    _r = get_video_summary_by_ai(video_info["aid"], video_info["cid"])
    print(_r)
