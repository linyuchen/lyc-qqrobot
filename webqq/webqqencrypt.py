# coding = UTF-8

import os

cur_path = os.path.dirname(__file__) or "."
print cur_path

class Encrypt:


    def encryptPassword(self, password, verifycode, uin):

        cmd = "python " + cur_path + "/qqencryption2.py encrypt_pwd %s %s %s" % (password, verifycode, repr(uin).encode("hex"))
        # print cmd
        result = os.popen(cmd).read()
        return result.strip()
        
    
    def getHash(self, qq, ptwebqq):
        cmd = "python " + cur_path + "/qqencryption2.py hash %s %s" % (qq, ptwebqq)
#        print cmd
        result = os.popen(cmd).read()
        return result.strip()


    def get_gtk(self,skey):

        hash = 5381
        for i in range(len(skey)):
            hash += (hash << 5) + ord(skey[i])

        return hash & 2147483647


if "__main__" == __name__:

    test = Encrypt()
#    print test.get_gtk("@GqJ9ZOwn4")
#    print test.getHash("1234567","4132421351")
    uin = "\x00\x00\x00\x00f\n\xd1L"
    pwd = ""
    v = "1234"
#    print test.encryptPassword(pwd, v, uin)
    qq = "1711984972"
    ptwebqq = "23832d6fe2ed32aa57a9b034bc9852356217233f8888b44d"
    print test.getHash(qq, ptwebqq)
