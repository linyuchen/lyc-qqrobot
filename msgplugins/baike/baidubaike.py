# -*- encoding:utf8 -*-

import re
import requests
from msgplugins.htmlhelper import HtmlHelper

html_helper = HtmlHelper()


class Baike:

    @staticmethod
    def get_para(html):

        content = ""
        result = html_helper.get_tag_html(html, "div", {"class": "para"})
        for i in result:
            content += i + "<br/>"
        content = html_helper.html2txt(content)
        return content[:400] + "..."

    def __call__(self, word):

        url = "https://baike.baidu.com/search/word?word=%s&pic=1&sug=1" % html_helper.quote(word)
        html = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        html.encoding = "utf8"
        html = html.text
        if "百度百科尚未收录词条" in html or "这是一个多义词，请在下列义项中选择浏览" in html_helper.html2txt(html):

            url = "http://baike.baidu.com/search/word?word=%s&pic=2&sug=1&enc=gbk" % html_helper.quote(
                word.encode("gbk"))
            html = requests.get(url, encoding="u8").text
            error = "抱歉，没有找到与“%s”相关的百科结果。" % word
            url = "http://baike.baidu.com"
            # 新的链接提取方式
            url = re.findall("class=\"result-title\" href=\"(.*?)\" target=", html)
            if not url:
                return error
            else:
                url = url[0]
            if "#" in url:
                _id = re.findall("/view/(\d+)\.htm\#sub(\d+)", url)
                url = "http://baike.baidu.com/subview/%s/%s.htm" % (_id[0][0], _id[0][1])
            html = requests.get(url, remove_charentity=False)
        title = re.findall("<title>(.*?)</title>", html)[0]
        if "card-summary-content" in html:
            result = html_helper.get_tag_html(html, "div", {"class": "card-summary-content"})
            #            print result
            content = html_helper.html2txt(result[0])
            if not content.strip():
                content = self.get_para(html)

        else:
            content = self.get_para(html)
        result = html_helper.html2txt(content)
        return title + "\n\n" + result + "\n\n原文：%s\n以上数据来源于百度百科" % url


if __name__ == "__main__":
    test = Baike()
    print(test("崩坏3"))
