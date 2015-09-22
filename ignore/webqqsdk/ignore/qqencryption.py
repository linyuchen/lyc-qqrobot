#encoding:UTF8

import urllib2
import urllib

host = "http://localhost/"

def encryptPassword(pwd, x , v):
#    print pwd, x, v
    url = host + "?pwd=%s&x=%s&v=%s"%(urllib.quote(pwd), urllib.quote(x), v)
#    print url
    return urllib2.urlopen(url).read()


if "__main__" == __name__:

    print getEncryption("#lyc66132956", "\x00\x00\x00\x00\x66\x0a\xd1\x4c", "mnhe")


