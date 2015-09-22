# -*- encoding:UTF8 -*-

import json
import httpclient
http = httpclient.Http()

class Translator:

    def __call__(slef,content,ttype="en"):
        """
        tttype: 要翻译成的语种,zh 中文，jp 日文，fra 法文，kor 韩文, en 英文
        """

        content = content.encode("u8")
        detect_url = "http://fanyi.baidu.com/langdetect"
        data = {"query":content}
        res = http.connect(detect_url,data)
        res = json.loads(res)
        src_lan = res["lan"]

        if src_lan == ttype:
            return u"你傻啊！都是相同语言，你翻译个毛线！"

        trans_url = "http://fanyi.baidu.com/v2transapi"
        data = {"from": src_lan, "to": ttype, "query": content, "transtype": "realtime"}
        res = http.connect(trans_url,data)
        res = json.loads(res)
#        print res
        result = res["trans_result"]["data"][0]["dst"]

        return u"---原文---\n%s\n---译文---\n%s"%(content.decode("u8"),result)
