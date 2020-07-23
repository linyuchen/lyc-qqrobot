# -*- encoding:UTF8 -*-

import httpclient
http = httpclient.Http()


class PhoneNumber:

    def __init__(self):
        pass

    def __call__(self, phone_number):

        url = "http://tools.2345.com/shouji/" + phone_number
        html = http.connect(url, encoding="gbk")
        html = http.get_tag_html(html, "div", {"class": "mod_search_think mt40"})
        if not html:
            error = u"手机号码有误!"
            return error
        html = http.html2txt(html[0]).replace(u"（查吉凶）","")
        return html

if __name__ == "__main__":
    print(PhoneNumber()("13088108191"))
