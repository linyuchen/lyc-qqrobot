# -*- encoding:utf8 -*-

import re
if __name__ == "__main__":
    import sys
    sys.path.append("..")
import httpclient
http = httpclient.Http()

class Baike:


    def get_para(self,html):

        content = ""
        result = http.get_tag_html(html,"div",{"class": "para"})
        for i in result:
            content += i + "<br/>"
        content = http.html2txt(content)
        return content[:400]  + "..."

    def __call__(self,word):

        url = "http://baike.baidu.com/search/word?word=%s&pic=1&sug=1"%http.quote(word.encode("u8"))
#        print url
        html = http.connect(url,encoding="u8")
#        print html
        if u"百科" not in html:
            html = http.connect(url,encoding="gbk")
#        print http.html2txt(html)
#        http.file_open("html.txt","w",html.encode("u8"))
        if u"百度百科尚未收录词条" in html or u"这是一个多义词，请在下列义项中选择浏览" in http.html2txt(html):

            url = "http://baike.baidu.com/search/word?word=%s&pic=2&sug=1&enc=gbk"%http.quote(word.encode("gbk"))
    #        print url
            html = http.connect(url,encoding="u8")
#            print http.html2txt(html)
            error = u"抱歉，没有找到与“%s”相关的百科结果。"%word
#            if error in http.html2txt(html):
#                return u"未找到%s相关百科结果"%word
#            http.file_open("b.html", "w", html.encode("u8"))
            url = "http://baike.baidu.com"
#            url = re.findall("<h2>\s+<a href=\"(.*?)\" target=",html)[0]
            # 新的链接提取方式
            url = re.findall("class=\"result-title\" href=\"(.*?)\" target=",html)
            if not url:
                return error
            else:
                url = url[0]
#            print url
            if "#" in url:
                id = re.findall("/view/(\d+)\.htm\#sub(\d+)",url)
                url = "http://baike.baidu.com/subview/%s/%s.htm"%(id[0][0],id[0][1])
            html = http.connect(url, remove_charentity=False)
        #    http.file_open("html.txt","w",html.encode("u8"))
        #    print html
    #    print result
#        print html
        title = re.findall("<title>(.*?)</title>",html)[0]
#        print title[0]
#        content = title + "<br/><br/>"
        if "card-summary-content" in html:
            result = http.get_tag_html(html,"div",{"class": "card-summary-content"})
#            print result
            content = http.html2txt(result[0])
            if not content.strip():
#                print "blank"
                content = self.get_para(html)

        else:
            content = self.get_para(html) 
        result = http.html2txt(content)
        return title + "\n\n" + result + u"\n\n原文：%s\nps：以上数据来源于百度百科"%url


if __name__ == "__main__":

    test = Baike()
    print test(u"再别康桥")
