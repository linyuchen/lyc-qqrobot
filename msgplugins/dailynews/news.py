import requests
from common.utils import htmlhelper


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
    return news


if __name__ == '__main__':
    r = get_news()
    print(r)
    # print(verse)
