import re
import textwrap
import unicodedata
from pathlib import PurePath

import requests
from common.utils import htmlhelper
from PIL import Image, ImageDraw, ImageFont


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
            if current_line_width >= 15:
                wrap_news.append("".join(current_line))
                current_line = []
                current_line_width = 0
        if current_line:
            wrap_news.append("".join(current_line))

    image = Image.new("RGB", (700, 41 * len(wrap_news)), (255, 255, 255))
    text_draw = ImageDraw.Draw(image)
    base_path = PurePath(__file__).parent
    font = ImageFont.truetype(str(base_path / "银河甜心&宇宙怪兽.ttf"), 40)
    for i, line in enumerate(wrap_news):
        text_draw.text((50, (i + 1) * 40), line, font=font, fill=(0, 0, 0), spacing=10)
    image.save(str(base_path / "news.png"))
    return news


if __name__ == '__main__':
    r = get_news()
    print(r)
    # print(verse)
