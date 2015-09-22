# -*- encoding:UTF8 -*-
import httpclient
http = httpclient.Http()

class Tools:
    def pairing(self,name):

        name = name.split()
        if len(name) < 2:
            return u"名字需要两个才能配对哦~"
        boy_name = name[0].encode("gbk")
#        print boy_name
        girl_name = name[1].encode("gbk")
#        print girl_name
        url = "http://www.8s8s.com/xx/xingming_peidui.php"
        post_data = {"boy": boy_name, "girl": girl_name, "Submit":u"姓名配对测试".encode("gbk")}
        res = http.connect(url,post_data,encoding="gbk")
#        print res
        result = http.get_tag_html(res,"div",{"class":"scenter_text"})
#        print result[0]
        result = http.html2txt(result[0])
        return result

    def test(self,name):

        submit = u'姓名测试命运'
        url = 'http://www.sheup.com/namechengfen.php'
        post_data = {'name':name.encode('gbk'), 'Submit':submit.encode('gbk')}
        html = http.connect(url,post_data,encoding="gbk")
        content = http.get_tag_html(html, 'div', {'class': "content_text"})[1]
        content = http.html2txt(content)
        return content
