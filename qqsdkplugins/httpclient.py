#coding=UTF-8
__doc__ = """
A convenient module for python 2.7 to operate http protocol and handle html
@author: LinYuChen
@contact:http://0yuchen.com
@version:1.3
"""

import urllib2
import cookielib
import urllib
import re
import traceback


class Http:
    
    def __init__(self,open_cookie = True,cookie_path="",proxy={}):

        self.open_cookie = open_cookie
        self.cookie_path = cookie_path
#        """
        if open_cookie:
            self.cookieJar = cookielib.LWPCookieJar()
            if cookie_path:
                try:
                    self.cookieJar.load(cookie_path)
                except:
                    pass
            #else:
            #    self.cookieJar = cookielib.CookieJar()
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
            urllib2.install_opener(self.opener)
#        """
        
        self.web_headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8",
                 }
        
        self.wap_headers = {'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'}

        self.headers = self.web_headers
        self.res = None
        self.res_url = ""
        self.res_headers = ""
        self.res_content = ""
        self.res_cookies = ""
        self.timeout = 0
        self.try_again = 0

    def set_tryagain(self,count):

        self.try_again = count

    def get_resheader(self):

        return self.res_headers

    def get_rescookies(self):

        return self.res_cookies

    def set_timeout(self,timeout):

        self.timeout = timeout

    def set_wap_header(self):

        self.headers = self.wap_headers
    
    def set_web_header(self):

        self.headers = self.web_headers

    def add_header(self,key,value):

        self.headers[key] = value

    def set_proxy(self,proxy_dict):

#        {'http':'http://user:passwd@172.16.9.11:8088'}
        proxy_support = urllib2.ProxyHandler(proxy_dict)
        self.opener.add_handler(proxy_support)
        

    def connect(self,url,post_data="",encoding="UTF-8",timeout=0,remove_charentity=True,try_again=1):
        """

        @type url:string
        
        @param post_data:the post data,if post_data is None,the request method is get
        @type post_data:dict or string
        
        @param encoding:the html text encoding

        @return:response html text
        @rtype self.res_content
        """

        
        if isinstance(post_data,dict):
            post_data = urllib.urlencode(post_data)

#        elif post_data:
#            post_data= self.str2dic(post_data)
#            post_data= urllib.urlencode(post_data)

        """
        if self.open_cookie:
            try:
                cookie=self.file_open(self.cookie_path)
                if cookie:
                    self.headers["Cookie"]=cookie
            except Exception,e:
                print e
        """
        if post_data:
            req = urllib2.Request(url,post_data,headers = self.headers)

        else:
            req = urllib2.Request(url,headers = self.headers)

        if self.try_again:
            try_again = self.try_again
        
        for i in range(try_again):
            try:
                if timeout:
                    res = urllib2.urlopen(req,timeout=timeout)
                elif self.timeout:
                    res = urllib2.urlopen(req,timeout=self.timeout)
                else:
                    res = urllib2.urlopen(req)

                self.res_headers = res.headers
                self.res_url = res.geturl()
                self.res_content = res.read()
                break
            except Exception,e:
                err = u"%s:%s\nurl:%s \n"%(__name__,str(e),url)
                if post_data:
                    err += "post data: %s\n"%str(post_data)
                print err
                if i == (try_again - 1):
                    return ""
    #        print dir(res)
        if remove_charentity:
            self.res_content = self.remove_charentity(self.res_content)

        if encoding:
            self.res_content = self.res_content.decode(encoding,"ignore")
            data = repr(self.res_content)
            data = data.replace("\\xa0"," ")
            self.res_content = eval(data)
#            self.res_content = self.res_content.decode(encoding)

        self.res = res
        self.res_cookies = self.res_headers.getheader("Set-Cookie")

        if self.open_cookie and self.cookie_path:
#            print cookie
            self.cookieJar.save(self.cookie_path)
            
        return self.res_content


    def file_open(self,path, method = 'r', content = ''):
        """
        open a file,read or write

        @param path:the file path
        @type path:string

        @param method:the open method
        @type method:'r',"rb","w","wb","a",if the method is r or rb,content could be None

        @param content:the content of the writing
        @type content:string

        """

        f = open(path,method)
        if method == 'r' or method =="rb": 
            data = f.read()
            f.close()
            return data
        elif  method == 'w' or method == 'a' or method == "wb": 
            f.write(content)
        f.close()

    def get_substring(self,start_string,end_string,data,contain_startstring=False,contain_endstring=False):

        if not start_string:
            pos0 = 0
        else:
            pos0=data.find(start_string)

            if -1 == pos0:
                return None

            if not contain_startstring:
                pos0 += len(start_string)

        data=data[pos0:]
        if not end_string:
            pos1 = len(data)
        else:
            pos1=data.find(end_string)

        if -1 == pos1:
            return None

        if contain_endstring:
            pos1 += len(end_string)

        data=data[:pos1]

        return data

    def str2dic(self,string):
        """
        convert post data string to a dict
        @param string:post data string
        @type:string

        @return:a dict of the converted post data string 
        @rtype dic:dict
        """
        dic={}
        list0=string.split("&")
        for i in list0:
            list2=i.split("=")
            dic[list2[0]]=list2[1]
        return dic
    
    def quote(self,content):

        return urllib.quote(content)

    def unquote(self,content):

        return urllib.unquote(content)


    def get_form(self,data,tag="postfield",encoding="utf8"):
        """
        get the form from data

        @param data:the html text
        @type data:string

        @param tag:the post tag of form,for example：<input name = "id"...> the tag is input
        @type tag:string

        @param encoding:post data encoding
        @type:string

        @return:post data
        @rtype param:
        """
        param={}
        field_list=re.findall(tag + ".*? name=\"(.*?)\".*?value=\"(.*?)\"",data)

        for i in field_list:
            param[i[0]]=i[1].encode(encoding) 

        return param

    
    def remove_charentity(self,html):

        charentity_dict = {"&nbsp;": " ", "&lt;": "<","&gt;": ">", "&amp;": "&", "&quot;": "\"",
                "&apos;": "'", "&plusmn;": "+", 
                }

        for i in charentity_dict:
            try:
                html = html.replace(i,charentity_dict[i])
            except:
#                print html
                print i
        
        def func(m):

            entity_ascii = int(m.group(1))
#            print entity_ascii
            if entity_ascii < 256:
                return chr(entity_ascii)
            else:
                return ""

        html = re.sub("&#(\d+);",func,html)

        return html

    def change2charentity(self,string):

        string = string.replace("&","&amp;")
        charentity_dict = {"'":"&apos;", "\"":"&quot;", u"\u0020":"&nbsp;", "<":"&lt;", ">":"&gt;","+": "&plusmn;"}
        for i in charentity_dict:
            string = string.replace(i,charentity_dict[i])

        return string

    def html2txt(self,html):
        """
        @param html: html string
        @type: string

        @return: The converted txt
        @rtype: string
        """
        
        html = re.sub("(\r\n)+","",html)
        html = re.sub("\n+","",html)
#        print html
        html = re.sub("\t+?","",html)
        html = re.sub(" +"," ",html)
#        html = re.sub("[\s^ ]+?","",html)
        pattern = re.compile("<!--.*?-->",re.S)
        html = re.sub(pattern,"",html)# remove the comment
#        pattern = re.compile("<style.*?>.*?</style>",re.S)
        html = re.sub(u"<style[^>]*?>.*?</style>","",html)# remove the style

        pattern = re.compile(u"<script[^>]*?>.*?</script>",re.S)
        html = re.sub(pattern,"",html)# remove the script

        #replace the <br/>
        html = re.sub(u"<br[^>]*?>","\n",html)
        html = re.sub(u"<p[^>]*?>","\n",html)
        html = re.sub(u"<h[^>]*?>","\n",html)
        html = re.sub(u"<li[^>]*?>","\n",html)
#        html = re.sub(u"</li>","\n",html)

        html = re.sub(u"</div>","\t",html)
#       表格处理        
        html = re.sub(u"</th>","\t",html)
        html = re.sub(u"<tr[^>]*?>","\n",html)
#        html = re.sub(u"</tr>","\n",html)
        html = re.sub(u"</td>","\t",html)

        html = re.sub(u"<[^>]*?>","",html)# remove the tag
#        html = re.sub("</[^>]*?>","",html)# remove the end tag
#        print html
#        pattern = re.compile("<.*?/>",re.S)
#        html = re.sub("<[^>]*?/>","",html)# remove the startend tag 

        html = self.remove_charentity(html)


        return html

    def txt2html(self,txt):

        html = self.change2charentity(txt)
        html = html.replace("\n","<br/>")

        return html

    def _get_tag_attrs(self,tag,tag_html):

        tag_html = re.findall("<%s[^>]*?>"%tag,tag_html)[0]
#        print tag_html
        attrs_list = re.findall("\s*(\S*)\s*=\s*[\"'](.*?)[\"']\s*",tag_html)#get attributes
#        print attrs_list
        _attrs = {}
        for key in attrs_list:
            _attrs[key[0]] = key[1]

        return _attrs

    def get_start_tag(self,html,tag,attrs={}):

        result = re.findall("<%s[^>]*?>"%tag,html)
#        print result
        start_tag_list = []
        for i in result:
             
            _attrs = self._get_tag_attrs(tag,i)

            #print _attrs
            is_attrs = True
            for key in attrs:
#                if not _attrs.has_key(key) or attrs[key] != _attrs[key]:
                if not _attrs.has_key(key) or not re.findall(attrs[key],_attrs[key]): 
                    is_attrs = False

#            print _attrs
            if not attrs:
                is_attrs = True

            if is_attrs:
                start_tag_list.append(i)

        return start_tag_list

    def get_tag_html(self,html,tag,attrs={}):
        """
        @param html: html string
        @type: str

        @tag
        @type: str

        @param attrs: {"attribute name": "attribute value"}, value support regular
        """

        start_tag = self.get_start_tag(html,tag,attrs)
#        print start_tag
        result_list = []
        end_tag = "</%s>"%tag

        def get_end_tag_pos(start_pos,end_pos):

#            print html[start_pos:end_pos]
            tag_count = html[start_pos + 1:end_pos].count("<"+tag)
#            print tag_count 
#            print end_pos
            start_pos = end_pos
            if not tag_count:
                return end_pos
            for i in range(tag_count):
                p = html.find(end_tag,end_pos + 1)
                if p != -1:
                    end_pos = p
#                print html[end_pos + 1:]
#                print end_pos
            return get_end_tag_pos(start_pos,end_pos)

        start_tag_pos = -1 
        for i in start_tag:
            start_tag_pos = html.find(i,start_tag_pos + 1)
#            print start_tag_pos
                
            """ <div class="wgt-best "> <div class="class"> <div>div</div></div><div>div2</div> </div>"""
            #print repr(sub_html)
            end_tag_pos = html.find(end_tag,start_tag_pos + 1)
#            print end_tag_pos
            end_pos = get_end_tag_pos(start_tag_pos,end_tag_pos)

#            print start_tag_pos,end_pos,end_tag_pos
            
#            print html[:end_pos + len(end_tag)]

            result_list.append(html[start_tag_pos:end_pos + len(end_tag)])

        return result_list

    def get_tag_attrs(self,html,tag,attrs={}):
        """
        @param html:html
        @type html:string

        @param tag: html tag
        @type tag: string

        @param attrs:attribute dic,{"class":"c"}
        @type attrs: dict
        
        @return: attrs
        @rtype: dict
        """
        
        tag_html_list = self.get_tag_html(html,tag,attrs)
        _attrs = []
        
        for i in tag_html_list:
            _attrs.append(self._get_tag_attrs(tag,i))

        return _attrs

    def remove_tag(self,html,tag,attrs={}):

        tag_html_list = self.get_tag_html(html,tag,attrs)
        
        result_html = html
        for i in tag_html_list:
            result_html = result_html.replace(i,"")

        return result_html
            

if "__main__" == __name__:

    import time
    http = Http()
    proxy = {"sock":"127.0.0.1:1080"}
    url = "http://localhost:80/?a=2"
#    print u"\xa0".replace(u"\xa0","")
    while 1:
        print http.connect(url,{"a":"a","b":"hello"})
#    html = open("html.html").read().decode("gbk")
#    result = http.get_tag_html(html,"a",{"href":"htm_data/.+"})
#    print html[5:317]
#    print result
