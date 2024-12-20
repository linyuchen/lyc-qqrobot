import re
import tempfile
import time
from io import BytesIO
from pathlib import Path, PurePath

import httpx
from PIL import Image, ImageDraw, ImageFont

from ..chatgpt.chatgpt import chat
from ..stringplus import split_lines

# session = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.35",
    "Referer": "https://www.bilibili.com/",
    "Accept": "application/json;charset=UTF-8"
}
session = httpx.AsyncClient(headers=headers, follow_redirects=True)


def get_cookie():
    base_path = PurePath(__file__).parent
    with open(base_path / "cookie.txt") as f:
        cookies = f.read()
        cookies = re.findall("(.*?)=(.*?); ", cookies)
        cookies = dict(cookies)
        session.cookies = cookies


def check_is_b23(text: str) -> []:
    b23tv = re.findall("(?<=b23.tv/)\w*", text)
    return b23tv


async def b32_to_bv(b23tv: str) -> str:
    """
    b23.tv链接转BV链接
    """
    url = f"https://b23.tv/{b23tv}"
    url = (await session.get(url)).url
    return str(url)


def get_bv_id(text: str):
    # 正则检查B站视频BV号
    result = re.findall(r"(?<=BV)\w+", text, re.I)
    return result and result[0] or ""


def get_av_id(text: str):
    result = re.findall(r"(?<=av)\d{4,}", text, re.I)
    return result and result[0] or ""


async def get_video_info(bv_id: str = "", av_id: str = "") -> None | dict:
    # get_cookie()
    url = ""
    if bv_id:
        url = f"http://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    elif av_id:
        url = f"http://api.bilibili.com/x/web-interface/view?aid={av_id}"
    res = await session.get(url)
    response_body = res.json().get("data", {})
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


# 获取评论，https://api.bilibili.com/x/v2/reply/wbi/main?oid=683107021&type=1&mode=3
# todo: 获取指定评论，然后判断是否是up的评论，将此评论也放到ai总结里面去

async def gen_text(bv_id: str) -> str:
    video_info = await get_video_info(bv_id)
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


async def get_subtitle(aid: str, cid: str):
    get_cookie()
    url = f"https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid}"

    res = (await session.get(url)).json()
    subtitles = res["data"]["subtitle"]["subtitles"]
    subtitle_urls = []
    for sub_t in subtitles:
        if sub_t["lan"] in ("ai-zh", "zh-Hans"):
            subtitle_urls.append("https:" + sub_t["subtitle_url"])

    subtitle_content = []
    for subtitle_url in subtitle_urls:
        res = (await session.get(subtitle_url)).json()
        for i in res["body"]:
            subtitle_content.append(i["content"])
    subtitle = "\n".join(subtitle_content)
    return subtitle


async def get_video_summary_by_ai(aid, cid) -> str:
    subtitle = await get_subtitle(aid, cid)
    if subtitle:
        res = chat("", "#有如下一个视频，请用中文完整的总结:\n" + subtitle)
        return res
    else:
        return ""


async def gen_image(video_info: dict) -> BytesIO:
    base_path = Path(__file__).parent
    # save_path = base_path / f"test.png"
    save_path = tempfile.mktemp(suffix=".png")
    image = Image.new("RGBA", (560, 470 + 15), (255, 255, 255, 255))
    # image.paste((220, 220, 220), (0, 480, 530, 620))
    cover = Image.open(BytesIO(
        (await session.get(video_info["cover_url"])).content)).resize((560, 315), Image.LANCZOS)
    cover_size = (0, 0, 560, 315)

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
    font = get_font()
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
    # 添加标题
    font = get_font(32)
    line_width = 16
    title = video_info["title"]
    max_title_len = line_width * 3 - 5
    if len(title) > max_title_len:
        title = title[:max_title_len] + "..."

    next_height = cover.height + 10
    for i, line in enumerate(split_lines(title, line_width)):
        next_height = cover.height + 10 + i * 40
        text_draw.text((20, next_height), f"{line}", font=font,
                       fill=(0, 0, 0))

    font = get_font(25)
    # 作者信息
    text_draw.text((20, cover.height + 140), f"UP: {video_info['owner']}", font=font, fill=(0, 0, 0))
    # 添加视频上传时间
    text_draw.text((340, cover.height + 140), f" {video_info['upload_time']}", font=font, fill=(0, 0, 0))
    temp_img = BytesIO()
    image.save(temp_img, format='PNG')
    return temp_img


def get_font(size=20):
    font = ImageFont.truetype(str(Path(__file__).parent.parent.parent / "common/fonts/仓耳舒圆体.ttf"), size)
    return font


if __name__ == "__main__":
    _text = "https://www.bilibili.com/video/BV1814y1V7RS/?spm_id_from=333.1073.channel.secondary_floor_video.click"
    _text = "https://www.bilibili.com/video/BV1Ps4y1v79v/?spm_id_from=444.41.list.card_archive.click&vd_source=210c4e2f9f0cdc36cd087b10ec64eedc"
    _text = "https://www.bilibili.com/video/BV1Ss4y1b7r9/?spm_id_from=333.1007.partition_recommend.content.click"

    # 白色背景封面
    _text = "https://www.bilibili.com/video/BV1sP411g7PZ/?spm_id_from=333.337.search-card.all.click&vd_source=210c4e2f9f0cdc36cd087b10ec64eedc"

    # _text = "https://www.bilibili.com/video/BV1MY4y1R7EN"

    # 长标题
    _text = "https://www.bilibili.com/video/BV17N411D7fB"

    # 长字幕
    # _text = 'https://www.bilibili.com/video/BV1MY4y1R7EN'

    # 被翻译成英文了
    # _text = 'https://bilibili.com/video/BV1Ds4y1e7ZB'
    bvid = get_bv_id(_text)
    # print(gen_text(bvid))
    _video_info = get_video_info(bvid)
    print(gen_image(_video_info))
    _r = get_video_summary_by_ai(_video_info["aid"], _video_info["cid"])
    # print(_r)
    # print(b32_to_bv("LPrGvRX"))
