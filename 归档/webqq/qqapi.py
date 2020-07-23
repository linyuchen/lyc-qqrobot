# coding=UTF8

import time
import json
import random
import requests
import webqqencrypt
import qqsdk

encrypt = webqqencrypt.Encrypt()

entity = qqsdk.entity


class QQApi(object):
    """
    self.qq: str, QQ号
    self.pwd: str, QQ密码
    self.online: bool, 是否处于在线状态, 登录成功才是True
    """
    
    def __init__(self, qq, pwd):

        super(QQApi, self).__init__()
        self.qq = qq
        self.pwd = pwd
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "zh-CN,zh;q=0.8",
                "Connection": "keep-alive",
                "Referer": "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"}

#        self.headers = {}
        self.http = requests.session()
        self.http.headers = self.headers

        self.clientid = "53999199"
        self.ptwebqq = ""
        self.vfwebqq = ""
        self.psessionid = ""
        self.port = ""
        self.gtk = ""
        self.verifyCode = ""
        self.needVerifyCode = False
        self.groupMsg_id = self.buddyMsgId = random.randint(0, 6000000)
        self.fontStyle = entity.FontStyle(u"黑体", 12, 16711680)
        self.verifyCodePath = "verfiycode.jpg"

        self.friends_dic = {}
        self.groups_dic = {}
        self.groups_info_dic = {} # key gcode, value dict

        # key: uin, value: qq
        self.online = False


    def __getPtui(self,key,data):
        
        data = data.strip()
        data = data[len(key) : -1]
        return eval(data)

    def check(self):
        """
        检查QQ是否能直接登录，
        @rtype:bool，False需要验证码
        """
        
        url = "https://ssl.ptlogin2.qq.com/check?pt_tea=1&uin=" + self.qq + "&appid=501004106&js_ver=10126&js_type=0&login_sig=&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html&r=0.8155406711157411"

        res = self.http.get(url)
        data = res.text
#        print data

        ptui = self.__getPtui("ptui_checkVC", data)
        self.verifyCode = ptui[1]
        self.uin = ptui[2]
        if "0" != ptui[0]:
            url="https://ssl.captcha.qq.com/getimage?aid=501004106&r=0.7308882384095341&uin=" + self.qq + "&cap_cd=" + self.verifyCode
            res = self.http.get(url)
            data = res.content
            with open(self.verifyCodePath,"wb") as f:
                f.write(data)
                
            self.needVerifyCode = True
            
            self.ptvfsession = res.cookies.get("verifysession")
            return False
        self.ptvfsession = res.cookies.get("ptvfsession")
        return True
        

    def __login1(self):
        """
        成功返回True
        失败返回失败原因(str)
        """

#        print repr(self.uin), self.ptvfsession
        p = encrypt.encryptPassword(self.pwd, self.verifyCode, self.uin)
        url = "https://ssl.ptlogin2.qq.com/login?u=" + self.qq 
        url += "&p=" 
        url += p 
        url += "&verifycode=" 
        url += self.verifyCode
        # print self.verifyCode
        url += "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-99-17525&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10126&login_sig=&pt_randsalt=0&pt_vcode_v1=0&pt_verifysession_v1=" 
        url += self.ptvfsession
        # print url
        res = self.http.get(url)
        self.needVerifyCode = False
        data = res.text
        # print data
        
        ptui = self.__getPtui("ptuiCB", data)
        # print ptui
        if ptui[0] == "0":
            self.ptwebqq = res.cookies.get("ptwebqq")
#            print self.qq, self.ptwebqq
            self.hash_code = encrypt.getHash(self.qq, self.ptwebqq)
#            print self.hash_code
            skey = res.cookies.get("skey")
            self.gtk = encrypt.get_gtk(skey)
            url = ptui[2]
            res = self.http.get(url)
            data = res.text
            self.gtk = str(self.gtk)
                        
            return True
        else:
            return data
            # reason = ptui[3]
            # return reason
#        print self.ptwebqq

    def __login2(self):
        """
        成功返回True
        失败返回失败原因(str)
        """
        #return True
        url="http://d.web2.qq.com/channel/login2"
        headers = self.headers.copy()
        headers["Referer"] = "http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2"
        a={"status": "callme", "ptwebqq": self.ptwebqq, "passwd_sig": "", "clientid": self.clientid, "psessionid": ""}
        a=json.dumps(a)
        a = {"r": a, "clientid": self.clientid, "psessionid": "null"}
        res = self.http.post(url, data=a)
#        print res.text
        result = res.json()
#        print result
        if not result["retcode"]:
            self.vfwebqq = self.get_vfwebqq(self.ptwebqq)
            self.psessionid = result["result"]["psessionid"]
            self.port = result["result"]["port"]
            self.index = result["result"]["index"]
            return True
        else:
            return result

    def get_vfwebqq(self, ptwebqq):

        url = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&clientid=%s&psessionid=&t=%d" % (ptwebqq, self.clientid, time.time() * 1000)
#        print url
#        print self.http.headers
        data = self.http.get(url).json()
#        print data
        return data["result"]["vfwebqq"]

    def login(self):
        """
        @return True:登录成功
        @return dic: 登录失败的原因
        """
        loginReuslt = self.__login1()
        if loginReuslt == True:
            loginReuslt = self.__login2()
            if loginReuslt == True:
                self.online = True
                return True
            else:
                return loginReuslt

        else:
            return loginReuslt
            
    def logout(self):
        """
        @return: 是否登出成功
        @rtype: bool
        """
        """
        http://d.web2.qq.com/channel/logout2?ids=&clientid=8745204&psessionid=8368046764001d636f6e6e7365727665725f77656271714031302e3133332e34312e383400000f45000000bb026e0400ecc3f92a6d0000000a405567555632306442656d00000028bfe6b3a295e03ef3b9491e5c366de0096cc6a710529f8c527249e7f3aafe4a8036cd44f7a39e02dc&t=1386995870481
        """
        url = "http://d.web2.qq.com/channel/logout2?ids=&clientid=" + self.clientid + "&psessionid=" + self.psessionid + "&t=" + str(int(time.time()))
        data = self.http.get(url).json()
#        print data
        if data["result"] == "ok":
            self.online = False
            return True
        else:
            return False
        return data

    def getDicFromList(self, dic_list, key, value):
        """
        """
        """
        @param dic_list: [{key:value},{key:value}]
        @param key: 
        @param value:
        @rtype: dict
        """
        result_list = [] # [{},{}]
        for dic in dic_list:
            if (isinstance(dic[key],int) or isinstance(dic[key],long)) and (isinstance(value,str) or isinstance(value,unicode)):
                if value.isdigit():
                    value = int(value)
            if dic[key] == value:
                result_list.append(dic)
        return result_list

    def getFriends(self):
        """
        例子：{"retcode":0,"result":{"friends":[{"flag":20,"uin":597845441,"categories":5},{"flag":20,"uin":769476381,"categories":5}],"marknames":[{"uin":3215442946,"markname":"林彬YAN","type":0}],"categories":[{"index":0,"sort":0,"name":"yi~~呀咿呀~"},{"index":5,"sort":5,"name":" 孤单相伴"}],"vipinfo":[{"vip_level":0,"u":597845441,"is_vip":0},{"vip_level":2,"u":769476381,"is_vip":1}],"info":[{"face":0,"flag":20972032,"nick":"林雨辰的那只神经喵喵","uin":597845441},{"face":288,"flag":20972102,"nick":" ☆紫梦璃★","uin":769476381}]}}
        @rtype: dict
        """

        self.vfwebqq = self.get_vfwebqq(self.ptwebqq)
        url = "http://s.web2.qq.com/api/get_user_friends2"
        a = {"hash": self.hash_code, "vfwebqq": self.vfwebqq}
        a = json.dumps(a)
        data = {"r": a}
        data = self.http.post(url, data=data).json()
#        print u"获取好友列表", data
        return data
    

    def getOnlineFriedns(self):

        """
        例子：{"retcode":0,"result":[{"uin":597845441,"status":"online","client_type":1},{"uin":769476381,"status":"online","client_type":1}]}
        @rtype: dict
        
        """
        url = "http://d.web2.qq.com/channel/get_online_buddies2?clientid="+self.clientid+"&psessionid="+self.psessionid+"&t=1376715224899"
        data = self.http.get(url).json()
        return data


    def uin2number(self, uin, type=1):
        """
        uin转真实QQ号
        uin: int,临时号码
        type: int, 1 好友uin转QQ，4 群uin转群号 已经失效!
        @rtype: ink
        """

        url = "http://s.web2.qq.com/api/get_friend_uin2?tuin="+str(uin)+"&verifysession=&type=%d&vfwebqq="%(type) + self.vfwebqq+"&t=1376721666740"
        # print url
        # "http://s.web2.qq.com/api/get_friend_uin2?tuin=632070613&type=1&vfwebqq=59c08b73191abc6aac224697750d296b4148f36d3b3fb4f21079930d2572047a0d9a9d6e1a64130f&t=1442134450901"
        data = self.http.get(url).json()
        # print data
        # print data["tips"]
        if not data.has_key("result"):
            return 0
#        print data
        qq = data["result"]["account"]
        return qq


    def getGroups(self):
        """
        {"retcode":0,"result":{"gmasklist":[{"gid":1000,"mask":3},{"gid":3181386224,"mask":0},{"gid":3063251357,"mask":2}],"gnamelist":[{"flag":1090519041,"name":"神经","gid":3181386224,"code":1597786235},{"flag":16777217,"name":"哭泣","gid":3063251357,"code":3462805735}],"gmarklist":[]}}
        
        mask: 群消息接收设置,如果为空，则使用群本身消息设置并每个群都接收
        code: gcode
        gid: 不明白

        @return: json
        @rtype: dict
        """

        url = "http://s.web2.qq.com/api/get_group_name_list_mask2"
        r = {"vfwebqq":self.vfwebqq,"hash":self.hash_code}
        a = json.dumps(r)
        data = {"r":a}
        data = self.http.post(url,data=data).json()
        return data

    def getGroupInfo(self,gCode):
        """
        {"retcode":0,"result":{"stats":[{"client_type":41,"uin":379450326,"stat":10},{"client_type":1,"uin":769476381,"stat":10}],"minfo":[{"nick":"神经喵咪","province":"","gender":"female","uin":379450326,"country":"","city":""},{"nick":" ☆紫梦璃★","province":"","gender":"female","uin":769476381,"country":"梵蒂冈","city":""}],"ginfo":{"face":0,"memo":"","class":10028,"fingermemo":"","code":1597786235,"createtime":1362561179,"flag":1090519041,"level":0,"name":"神经","gid":3181386224,"owner":769476381,"members":[{"muin":379450326,"mflag":4},{"muin":769476381,"mflag":196}],"option":2},"vipinfo":[{"vip_level":0,"u":379450326,"is_vip":0},{"vip_level":2,"u":769476381,"is_vip":1}]}}

        @rtype: dict
        """
        url = "http://s.web2.qq.com/api/get_group_info_ext2?gcode="+str(gCode)+"&vfwebqq="+self.vfwebqq+"&t=1376720992778"
        data = self.http.get(url).json()
        return data
#         if data["retcode"] == 0:
#             self.groups_info_dic[gCode] = data["result"]
#             return 0
#         else:
#             return data["retcode"]
# #            return self.getGroupMember(gCode)
#         return data


    def getMsg(self):
        """
        获取消息，返回dict
        """

        url = "http://d.web2.qq.com/channel/poll2"
#        a = {"clientid":self.clientid,"psessionid":self.psessionid,"key":0,"ids":[]}
#        a = json.dumps(a)
#        print type(a)
        data = {"clientid": self.clientid, "psessionid": self.psessionid, "key":"", "ptwebqq": self.ptwebqq}
        data = {"r": json.dumps(data)}
        headers = self.headers
        headers["Referer"] = "http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2"
        res = self.http.post(url, data=data, headers=headers)
        data = res.json()
        return data

    def __convertMsg(self,content):


        content = content.replace("\\","\\\\").replace("\r\n","\n").replace("\n","\\n").replace("\"","\\\"").replace("\t","\\t")

        return content

    def __getGroupSig(self,groupId,buddyId):

        url = "http://d.web2.qq.com/channel/get_c2cmsg_sig2?id=%s&to_uin=%s&service_type=0&clientid=%s&psessionid=%s&t=%d"%(groupId,buddyId,self.clientid,self.psessionid,int(time.time() * 100))

        data = self.http.get(url).json()
        data = json.loads(data)
        if data["retcode"] != 0:
            return ""
        sig = data["result"]["value"]
        return sig

    def sendTempMsgFromGroup(self,groupId,buddyId,content,fontStyle=None):
        """
        groupId: 群uin
        buddyId: 对方uin
        content: 要发送的内容，Unicode编码
        fontStyle: entity.FontStyle
        """
        
        if not fontStyle:
            fontStyle = self.fontStyle
        group_sig = self.__getGroupSig(groupId,buddyId)

        content = self.__convertMsg(content)
        url = "http://d.web2.qq.com/channel/send_sess_msg2"
        a ={"to":buddyId,"group_sig":group_sig,"face":0,"content":"[\"%s\",[\"font\",%s]]"%(content,fontStyle),"msg_id":self.buddyMsgId,"service_type":0,"clientid":self.clientid,"psessionid":self.psessionid}
        a = json.encoder.JSONEncoder().encode(a)
        data = {"clientid":self.clientid,"psessionid":self.psessionid, "r": a}

        data = self.http.post(url,data=data).json()
#        print data
        return data


    def sendMsg2Buddy(self,buddyId,content,fontStyle=None):
        # buddyId: 好友的uin
        # content: 要发送的内容，unicode编码
        # fontStyle: entity.FontStyle
        # print buddyId, content
        if not fontStyle:
            fontStyle = self.fontStyle

        url = "http://d.web2.qq.com/channel/send_buddy_msg2"

        content = self.__convertMsg(content)
        self.buddyMsgId += 1
        a = {"to": buddyId, "face": 1, "content": "[\"%s\",[\"font\",%s]]"%(content, fontStyle),"msg_id":self.buddyMsgId,"clientid":self.clientid,"psessionid":self.psessionid}
        a = json.encoder.JSONEncoder().encode(a)
        data = {"clientid": self.clientid, "psessionid": self.psessionid, "r": a}
        data = self.http.post(url, data=data).json()
        return data

    def sendMsg2Group(self, groupId, content, fontStyle=None):
        """
        groupId:群uin
        content: 要发送的内容, unicode编码
        fontStyle: entity.FontStyle实例
        """

        if not fontStyle:
            fontStyle = self.fontStyle

        url="http://d.web2.qq.com/channel/send_qun_msg2"
        content = self.__convertMsg(content)
        self.groupMsg_id += 1
        a = {"group_uin":groupId,"content":"[\""+content+"\",[\"font\",%s]]"%fontStyle,"msg_id":self.groupMsg_id,"clientid":self.clientid,"psessionid":self.psessionid}
        a=json.dumps(a)
        data={"clientid":self.clientid,"psessionid":self.psessionid,"r":a}
#        print data
        data = self.http.post(url, data=data).json()
#        url = "http://tj.qstatic.com/getlog?qqweb2=%s$groupmask$bottom$send&t=1377456226064"%self.qq
        return data

    # 同意别人添加自己好友
    # 参数 别人的QQ号 备注
    def allowAddFriend(self, qq, mname):

        url = "http://s.web2.qq.com/api/allow_and_add2"

        r = {"account":qq,"gid":0,"mname":"","vfwebqq":self.vfwebqq}
        r = json.dumps(r)
        data = {"r":r}
        data = self.http.post(url, data=data).json()
        return data
    
    # 处理别人加群消息（必须是管理员才有效）
    # 参数 reqUin 加群者的临时号码， groupUIn 加的群的临时号码，msg 拒绝理由，allow True是同意加群，False是不同意
    def handleAddGroupMsg(self, reqUin, groupUin, msg="", allow=True):

        msg = self.http.quote(msg)
        if allow:
            opType = 2
        else:
            opType = 3
        url = "http://d.web2.qq.com/channel/op_group_join_req?group_uin=%s&req_uin=%s&msg=%s&op_type=%d&clientid=%s&psessionid=%s"%(groupUin,reqUin,msg,opType,self.clientid,self.psessionid)
        data = self.http.get(url).json
        return data

    def deleteGroupMember(self, group_number, qq_number):

        """
        @return 
            int: 0 成功
            int: 3 成员不存在
            int: 7 权限不足
            int: 11 群号错误
            int: -1 网络错误
        """
        url = "http://qinfo.clt.qq.com/cgi-bin/qun_info/delete_group_member"

        post_data = {"gc":group_number, "ul": qq_number, "bkn": self.gtk}

        res_content = self.http.post(url, data=post_data).json()

        return res_content["ec"]
        
    def quitGroup(self,gcode):
        # 退群

        url = "http://s.web2.qq.com/api/quit_group2"
        r = json.dumps({"gcode":gcode,"vfwebqq":self.vfwebqq})
        post_data = {"r": r}
        result = self.http.post(url, data=post_data).json()
        return result

    def changeGroupMessageFilter(self,group_uin="",state=0,all_state=0):

        """
        @param group_uin: 群临时号码
        @param state: 0 接收并提醒，1 接收不提醒，2 不接受
        @param all_state: 0 使用每群自身的消息设置，1 所有群接收并提示， 2 接收不提示，3 不接收
        """
        """
        retype:1
        app:EQQ
        itemlist:{"groupmask":{"3063251357":"2","3181386224":"1","cAll":3,"idx":1075,"port":25293}}
        vfwebqq:9ac2d0e9f567ad545d57dc336165e1b3a340e14d1534d802ecd7fdf363f380cbe7751f8f7e657e4e
        """
        url = "http://cgi.web2.qq.com/keycgi/qqweb/uac/messagefilter.do"

        self.groups_dic["gmasklist"][0]["mask"] = all_state
        groupmask = {"cAll":all_state,"idx":self.index,"port":self.port}
        for dic in self.groups_dic["gmasklist"]:
            uin = str(dic["gid"])
            if uin == "1000":
                continue
            if uin == group_uin:
                dic["mask"] = state
            mask = dic["mask"]

            groupmask[uin] = "%d"%mask
        itemlist = {"groupmask":groupmask}
        itemlist = json.dumps(itemlist)#.replace(" ","").replace("\\","")
        post_data = {"retype":"1","app":"EQQ","itemlist":itemlist,"vfwebqq":self.vfwebqq}
        result = self.http.post(url, post=post_data).json()
        return result["retcode"]

    def getFriendMsgImage(self, file_path, friendUin):
        """
        获取好友消息里的图片
        相关参数在好友图片消息中获得
        @type file_path: str
        @type friendUin: int

        @return: 返回图片的内容,  由于是二进制，保存图片时open参数要用wb
        @rtype: str
        """

        file_path = file_path.replace("/", "%2f")
        url = "http://d.web2.qq.com/channel/get_offpic2?file_path=%s&f_uin=%s&clientid=%s&psessionid=%s" % (file_path, str(friendUin), self.clientid, self.psessionid)
        return self.http.get(url)

    def getGroupMsgImage(self, gcode, groupMemberUin, server, fileId, filePath):
        """
        获取群消息里的图片
        相关参数在群图片消息中获得
        @param gcode: str
        @param groupMemberUin: int
        @param server: str, 图片服务器ip
        @param fileId: str, 图片id,
        @param filePath: str, 图片文件名

        @return: 返回图片内容, 由于是二进制，保存图片时open参数要用wb
        @rtype: str
        """

        filePath = self.http.quote(filePath)
        server = server.split(":")
        server = server[0]
        url = "http://web2.qq.com/cgi-bin/get_group_pic?type=0&gid={gcode}&uin={groupMemberUin}&rip={rip}&rport=80&fid={fid}&pic={filePath}&vfwebqq={vfwebqq}&t=1424464032".format(gcode=gcode, groupMemberUin=groupMemberUin, rip=server, fid=fileId, filePath=filePath, vfwebqq=self.vfwebqq)
        return self.http.get(url)
        filePath = self.http.quote(filePath)
        server = server.split(":")
        server = server[0]
        url = "http://web2.qq.com/cgi-bin/get_group_pic?type=0&gid={gcode}&uin={groupMemberUin}&rip={rip}&rport=80&fid={fid}&pic={filePath}&vfwebqq={vfwebqq}&t=1424464032".format(gcode=gcode, groupMemberUin=groupMemberUin, rip=server, fid=fileId, filePath=filePath, vfwebqq=self.vfwebqq)
        return self.http.get(url)




if "__main__" == __name__:
    qq_number = raw_input("qq:")
    qq_pwd = raw_input("pwd:")
    qq = QQApi(qq_number, qq_pwd)
    checkResult = qq.check()
    if checkResult == False:
        qq.verifyCode = raw_input("verify code:")
        

    print qq.login()
#    print qq.getFriends()
#    print qq.getMsg()
#    print qq.delete_group_member("291186448","379450326")
#    print qq.getFriends()
#    print qq.getGroups()
#     print qq.uin2number("1280520008", 4)

#    qq.deleteGroupMember("149443938", "721011691")

