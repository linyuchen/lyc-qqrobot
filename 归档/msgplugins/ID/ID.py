# -*- encoding:UTF8 -*-

import httpclient
http = httpclient.Http()

class ID:

    def __call__(self,id):
        url = "http://tools.2345.com/shenfenzheng.htm?card=" + id

        url = "http://idquery.duapp.com/index.php"
        html = http.connect(url,{"in_id": id},encoding="gbk")
        html = http.get_tag_html(html,"div",{"id":"i"})
#        print html
        html = http.get_tag_html(html[0],"div",{"class":"b$"})
        html = "<br/>".join(html[1:])
#        print html
        text = http.html2txt(html)
#        print text
        return text
#        print html


if __name__ == "__main__":
    test = ID()
    print test("410523199102286185")
