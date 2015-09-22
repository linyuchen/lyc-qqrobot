# -*- encoding:UTF8 -*-

import re
if __name__ == "__main__":
    import sys
    sys.path.append("..")
import httpclient
http = httpclient.Http()
class Digital:
    def __call__(sefl,mobile_name):

        error_info = u"抱歉，没有找到与"

        search_url = "http://detail.zol.com.cn/index.php?c=SearchList&keyword=" + http.quote(mobile_name.encode("gbk"))
    #    print search_url
        search_result_html = http.connect(search_url,encoding="gbk", timeout = 30)
        if error_info in search_result_html:
            return u"%s %s 相关的数码产品信息"%(error_info,mobile_name)
        else:
           parttern = u"<a href=\"([^>]*?)\" target=\"_blank\">更多参数>></a>.*?<b class=\"price-type\">(.+?)</b>"
    #       print search_result_html
           zol_url = "http://detail.zol.com.cn"
           result = re.findall(parttern,search_result_html,re.S)
           url = zol_url + result[0][0]
#           print url
           price = u"\n价格：" + result[0][1]
    #       price = u"\n价格：" + re.findall("<b class=\"price-type\">(.+?)</b>",search_result_html)[0]

    #       print url
           html_text = http.connect(url,encoding="gbk", timeout=30)
           title = re.findall("h1 class=\"ptitle\">(.+?)</h1>",html_text)[0]
           """
           html_text = http.get_substring("<ul class=\"main_param_list\">","</ul>\n",html_text)
           html_text = re.sub("<a href=.*?>","",html_text).replace("</a>","")
           result = title +  u"及报价：" + price + "\n"
           for i in re.findall("<li>(.+?)</li>",html_text):
               result += i + "\n"
            """

           result = title +  u"及报价：" + price + "\n"
#           txt = http.get_tag_html(html_text,"dd",{"id":"mParam"})
           txt = http.get_tag_html(html_text,"div",{"id":"newTb"})
           if not txt:
               return error_info
           txt = http.remove_tag(txt[0],"ul",{"id":"paramNavList"})
           result += http.html2txt(txt)
#           print result
#           result = http.get_substring(None,u"服务与支持",result)
           result = result.replace(u"纠错","")

           return result + u"\n\nps：以上数据来源于中关村"

if __name__ == "__main__":

    test = Digital()
    print test(u"红米NOTE")
