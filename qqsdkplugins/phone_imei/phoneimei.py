# -*- encoding:UTF8 -*-
import httpclient
http = httpclient.Http()


class PhoneImei:

    def __init__(self):
        pass

    def __call__(self, imei):

        url = "http://www.opda.com/test.html"
        post_data = {"ImeiForm[imei]": imei}
        html = http.connect(url, post_data, encoding="u8")
        not_find = u"未找到相关机型数据"
        if u"串号无效" in html:
            error = u"您输入的imei串号无效, 请确保正确输入, 如果输入一致该款机器有可能是山寨无码机!"
            return error
        elif not_find in html:
            return not_find
        
        result_html = http.get_tag_html(html, "table",{"class":"table table table-bordered"})[0]
        result = http.html2txt(result_html) + u"\n\n如果查询结果手机与实际不符，极有可能该型号为翻新机或者是高仿机"
        
        return result
