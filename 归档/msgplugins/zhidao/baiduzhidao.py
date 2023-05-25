# -*- encoding:utf8 -*-
import re
import httpclient

http = httpclient.Http()


class ZhiDao:

    def __init__(self):

        self.bdknow_question_url_list = []
        self.bdknow_search_word = ""
        self.bdknow_pn = 0

        self.lyrics_list = []

    def getNextQuestions(self):

        if self.bdknow_search_word:
            self.bdknow_pn += 10        
            return self.getQuestions(self.bdknow_search_word, pn=self.bdknow_pn)
        else:
            return u"请先搜索问题"
    
    def getQuestions(self, word, pn=0, date=0):
        
        self.bdknow_pn = pn

        self.bdknow_search_word = word
        url = "http://zhidao.baidu.com/search?lm=0&date=%d&rn=10&pn=%d&fr=search&ie=gbk&word=%s" % \
              (date, pn, http.quote(word.encode("gbk")))
        html = http.connect(url,encoding="gbk")  # 知道答案列表页面
        error = u"抱歉，暂时没有找到"
        if error in http.html2txt(html):
            return error + u"您搜索的问题"
        html = re.findall("<div class=\"list\s?(.*)",html,re.S)[0]
        url_list = re.findall("<a href=\"([^>]*?)\"[^>]*?>(.*?)</a>",html,re.S)#提取答案链接
        self.bdknow_question_url_list = []
        question_title_list = ""
        title_index = 1
        url_index = 1

        for i in range(len(url_list)):
            info = url_list[i]
            if info[0].startswith("http://zhidao.baidu.com/question/"):
                """
                偶数是问题
                奇数是答案
                """
                if (url_index%2):
                    title = u"%d：" % title_index + http.html2txt(info[1]) 
                    self.bdknow_question_url_list.append(info[0])
                    question_title_list += title
                    title_index += 1
                else:
                    question_title_list += u"（" + http.html2txt(info[1]) + u"）\n"

                url_index += 1

        if not self.bdknow_question_url_list:
            
            return self.getNextQuestions()

        else:
            return question_title_list

    def getAnswer(self, index):

        index = index.strip()
        if not index.isdigit():
            return u"序号命令错误"

        if not self.bdknow_question_url_list:
            return u"请先搜索问题"

        url = self.bdknow_question_url_list[int(index) - 1]
        html = http.connect(url,encoding="gbk")
        result = u"\n-----答案-----\n"

        title = u"问题："
#        title += re.findall("<span class=\"ask-title\">(.*?)</span>",html)[0]
        title += http.html2txt(http.get_tag_html(html,"span",{"class": "ask-title"})[0])

        best_answer = http.get_substring("<pre id=\"best-content", "</pre>", html,
                                         contain_start=True, contain_end=True)
        recommend_answer = http.get_substring("<pre id=\"recommend-content","</pre>", html, contain_start=True, contain_end=True)
        """
        answer = re.findall("<div class=\"line content\">(.+?)</div>",html)
        print answer

        for i in answer:
            result += http.html2txt(i) + "\n\n"
        """ 
        if best_answer:
            result += http.html2txt(best_answer)
        elif recommend_answer:
            result += http.html2txt(recommend_answer)
        else:
            other_answer_list = re.findall("<pre id=\"answer-content[^>]*?>([^<]*?)</pre>",html)
    #        print other_answer_list
            for i in range(len(other_answer_list)):
                result += u"答案%d：" % (i+1) + http.html2txt(other_answer_list[i]) + "\n\n"
        
        return title + "\n\n" + result + u"\n原文：%s\nps：以上数据来源于百度知道" % url


if __name__ == "__main__":

    test = ZhiDao()
    print test.getQuestions(u"吃不胖")
    print test.getNextQuestions()
    print test.getAnswer("1")
