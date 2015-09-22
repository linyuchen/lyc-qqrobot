# coding=UTF8

import PyV8
import os
import sys


class Navigator(PyV8.JSClass):

    def __init__(self):

        self.appName = "Netscape"
        self.appVersion = 5


class Window(PyV8.JSClass):

    def __init__(self):
        self.window = self
        self.navigator = Navigator()


ctxt = PyV8.JSContext(Window())
ctxt.enter()
curPath = os.path.dirname(__file__)
curPath = curPath if curPath else "."
js = open(curPath + "/encrypt.js").read().decode("u8", "ignore")
ctxt.eval(js)


def getEncryption(pwd, v, uin):
    uin = uin.decode("hex")
    js = "Encryption.getEncryption('%s',%s,'%s')" % (pwd, uin, v)
#    print repr(js)
    return ctxt.eval(js)


def get_hash(qq, ptwebqq):
    js = "Encryption.get_hash('%s', '%s')" % (qq, ptwebqq)
    return ctxt.eval(js)


cmd_type = sys.argv[1]
if cmd_type == "encrypt_pwd":
    pwd = sys.argv[2]
    uin = sys.argv[3]
    v = sys.argv[4]
    print getEncryption(pwd, uin, v)
elif cmd_type == "hash":
    qq = sys.argv[2]
    ptwebqq = sys.argv[3]
    print get_hash(qq, ptwebqq)
    
#    u = r"'\x00\x00\x00\x00f\n\xd1L'"


