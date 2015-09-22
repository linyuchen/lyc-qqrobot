# -*- encoding:UTF8 -*-
import os
import urllib2
import time
import re

class HistoryToday:

    def __init__(self):

        self.path = os.path.dirname(__file__) or "."
        self.path += "/history_today/"
        self.ext = ".txt"

    def __call__(self):

        url="http://www.todayonhistory.com/index.htm"
        today = time.strftime("%m-%d")
        path = self.path + today + self.ext
        if not os.path.exists(path):
            data = urllib2.urlopen(url).read().decode("u8", "ignore")
            #print data
        #    print data
        #    data.encode("gb2312")
            result=re.findall("<em>(.*?)</em> <i>(.*?)</i>",data)
        #    print result
            tmp="";
            for i in result:
        #        print i
                tmp+="\n"+i[0]+i[1]
            with open(path, "w") as fopen:
                fopen.write(tmp.encode("u8"))
        else:
            with open(path) as fopen:
                tmp = fopen.read().decode("u8")
        return tmp

if __name__ == "__main__":

    test = HistoryToday()
    print test()
