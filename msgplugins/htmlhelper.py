# coding=UTF-8
__doc__ = """
A convenient module for python 3 to handle html
@author: LinYuChen
@version:1.4
"""

import re
from urllib import parse
from typing import List


class HtmlHelper:

    @staticmethod
    def quote(content: str) -> str:
        return parse.quote(content)

    @staticmethod
    def unquote(content: str) -> str:
        return parse.unquote(content)

    @staticmethod
    def file_open(path, method='r', content=''):
        """
        open a file,read or write

        @param path:the file path
        @type path:string

        @param method:the open method
        @type method:'r',"rb","w","wb","a",if the method is r or rb,content could be None

        @param content:the content of the writing
        @type content:string

        """

        f = open(path, method)
        if method == 'r' or method == "rb":
            data = f.read()
            f.close()
            return data
        elif method == 'w' or method == 'a' or method == "wb":
            f.write(content)
        f.close()

    @staticmethod
    def get_substring(start_string: str, end_string: str, data: str, contain_start=False, contain_end=False) -> str:

        if not start_string:
            pos0 = 0
        else:
            pos0 = data.find(start_string)

            if -1 == pos0:
                return None

            if not contain_start:
                pos0 += len(start_string)

        data = data[pos0:]
        if not end_string:
            pos1 = len(data)
        else:
            pos1 = data.find(end_string)

        if -1 == pos1:
            return None

        if contain_end:
            pos1 += len(end_string)

        data = data[:pos1]

        return data

    @staticmethod
    def str2dic(s: str) -> dict:
        """
        convert post data string to a dict
        @param s:post data string
        @type:string

        @return:a dict of the converted post data string 
        @rtype dic:dict
        """
        dic = {}
        list0 = s.split("&")
        for i in list0:
            list2 = i.split("=")
            dic[list2[0]] = list2[1]
        return dic

    @staticmethod
    def get_form(data: str, tag="postfield", encoding="utf8") -> dict:
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
        param = {}
        field_list = re.findall(tag + ".*? name=\"(.*?)\".*?value=\"(.*?)\"", data)

        for i in field_list:
            param[i[0]] = i[1].encode(encoding)

        return param

    @staticmethod
    def remove_charentity(html: str):

        charentity_dict = {"&nbsp;": " ", "&lt;": "<", "&gt;": ">", "&amp;": "&", "&quot;": "\"",
                           "&apos;": "'", "&plusmn;": "+",
                           }

        for i in charentity_dict:
            try:
                html = html.replace(i, charentity_dict[i])
            except:
                pass

        #                print html

        def func(m):

            entity_ascii = int(m.group(1))
            #            print entity_ascii
            if entity_ascii < 256:
                return chr(entity_ascii)
            else:
                return ""

        html = re.sub("&#(\d+);", func, html)

        return html

    def change2charentity(self, s: str) -> str:

        s = s.replace("&", "&amp;")
        charentity_dict = {"'": "&apos;", "\"": "&quot;", u"\u0020": "&nbsp;", "<": "&lt;", ">": "&gt;",
                           "+": "&plusmn;"}
        for i in charentity_dict:
            s = s.replace(i, charentity_dict[i])

        return s

    def html2txt(self, html: str) -> str:
        """
        @param html: html string
        @type: string

        @return: The converted txt
        @rtype: string
        """

        html = re.sub("(\r\n)+", "", html)
        html = re.sub("\n+", "", html)
        html = re.sub("\t+?", "", html)
        html = re.sub(" +", " ", html)
        pattern = re.compile("<!--.*?-->", re.S)
        html = re.sub(pattern, "", html)  # remove the comment
        html = re.sub(u"<style[^>]*?>.*?</style>", "", html)  # remove the style

        pattern = re.compile(u"<script[^>]*?>.*?</script>", re.S)
        html = re.sub(pattern, "", html)  # remove the script

        # replace the <br/>
        html = re.sub(u"<br[^>]*?>", "\n", html)
        html = re.sub(u"<p[^>]*?>", "\n", html)
        html = re.sub(u"<h[^>]*?>", "\n", html)
        html = re.sub(u"<li[^>]*?>", "\n", html)
        #        html = re.sub(u"</li>","\n",html)

        html = re.sub(u"</div>", "\t", html)
        #       表格处理
        html = re.sub(u"</th>", "\t", html)
        html = re.sub(u"<tr[^>]*?>", "\n", html)
        #        html = re.sub(u"</tr>","\n",html)
        html = re.sub(u"</td>", "\t", html)

        html = re.sub(u"<[^>]*?>", "", html)  # remove the tag
        #        html = re.sub("</[^>]*?>","",html)# remove the end tag
        #        print html
        #        pattern = re.compile("<.*?/>",re.S)
        #        html = re.sub("<[^>]*?/>","",html)# remove the startend tag

        html = self.remove_charentity(html)

        return html

    def txt2html(self, txt: str) -> str:

        html = self.change2charentity(txt)
        html = html.replace("\n", "<br/>")

        return html

    def _get_tag_attrs(self, tag: str, tag_html: str) -> dict:

        tag_html = re.findall("<%s[^>]*?>" % tag, tag_html)[0]
        #        print tag_html
        attrs_list = re.findall("\s*(\S*)\s*=\s*[\"'](.*?)[\"']\s*", tag_html)  # get attributes
        #        print attrs_list
        _attrs = {}
        for key in attrs_list:
            _attrs[key[0]] = key[1]

        return _attrs

    def get_start_tag(self, html, tag, attrs={}) -> List[str]:

        result = re.findall("<%s[^>]*?>" % tag, html)
        #        print result
        start_tag_list = []
        for i in result:

            _attrs = self._get_tag_attrs(tag, i)

            # print _attrs
            is_attrs = True
            for key in attrs:
                #                if not _attrs.has_key(key) or attrs[key] != _attrs[key]:
                if key not in _attrs or not re.findall(attrs[key], _attrs[key]):
                    is_attrs = False

            #            print _attrs
            if not attrs:
                is_attrs = True

            if is_attrs:
                start_tag_list.append(i)

        return start_tag_list

    def get_tag_html(self, html: str, tag: str, attrs={}) -> str:
        """
        @param html: html string
        @type: str

        @param tag
        @type: str

        @param attrs: {"attribute name": "attribute value"}, value support regular
        """

        start_tag = self.get_start_tag(html, tag, attrs)
        #        print start_tag
        result_list = []
        end_tag = "</%s>" % tag

        def get_end_tag_pos(start_pos, end_pos):

            #            print html[start_pos:end_pos]
            tag_count = html[start_pos + 1:end_pos].count("<" + tag)
            #            print tag_count
            #            print end_pos
            start_pos = end_pos
            if not tag_count:
                return end_pos
            for i in range(tag_count):
                p = html.find(end_tag, end_pos + 1)
                if p != -1:
                    end_pos = p
            #                print html[end_pos + 1:]
            #                print end_pos
            return get_end_tag_pos(start_pos, end_pos)

        start_tag_pos = -1
        for i in start_tag:
            start_tag_pos = html.find(i, start_tag_pos + 1)
            #            print start_tag_pos

            """ <div class="wgt-best "> <div class="class"> <div>div</div></div><div>div2</div> </div>"""
            # print repr(sub_html)
            end_tag_pos = html.find(end_tag, start_tag_pos + 1)
            #            print end_tag_pos
            end_pos = get_end_tag_pos(start_tag_pos, end_tag_pos)

            #            print start_tag_pos,end_pos,end_tag_pos

            #            print html[:end_pos + len(end_tag)]

            result_list.append(html[start_tag_pos:end_pos + len(end_tag)])

        return result_list

    def get_tag_attrs(self, html: str, tag: str, attrs={}) -> List[dict]:
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

        tag_html_list = self.get_tag_html(html, tag, attrs)
        _attrs = []

        for i in tag_html_list:
            _attrs.append(self._get_tag_attrs(tag, i))

        return _attrs

    def remove_tag(self, html: str, tag: str, attrs={}):

        tag_html_list = self.get_tag_html(html, tag, attrs)

        result_html = html
        for i in tag_html_list:
            result_html = result_html.replace(i, "")

        return result_html


if "__main__" == __name__:

    import time

    http = HtmlHelper()
#    html = open("html.html").read().decode("gbk")
#    result = http.get_tag_html(html,"a",{"href":"htm_data/.+"})
#    print(html[5:317])
#    print result
