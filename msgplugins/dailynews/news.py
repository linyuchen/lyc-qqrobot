import os.path
import re
import textwrap
import time

import unicodedata
from pathlib import PurePath

import requests
from common.utils import htmlhelper
from PIL import Image, ImageDraw, ImageFont

base_path = PurePath(__file__).parent


def get_news():
    # 从知乎每日新闻接口获取新闻内容
    url = 'https://www.zhihu.com/api/v4/columns/c_1261258401923026944/items'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.106 Safari/537.36"}
    response = requests.get(url, headers=headers)
    res = response.json()
    content = res['data'][0]['content']
    content = htmlhelper.remove_tag(content, 'a')

    news = htmlhelper.html2txt(content).strip()
    lines = news.split('\n')
    news = '\n'.join(lines[:2]) + '\n\n' + '\n\n'.join(lines[2:])
    # news = re.sub(r'(\d+)', r' \1 ', news)
    # news = news.translate(str.maketrans("0123456789", "０１２３４５６７８９"))
    # news = textwrap.wrap(text=news, width=30)
    # line_count = len(news)
    # news = "\n".join(news)
    # 创建 TextWrapper 对象

    # wrapper = textwrap.TextWrapper(width=lambda c: char_width(c) * 0.5)
    # wrapper = textwrap.TextWrapper(width=20, expand_tabs=False, replace_whitespace=False, drop_whitespace=False,
    #                                break_long_words=True, break_on_hyphens=False)

    # 设置数字和英文字母的宽度为 0.5
    # wrapper.width = 15
    # wrapper.place_holder_width = 0.5

    # 进行文本换行
    line_width = 30
    wrap_news = []
    for line in news.splitlines():
        if line == "":
            wrap_news.append("")
            continue
        current_line_width = 0
        current_line = []
        for c in line:
            # todo: 这里标点符号被算做了半角字符，导致换行不准确
            # 标点符号算作全角字符
            if not re.match("[\da-zA-Z]", c):
            # if unicodedata.east_asian_width(c) in ('F', 'W'):
                # 全角字符
                current_line_width += 1
            else:
                # 半角字符
                current_line_width += 0.4
            current_line.append(c)
            if current_line_width >= line_width:
                wrap_news.append("".join(current_line))
                current_line = []
                current_line_width = 0
        if current_line:
            wrap_news.append("".join(current_line))

    line_height = 60
    image = Image.new("RGB", (1080, (line_height + 1) * len(wrap_news)), (255, 255, 255))
    text_draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(base_path / "仓耳今楷01-9128-W05.otf"), 30)
    for i, line in enumerate(wrap_news):
        text_draw.text((50, (i + 1) * line_height), line, font=font, fill=(0, 0, 0), spacing=10)
    image.save(str(base_path / "news.png"))
    return news


def get_news2():
    today = time.strftime("%Y-%m-%d")
    yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24 * 60 * 60))
    today_img_path = base_path / "data" / (today + ".png")
    yesterday_img_path = base_path / "data" / (yesterday + ".png")

    if os.path.exists(today_img_path):
        # 对比昨天的图片，如果一样就不更新
        if os.path.exists(yesterday_img_path) and os.path.getsize(yesterday_img_path) == os.path.getsize(today_img_path):
            os.remove(today_img_path)
        else:
            return str(today_img_path)
    url = "https://api.03c3.cn/zb/"
    with open(today_img_path, "wb") as f:
        try:
            img_data = requests.get(url).content
            f.write(img_data)
            return str(today_img_path)
        except:
            return


if __name__ == '__main__':
    print(get_news2())
