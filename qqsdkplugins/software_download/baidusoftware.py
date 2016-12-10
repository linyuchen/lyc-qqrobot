# -*- encoding:UTF8 -*-

import httpclient
import re
http = httpclient.Http()


class Software:

    def __init__(self):
        pass

    @staticmethod
    def windows(softname):

        softname = softname.encode("u8")
        softname = http.quote(softname)
        host = "http://rj.baidu.com"
        error = u"没有找到 %s 相关的软件" % softname
        url = host + "/search/index/?kw=" + softname
        html = http.connect(url)
        softkind = http.get_tag_html(html, "p", {"class": "softKind"})[0]
        soft_count = re.findall(u"到 (\d+) 款", softkind)[0]
        if soft_count == "0":
            return error

        soft_url = re.findall("/soft/detail/\d+\.html", html)[0]
        soft_url = host + soft_url
        html = http.connect(soft_url)

        soft_info_html = http.get_tag_html(html, "div", {"class": "info"})[0]
        soft_info_html = http.remove_tag(soft_info_html, "span", {"class": "real_score"})
        soft_info = http.html2txt(soft_info_html)

        soft_message = http.get_tag_html(html, "p", {"class": "message"})
        soft_message1 = u"\n\n功能简介：\n" + http.html2txt(soft_message[0])
        soft_message2 = u"\n\n更新内容：\n" + http.html2txt(soft_message[1])

        down_url = http.get_tag_attrs(html, "a", {"class": "fast_download"})[0]["bddlurl"]
        down_url = u"\n\n下载地址：" + down_url + "\n\n%s" % (u"原文：%s" % soft_url)

        return soft_info + soft_message1 + soft_message2 + down_url

    @staticmethod
    def android(soft):

        url = "http://m.baidu.com/s?st=10a001&tn=webmkt&pre=web_am_item&word=" + http.quote(soft.encode("gbk"))
        html = http.connect(url, encoding="gbk")
        http.file_open("test.html", "w", html.encode("u8"))
        if u"抱歉,没有找到" in html:
            error = u"抱歉,没有找到“%s”相关的安卓应用。" % soft
            return error
        url = http.get_tag_attrs(html, "a", {"class": "list-a"})[0]["href"]
        html = http.connect(url)
        soft_name = http.get_tag_html(html, "h1", {"class": "app-name"})[0]
        soft_name = http.html2txt(soft_name)

        soft_info_html = http.get_tag_html(html, "div", {"class": "intro-top"})[0]
        soft_info_html = http.remove_tag(soft_info_html, "div", {"class": "origin-wrap"})
        feature = http.get_tag_html(soft_info_html, "div", {"class": "app-feature"})[0]
        feature = http.html2txt(feature)

        detail_html = http.get_tag_html(soft_info_html, "div", {"class": "detail"})[0]
        detail = http.html2txt(detail_html)

        soft_info = feature + "\n" + detail

        soft_desc = http.get_tag_html(html, "div", {"class": "brief-long"})[0]
        soft_desc = http.remove_tag(soft_desc, "a", {"href": "javascript:;"})
        soft_desc = http.html2txt(soft_desc)

        download_url = http.get_tag_attrs(html, "a", {"class": "apk"})[0]["href"]

        result = soft_name + "\n\n" + soft_info + "\n\n" + soft_desc + u"\n下载地址：" + download_url + u"\n\n原文：" + url

        return result
