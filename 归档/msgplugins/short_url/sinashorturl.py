# -*- encoding:UTF8 -*-

import json
import urllib2


class ShortUrl:
    
    def __init__(self):

        self.appkey = "5786724301"

    def make(self, long_url):

        url = "http://api.weibo.com/2/short_url/shorten.json?source=%s&url_long=%s" % (self.appkey, long_url)
        result = urllib2.urlopen(url).read()
        if not result:
            return u"网址有误！"
        dic = json.loads(result)
        if "error" in dic:
            return dic["error"]

        return dic["urls"][0]["url_short"]

    def expand(self, short_url):

        url = "http://api.weibo.com/2/short_url/expand.json?source=%s&url_short=%s" % (self.appkey, short_url)
        result = urllib2.urlopen(url).read()
        if not result:
            return u"网址有误！"
        dic = json.loads(result)
        if "error" in dic:
            return dic["error"]

        return dic["urls"][0]["url_long"]


if "__main__" == __name__:

    test = ShortUrl()
    print test.make("http://0yuchen.com")
    print test.expand("http://t.cn/RwqaFqp")
