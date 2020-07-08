# coding=UTF8
import thread
import time
import json

from 归档.webqq import qqapi

QQApi = qqapi.QQApi
entity = qqapi.qqsdk.entity
message = qqapi.qqsdk.message


class QQClient(qqapi.qqsdk.QQClient, QQApi):
    """
    self.loginSucCount: int, 登录成功的次数
    """
    def __init__(self, qq, pwd):
        self.logoutCodes = [121, 108, 103]
        self.getMsgFailedCount = 0

        #
        self.__qqNumbers = {}  # key uin,qq
        self.__uinNumbers = {}  # key qq, value uin
        self.__groupQQNumbers = {}  # 同上
        self.__groupUinNumbers = {}  # key group qq, value group uin
        self.msgIds = []  # item 为元组(msg_id1, msg_id2)，用于保存已经收到过的msg
        self.msgIdsMaxNum = 50  # self.msgIds 最大容量，超出则pop(0)
        
        QQApi.__init__(self, qq, pwd)
        qqapi.qqsdk.QQClient.__init__(self)


    def uin2number(self, uin, type=1):
        """
        type 4:群
        """
        if type == 1:
            qqNumberDict = self.__qqNumbers
        elif type == 4:
            qqNumberDict = self.__groupQQNumbers
        else:
            return

        if qqNumberDict.has_key(uin):
            return qqNumberDict[uin]
        qq = QQApi.uin2number(self, uin, type)
            
        if qq:
            qqNumberDict[uin] = qq
            if type == 1:
                self.__uinNumbers[qq] = uin
            elif type == 4:
                self.__groupUinNumbers[qq] = uin
        return qq

    def debug(self):
        self.__startListenEventsAfterLogin()

    def login(self):

        msg = u"开始登陆...\n"
        if not self.loginSucCount:
            self.__startListenEventsBeforLogin()
        checkResult = self.check()
        msg += u"是否需要验证码:" + unicode(not checkResult) + "\n"
        if not checkResult:
            _msg = message.BaseMsg()
            _msg.msg = checkResult
            self.__needVerifyCodeMsgs.put(_msg)
            while self.needVerifyCode: pass

        loginResult = QQApi.login(self)
        msg += u"登录结果: %s"%(unicode(loginResult))
        self.addLogMsg(msg)

        if loginResult != True:
            msg = message.BaseMsg()
            msg.msg = loginResult
            self.__loginFailedMsgs.put(msg)
            if u"验证码不正确" in loginResult:
                self.login()
        else:
            #self.__loginSuccessMsgs.append(loginResult)
            self.qqUser = entity.QQUser()
            self.qqUser.gtk = self.gtk
            self.online = True
            self.getFriends()
            self.getGroups()

            for event in self.loginSuccessEvents:
                event.main(loginResult)
            
            if not self.loginSucCount:
                self.__startListenEventsAfterLogin()
                thread.start_new_thread(self.__startSendMsgFuncPool,(None,))

            self.loginSucCount += 1

    def getFriends(self):

        """
        获取好友，结果将放在self.qqUser.friends里面
            self.qqUser.friends是个dict，key是uin，value是entity.Friend实例
        """
        """
        {"retcode":0,"result":{"friends":[{"flag":20,"uin":597845441,"categories":5},{"flag":20,"uin":769476381,"categories":5}],"marknames":[{"uin":3215442946,"markname":"林彬YAN","type":0}],"categories":[{"index":0,"sort":0,"name":"yi~~呀咿呀~"},{"index":5,"sort":5,"name":" 孤单相伴"}],"vipinfo":[{"vip_level":0,"u":597845441,"is_vip":0},{"vip_level":2,"u":769476381,"is_vip":1}],"info":[{"face":0,"flag":20972032,"nick":"林雨辰的那只神经喵喵","uin":597845441},{"face":288,"flag":20972102,"nick":" ☆紫梦璃★","uin":769476381}]}}
        """
        data = QQApi.getFriends(self)
        if data["retcode"] == 0:
            data = data["result"]
            for i in data["friends"]:
                friendObj = entity.Friend()
                uin = i["uin"]
                uin = long(uin)
                friendObj.uin = uin
                groupId = data["categories"]

                friendObj.groupId = groupId
                friendObj.groupName = self.__getValueFromDic(groupId, data["categories"], "index", "name")
                friendObj.markName = self.__getValueFromDic(uin, data["marknames"], "uin", "markname")
                friendObj.nick = self.__getValueFromDic(uin, data["info"], "uin", "nick")
                friendObj.get_qq = self.uin2number

                self.qqUser.friends[uin] = friendObj
#                print self.qqUser.friends

    def getGroupByQQ(self, groupQQ):
        """
        @param groupQQ: 群号
        @rtype: entity.Group实例
        """
        if self.__groupUinNumbers.has_key(groupQQ):
            uin = self.__groupUinNumbers[groupQQ]
        else:
            return None
        group = self.qqUser.groups[uin]
        return group

    def getGroups(self):
        """
        结果保存在 self.qqUser.groups，self.qqUser.groups是个dict，key uin，value entity.Group实例
        """
        """
        {"retcode":0,"result":{"gmasklist":[{"gid":1000,"mask":3},{"gid":3181386224,"mask":0},{"gid":3063251357,"mask":2}],"gnamelist":[{"flag":1090519041,"name":"神经","gid":3181386224,"code":1597786235},{"flag":16777217,"name":"哭泣","gid":3063251357,"code":3462805735}],"gmarklist":[]}}
        """

        data = QQApi.getGroups(self)

        if data["retcode"] == 0:
            data = data["result"]
#            print data
            for gname in data["gnamelist"]:
#                gid = maskDic["gid"]
#                uin = long(uin)                
                uin = gname["gid"]
                group = entity.Group()
                group.uin = uin
                group.gid = uin
                group.code = gname["code"]
                mask = self.__getValueFromDic(uin, data["gmasklist"], "gid", "mask")
                if not mask:
                    mask = 0
                group.mask = mask
                group.name = gname["name"]
#                groupQQ = self.uin2number(uin ,type=4)
#                print groupQQ
#                group.members = []

                self.qqUser.groups[uin] = group
                self.getGroupMembers(uin)
#                print self.groups

    def getGroupMembers(self,uin):
        """
        uin: group uin
        members保存在entity.Group.members
        """

        """
        {"retcode":0,"result":{"stats":[{"client_type":41,"uin":379450326,"stat":10},{"client_type":1,"uin":769476381,"stat":10}],"minfo":[{"nick":"神经喵咪","province":"","gender":"female","uin":379450326,"country":"","city":""},{"nick":" ☆紫梦璃★","province":"","gender":"female","uin":769476381,"country":"梵蒂冈","city":""}],"ginfo":{"face":0,"memo":"","class":10028,"fingermemo":"","code":1597786235,"createtime":1362561179,"flag":1090519041,"level":0,"name":"神经","gid":3181386224,"owner":769476381,"members":[{"muin":379450326,"mflag":4},{"muin":769476381,"mflag":196}],"option":2},"vipinfo":[{"vip_level":0,"u":379450326,"is_vip":0},{"vip_level":2,"u":769476381,"is_vip":1}]}}
        """
        group = self.getGroupByUin(uin)
        data = QQApi.getGroupInfo(self, group.code)
        members = {}
        if data["retcode"] == 0:
            data = data["result"]
            # 如果有群名片的话，result里面会有cards这个key
            if data.has_key("cards"):
                cards = data["cards"] # [{muin: 3764013857, card: "呵呵"}]
            else:
                cards = []
            group.createTime = data["ginfo"]["createtime"]
            creator = data["ginfo"]["owner"]
#            print data
            for memberDic in data["ginfo"]["members"]:
                uin = memberDic["muin"]
#                uin = long(uin)
                member = entity.GroupMember()                
                if uin == creator:
                    group.creator = member
                member.nick = self.__getValueFromDic(uin, data["minfo"], "uin", "nick")
                member.isAdmin = not ((self.__getValueFromDic(uin, data["ginfo"]["members"], "muin", "mflag"))%2 == 0)
                member.status = self.__getValueFromDic(uin,data["stats"],"uin","stat")
                member.card = self.__getValueFromDic(uin,cards,"muin","card")
                member.uin = uin
                member.get_qq = self.uin2number
                members[uin] = member

        group.members = members
#        print members

    def __getValueFromDic(self,standardValue,dicList,standardKey,needKey):
        """
        """
        for i in dicList:
            if standardValue == i[standardKey]:
                return i[needKey]

        return ""

    def handleAddGroupMsg(self,reqUin,groupUin,msg="",allow = True):
        """
        @param reqUin: 加群者的uin
        @type reqUin: int

        @param groupUin: 所加的群的uin
        @type:int

        @msg: 拒绝加群时填的消息
        @type: str

        @param allow:是否同意加群
        @type: bool
        """
        QQApi.handleAddGroupMsg(self, reqUin, groupUin, msg, allow)
        qq = self.uin2number(reqUin)
        group = self.getGroupByUin(groupUin)
        msgContent = u"QQ%d加入群（%s）[%d], 验证信息：%s"%(qq, group.name, group.qq, msg)
        if allow:
            self.getGroupMembers(groupUin)
            logMsg = u"同意了" + msgContent
        else:
            logMsg = u"拒绝了" + msgContent

        self.addLogMsg(logMsg)


    def __mergeMsg(self,msg):
        
        result = ""
        for i in msg:
            if isinstance(i,list):
                continue
            else:
                result += i
        return result.strip()
    
    def checkMsgId(self, msgId1,msgId2):
        
        msgId = (msgId1, msgId2)
        exists = msgId in self.msgIds
        self.msgIds.append(msgId)

        if len(self.msgIds) > self.msgIdsMaxNum:
            self.msgIds.pop(0)

        return exists
        
    def getMsg(self):

        dic = qqapi.QQApi.getMsg(self)

#        logMsg = u"收到消息(全), " + str(dic)
#        self.addLogMsg(logMsg)

        if not dic.has_key("retcode"):
            self.recordMsgError()
            return

        if 0 == dic["retcode"] and isinstance(dic["result"], list):

            self.getMsgFailedCount = 0
            resultDic = {"Data":[]}

            for i in dic["result"]:

#                i = copy.deepcopy(i)
               
                """
                {u'retcode': 0, u'result': [{u'poll_type': u'buddies_status_change', u'value': { u'status': u'online', u'client_type': 1, u'uin': 2010848814}}]} 
                好友状态改变
                
                """
                msgDic = {"SendTime": time.time(), "Event": "Error"}  # 根据下面的分析生成
                if "buddies_status_change" == i["poll_type"]:

                    data = i["value"]
                    uin = data["uin"]
#                    uin = self.uin2number(uin)
                    msgDic.update({"Event": message.FriendStatusChangeMsg.EVENT_NAME, "Data":{"Sender": uin, "QQStatus": data["status"]}})
                    

                elif "message" == i["poll_type"]:# 好友消息
                    """
                    {"retcode":0,"result":[{"poll_type":"message","value":{"msg_id":26113,"from_uin":908551613,"to_uin":721011692,"msg_id2":266862,"msg_type":9,"reply_ip":178848407,"time":1386500840,"content":[["font",{"size":11,"color":"ff00ff","style":[1,0,0],"name":"\u5FAE\u8F6F\u96C5\u9ED1"}],"\u5475\u5475 "]}}]}
                    """
                    data = i["value"]
                    if self.checkMsgId(data["msg_id"], data["msg_id2"]):
                        continue
                    uin = data["from_uin"]
#                    uin = self.uin2number(uin)
#                    uin = long(uin)

                    originalMsg = data["content"][1:]
#                    print msg.originalMsg
                    msg = self.__mergeMsg(originalMsg)
#                    print msg.msg
                    msgDic = {"Event": message.FriendMsg.EVENT_NAME, "Data":{"Sender": uin, "SendTime": data["time"],
                            "Message": msg}}

                elif "sess_message" == i["poll_type"]:# new temporary conversation message
                    """
                    {"retcode":0,"result":[{"poll_type":"sess_message","value":{"msg_id":29709,"from_uin":3863325290,"to_uin":1546582558,"msg_id2":51531,"msg_type":140,"reply1_ip":178848406,"time":1376718421,"id":456949784,"ruin":379450326,"service_type":0,"flags":{"text":1,"pic":1,"file":1,"audio":1,"video":1},"content":[["font",{"size":11,"color":"ff0000","style":[1,0,0],"name":"\u5FAE\u8F6F\u96C5\u9ED1"}],"a "]}}]}

                    """
                    data = i["value"]
                    if self.checkMsgId(data["msg_id"], data["msg_id2"]):
                        continue
                    uin = data["from_uin"]
#                    uin = long(uin)
#                    msg.ip = data["reply1_ip"]
                    qq = int(data["ruin"])
                    self.__qqNumbers[uin] = qq
#                    time = data["time"]
                    originalMsg = data["content"][1:]
#                    print msg.originalMsg
                    msg = self.__mergeMsg(originalMsg)
#                    print msg.msg

                elif "group_message"==i["poll_type"]:# New group message
                    """
                     {"retcode":0,"result":[{"poll_type":"group_message","value":{"msg_id":16985,"from_uin":456949784,"to_uin":1546582558,"msg_id2":519158,"msg_type":43,"reply_ip":176488598,"group_code":432844316,"send_uin":1615088372,"seq":2869,"time":1376716816,"info_seq":141382064,"content":[["font",{"size":11,"color":"ff00ff","style":[1,0,0],"name":"\u5FAE\u8F6F\u96C5\u9ED1"}],"1 "]}}]}

                    """
                    data = i["value"]
#                    print data
                    if self.checkMsgId(data["msg_id"], data["msg_id2"]):
                        continue
                    uin = data["from_uin"]
                    memberUin = data["send_uin"]

                    groupQQ = data["info_seq"]
                    self.__groupUinNumbers[groupQQ] = uin
                    originalMsg = data["content"][1:]
                    msg = self.__mergeMsg(originalMsg)
                    group_object = self.getGroupByUin(uin)
                    group_object.qq = groupQQ
                    member = group_object.getMemberByUin(memberUin)
#                    print memberUin
                    member.qq = self.uin2number(memberUin)
                    msgDic.update({"Event": message.GroupMsg.EVENT_NAME, "Data":{"ClusterNum": uin,
                        "Sender": memberUin, "Message": msg, "SendTime": data["time"]}})
                    
                elif "system_message" == i["poll_type"]:

                    data = i["value"]
                    if "verify_required" == data["type"]:# Add me friend
                        """
                        {"retcode":0,"result":[{"poll_type":"system_message","value":{"seq":34653,"type":"verify_required","uiuin":"","from_uin":3863325290,"account":379450326,"msg":"adfas","allow":1,"stat":10,"client_type":1}}]}
                        """
                        uin = data["from_uin"]
                        qq = data["account"]
                        msg = data["msg"]
                        allow = data["allow"]
                        msgDic.update({"Event": message.RequestAddMeFriend.EVENT_NAME, "Data":{ "Sender": qq}})

                    elif "added_buddy_sig" == data["type"]:

                        """
                        收到消息(全), {u'retcode': 0, u'result': [{u'poll_type': u'system_message', u'va lue': {u'account': 721011691, u'seq': 59188, u'stat': 20, u'uiuin': u'', u'sig': u'\xb5!\xdctN\xfbX@e\x03\xee\xf9\x0bb\xaa\x1f\x99S\xf1\x856\xe4/\xb2', u'from_uin': 1849509427, u'type': u'added_buddy_sig'}}]}
                        别人添加了我为好友 
                        """
                        uin = data["from_uin"]
                        qq = data["account"]

                elif "sys_g_msg" == i["poll_type"]:# New group system message
                    
                    data = i["value"]
                    if self.checkMsgId(data["msg_id"], data["msg_id2"]):
                        continue
                    groupUin = data["from_uin"]#Group's temporary number
                    msgType = data["type"]
                    
                    if "group_leave" == msgType:
                        """
                        我被踢出群
                        {"retcode":0,"result":[{"poll_type":"sys_g_msg","value":{"msg_id":25842,"from_uin":3547669097,"to_uin":721011692,"msg_id2":587672,"msg_type":34,"reply_ip":176488602,"type":"group_leave","gcode":869074255,"t_gcode":164461995,"op_type":3,"old_member":721011692,"t_old_member":"","admin_uin":3530940629,"t_admin_uin":"","admin_nick":"\u521B\u5EFA\u8005"}}]}
                        t_gcode: 群号
                        """
                        groupQQ = data["t_gcode"]
                        adminUin = data["admin_uin"]
                        adminNick = data["admin_nick"]
                        msgDic.update({"Event": message.GroupRemoveMeMsg.EVENT_NAME, "Data":{}})

                    elif "group_admin_op" == msgType:
                        """
                        
                        管理员变更(设置)
                        {u'retcode': 0, u'result': [{u'poll_type': u'sys_g_msg', u'value': {u'reply_ip': 180061933, u'uin_flag': 1, u'msg_type': 44, u't_uin': 721011692, u'type': u'group_admin_op', u't_gcode': 291186448, u'msg_id': 36217, u'uin': 721011692, u'msg_id2': 254668, u'op_type': 1, u'from_uin': 3124397784L, u'gcode': 3046992595L, u' to_uin': 721011692}}]} 
                        管理员变更(取消)
                        {u'retcode': 0, u'result': [{u'poll_type': u'sys_g_msg', u'value': {u'reply_ip': 176757008, u'uin_flag': 0, u'msg_type': 44, u't_uin': 721011692, u'type': u'group_admin_op', u't_gcode': 291186448, u'msg_id': 7304, u'uin': 721011692, u'msg_id2': 428715, u'op_type': 0, u'from_uin': 3124397784L, u'gcode': 3046992595L, u't o_uin': 721011692}}]}
                        
                        """
                        groupMemberUin = data["uin"]

                        data["op_type"]

                        msgDic.update({"Event": message.GroupAdminChangedMsg.EVENT_NAME, 
                            "Data":{"ClusterNum": groupUin, "IsSet": bool(data["op_type"])} })


                    elif "group_request_join" == msgType:# Somebody want to join group
                        """
                        {"retcode":0,"result":[{"poll_type":"sys_g_msg","value":{"msg_id":62532,"from_uin":456949784,"to_uin":1546582558,"msg_id2":29087,"msg_type":35,"reply_ip":176489085,"type":"group_request_join","gcode":432844316,"t_gcode":141382064,"request_uin":3863325290,"t_request_uin":"","msg":"123"}}]}
                        """
                        msgDic.update({"Event": message.RequestJoinGroupMsg.EVENT_NAME, "Data":{
                            "ClusterNum": groupUin, "Sender": data["request_uin"], 
                            "Message": data["msg"], "SendName": str(data["request_uin"])} })


                resultDic["Data"].append(json.dumps(msgDic))

            return resultDic
            
        elif dic["retcode"] in self.logoutCodes:
            self.online = False
            msg = message.BaseMsg()
            msg.msg = dic["retcode"]
            self.__logoutMsgs.put(msg)
            logMsg = u"登出了，看看是不是掉线了"
            self.addLogMsg(logMsg)

        elif dic["retcode"] == -1:
            self.recordMsgError()
        
        elif dic["retcode"] in [102, 116]:
            """
            无消息
            """
            pass
        else:
            msg = str(dic)
            self.addErrorMsg(msg)
        
    def recordMsgError(self):

        self.getMsgFailedCount += 1
        msg = u"网络连接失败"
        self.addErrorMsg(msg)
        if self.getMsgFailedCount >= 3:
            self.online = False
            self.__logoutMsgs.put(msg)

    def __addSendBuddyMsg(self,buddyId,fontStyle,content):

        msg = message.SendBuddyMsg()
        msg.qq = self.uin2number(buddyId)
        msg.fontStyle = fontStyle
        msg.time = time.time()
        msg.content = content
        self.__sendBuddyMsgs.put(msg)
        logMsg = u"发送消息给QQ:%d：%s"%(msg.qq,content)
        self.addLogMsg(logMsg)

    def __addSendGroupMsg(self,uin,fontStyle,content):

        msg = message.SendGroupMsg()
        msg.group = self.getGroupByUin(uin)
        msg.fontStyle = fontStyle
        msg.time = time.time()
        msg.content = content
        self.__sendGroupMsgs.put(msg)
        logMsg = u"发送消息给群:%d：%s"%(msg.group.qq,content)
        self.addLogMsg(logMsg)


    def sendTempMsgFromGroup(self, groupId, buddyId, content, fontStyle=None):
        """
        groupId: 群uin
        buddyId: 对方uin
        content: 要发送的内容，Unicode编码
        fontStyle: entity.FontStyle
        """

        if fontStyle:
            fontStyle = fontStyle.__str__()
        else:
            fontStyle = self.qqUser.fontStyle
        
        self.__addSendBuddyMsg(buddyId,fontStyle,content)

        self.sendMsgFuncPool.put(lambda g=groupId, qq=buddyId, c=content, f=fontStyle: QQApi.sendMsg2Group(self, g, qq, c, f))
    

    def deleteGroupMember(self, group_number, qq_number):

        res = QQApi.deleteGroupMember(self, group_number, qq_number)
        code = res
        if code == 0:
            result = u"删除成功"
        elif code == 3:
            result = u"删除失败,此成员不存在"
        elif code == 7:
            result = u"删除失败,权限不足"
        elif code == 11:
            result = u"群号错误"
        elif code == -1:
            result = u"网络错误"
        else:
            result = u"删除失败，我不是管理员诶~"
        return result

    def api_sendMsg2Buddy(self, qq, content, fontstyle):
        QQApi.sendMsg2Buddy(self, qq, content, fontstyle)

    def api_sendMsg2Group(self, qq, content, fontstyle):
        QQApi.sendMsg2Group(self, qq, content, fontstyle)

