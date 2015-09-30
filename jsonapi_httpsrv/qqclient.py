# -*- coding:UTF-8 -*-

import time
import traceback
import Queue
import threading

import webqq.qqapi
from qqsdk import events
from qqsdk import message
from status_codes import *
from qqsdk import entity
from response import Response
from log_helper import GeneralLogger



class QQClient(webqq.qqapi.QQApi, threading.Thread):
    
    def __init__(self, qq, pwd):
        webqq.qqapi.QQApi.__init__(self, qq, pwd)
        threading.Thread.__init__(self)
        self.logger = None
        self.qq_user = entity.QQUser()
        self.__qq_numbers = {}  # key uin,qq
        self.msg_ids = []  # item 为元组(msg_id1, msg_id2)，用于保存已经收到过的msg
        self.msg_ids_max_num = 50  # self.msg_ids 最大容量，超出则pop(0)
        self.msg_handlers = {
            "buddies_status_change": self.handle_friend_status_changed_msg,
            "message": self.handle_friend_msg,
            "group_message": self.handle_group_msg,
            # "sess_message",
        }
        self.online = False
        self.msg_pool = Queue.Queue()
        self.logout_codes = [121, 108, 103]
        self.get_msg_failed_count = 1

    def first_login(self):
        self.logger = GeneralLogger(file_name="%s.log"%self.qq, err_file_name="%s_err.log"%self.qq).get_logger()
        check_result = self.check()
        print u"登录之前账号检查结果:", check_result
        if not check_result:
            vc = raw_input(u"verify code:")
            res = self.input_verify_code(vc)
        else:
            res = self.__login()

        print res.data
        if res.code == OK:
            self.start()

    def __login(self):
        try:
            result = super(QQClient, self).login()
        except:
            print u"登录联网失败"
            self.msg_pool.put([self.__make_event_dic(events.LOGOUT, u"网络错误")])
            return Response(LOGOUT, u"网络错误")
        if result is True:
            note = u"登录成功"
            print note
            self.online = True
            self.msg_pool.put([self.__make_event_dic(events.LOGIN_SUCCESS, note)])
            res = Response(OK, note)
        else:
            # print result
            self.msg_pool.put([self.__make_event_dic(events.LOGIN_FAILED, result)])
            res = Response(AUTH_FAILED, result)

        return res

    def __make_event_dic(self, event_name, data):
        event_dic = {"Event": event_name, "Data": data}
        return event_dic

    def login(self):
        check_result = self.check()
        if not check_result:
            note = u"需要验证码，请调用API输入验证码"
            # print note
            self.msg_pool.put([self.__make_event_dic(events.NEED_VC, {"Sender": self.qq, "SendTime": time.time()})])
            res = Response(NEED_VC, note)
            return res
        return self.__login()

    def input_verify_code(self, vc):
        self.verifyCode = vc
        return self.__login()

    def uin2number(self, uin, type=1):
        qq_number_dict = self.__qq_numbers
        # print "qq_number_dict", qq_number_dict
        qq = qq_number_dict.get(uin)
        if qq:
            return qq
        qq = super(QQClient, self).uin2number(uin)
        if qq:
            qq_number_dict[uin] = qq
        return qq

    def uin2qq(self, uin):
        qq = self.uin2number(uin)
        return Response(OK, qq)

    def __getValueFromDic(self, standardValue, dicList, standardKey, needKey):
        """
        """
        for i in dicList:
            if standardValue == i[standardKey]:
                return i[needKey]

        return ""

    def __get_friends(self):
        data = self.getFriends()
        # print data
        if data["retcode"] == 0:
            data = data["result"]
            for i in data["friends"]:
                _friend = entity.Friend()
                uin = i["uin"]
                uin = long(uin)
                _friend.uin = uin
                group_id = data["categories"]

                _friend.groupId = group_id
                _friend.groupName = self.__getValueFromDic(group_id, data["categories"], "index", "name")
                _friend.markName = self.__getValueFromDic(uin, data["marknames"], "uin", "markname")
                _friend.nick = self.__getValueFromDic(uin, data["info"], "uin", "nick")
                # _friend.getQQ = self.uin2number

                self.qq_user.friends[uin] = _friend

    def get_friends(self):
        self.__get_friends()
        data = {}
        for f, fo in self.qq_user.friends.items():
            data[f] = fo.__dict__

        return Response(OK, data)

    def get_groups(self):
        self.__get_groups()
        data = {}
        for u, g in self.qq_user.groups.items():
            g_info = {"uin": g.uin, "name": g.name, "mask": g.mask}
            g_info["members"] = {}
            for mu, m in g.members.items():
                m_info = m.__dict__
                g_info["members"][mu] = m_info
            data[u] = g_info
        return Response(OK, data)

    def __get_groups(self):
        data = self.getGroups()
        if data["retcode"] == 0:
            data = data["result"]
            for gname in data["gnamelist"]:
                uin = gname["gid"]
                # uin = uin
                group = entity.Group()
                group.uin = uin
                group.gid = uin
                group.code = gname["code"]
                mask = self.__getValueFromDic(uin, data["gmasklist"], "gid", "mask")
                if not mask:
                    mask = 0
                group.mask = mask
                group.name = gname["name"]
                self.qq_user.groups[uin] = group
                self.__get_group_members(uin)

    def __get_group_members(self, uin):
        """
        uin: group uin
        members保存在entity.Group.members
        """

        """
        {"retcode":0,"result":{"stats":[{"client_type":41,"uin":379450326,"stat":10},{"client_type":1,"uin":769476381,"stat":10}],"minfo":[{"nick":"神经喵咪","province":"","gender":"female","uin":379450326,"country":"","city":""},{"nick":" ☆紫梦璃★","province":"","gender":"female","uin":769476381,"country":"梵蒂冈","city":""}],"ginfo":{"face":0,"memo":"","class":10028,"fingermemo":"","code":1597786235,"createtime":1362561179,"flag":1090519041,"level":0,"name":"神经","gid":3181386224,"owner":769476381,"members":[{"muin":379450326,"mflag":4},{"muin":769476381,"mflag":196}],"option":2},"vipinfo":[{"vip_level":0,"u":379450326,"is_vip":0},{"vip_level":2,"u":769476381,"is_vip":1}]}}
        """
        group = self.getGroupByUin(uin)
        data = self.getGroupInfo(group.code)
        members = {}
        if data["retcode"] == 0:
            data = data["result"]
            # 如果有群名片的话，result里面会有cards这个key
            if data.has_key("cards"):
                cards = data["cards"]  # [{muin: 3764013857, card: "呵呵"}]
            else:
                cards = []
            group.createTime = data["ginfo"]["createtime"]
            creator = data["ginfo"]["owner"]
            # creator = str(creator)
#            print data
            for memberDic in data["ginfo"]["members"]:
                uin = memberDic["muin"]
                # uin = str(uin)
#                uin = long(uin)
                member = entity.GroupMember()
                member.nick = self.__getValueFromDic(uin, data["minfo"], "uin", "nick")
                member.isAdmin = not ((self.__getValueFromDic(uin, data["ginfo"]["members"], "muin", "mflag"))%2 == 0)
                member.status = self.__getValueFromDic(uin, data["stats"],"uin","stat")
                member.card = self.__getValueFromDic(uin, cards, "muin", "card")
                member.uin = uin
                if uin == creator:
                    group.creator = member
                    member.isAdmin = True
                    member.isCreator = True
                # member.getQQ = self.uin2number
                members[uin] = member

        group.members = members

    def handle_friend_status_changed_msg(self, i):
        """
            {u'retcode': 0, u'result': [{u'poll_type': u'buddies_status_change', u'value': { u'status': u'online', u'client_type': 1, u'uin': 2010848814}}]}
            好友状态改变

        """
        data = i["value"]
        uin = data["uin"]
        result = {"Event": events.FRIEND_STATUS_CHANGED,
                  "Data": {"Sender": uin, "QQStatus": data["status"]}
                  }
        return result

    def handle_friend_msg(self, i):
        data = i["value"]
        if self.checkMsgId(data["msg_id"], data["msg_id2"]):
            return
        uin = data["from_uin"]
    #                    uin = self.uin2number(uin)
    #                    uin = long(uin)

        originalMsg = data["content"][1:]
    #                    print msg.originalMsg
        msg = self.__mergeMsg(originalMsg)
    #                    print msg.msg
        msgDic = {"Event": events.FRIEND_MSG,
                  "Data": {"Sender": uin, "SendTime": data["time"],"Message": msg}
                  }
        return msgDic

    def checkMsgId(self, msg_id1, msg_id2):

        msg_id = (msg_id1, msg_id2)
        exists = msg_id in self.msg_ids
        self.msg_ids.append(msg_id)

        if len(self.msg_ids) > self.msg_ids_max_num:
            self.msg_ids.pop(0)

        return exists

    def handle_group_msg(self, i):
        data = i["value"]
        # print data
        if self.checkMsgId(data["msg_id"], data["msg_id2"]):
            return
        uin = data["from_uin"]
        member_uin = data["send_uin"]
        groupQQ = data["info_seq"]
        # self.__groupUinNumbers[groupQQ] = uin
        original_msg = data["content"][1:]
        msg = self.__mergeMsg(original_msg)
        group_object = self.getGroupByUin(uin)
        group_object.qq = groupQQ
        member = group_object.getMemberByUin(member_uin)
        if not member:
            self.__get_group_members(uin)
            group_object = self.getGroupByUin(uin)
            member = group_object.getMemberByUin(member_uin)            
        member.qq = self.uin2number(member_uin)
        result = {"Event": events.GROUP_MSG,
                  "Data": {"GroupQQ": groupQQ, "ClusterNum": uin,
                           "Sender": member_uin, "SenderQQ": member.qq, "Message": msg, "SendTime": data["time"]}
                  }
        return result

    def handle_temp_msg(self, i):
        """
        临时会话
        :param i:
        :return:
        """
        data = i["value"]
        if self.checkMsgId(data["msg_id"], data["msg_id2"]):
            return
        uin = data["from_uin"]
#                    uin = long(uin)
#                    msg.ip = data["reply1_ip"]
        qq = int(data["ruin"])
        self.__qqNumbers[uin] = qq
#                    time = data["time"]
        originalMsg = data["content"][1:]
#                    print msg.originalMsg
        msg = self.__mergeMsg(originalMsg)
        result = {"Event": message.TempMsg.EVENT_NAME,
                  "Data": {"Sender": uin, "Message": msg, "SendTime": data["time"]}}
        return result

    def handle_logout(self):
        self.online = False
        self.msg_pool.put([self.__make_event_dic(events.LOGOUT, u"掉线了")])

    def __mergeMsg(self, msg):
        result = ""
        for i in msg:
            if isinstance(i, list):
                continue
            else:
                result += i
        return result.strip()

    def getGroupByUin(self, uin):
        """
        @param uin: 群号
        @rtype: entity.Group实例
        """
        for i in range(6):
            # self.qq_user.groups.get(uin)
            group = self.qq_user.groups.get(uin)
            if group:
                return group
            else:
                self.__get_groups()

    def __get_msg(self):
        try:
            dic = self.getMsg()
            try:
                self.logger.info(str(dic))
            except:
                pass
        except:
            # traceback.print_exc()
            self.get_msg_failed_count += 1
            if self.get_msg_failed_count >= 2:
                self.handle_logout()
                self.get_msg_failed_count = 0
            return
        # print __file__, dic
        resultDic = []
        if 0 != dic["retcode"] or not isinstance(dic["result"], list):
            return
        if dic["retcode"] in self.logout_codes:
            self.handle_logout()
            return
        for i in dic["result"]:
            msgDic = {"SendTime": time.time(), "Event": "others", "Data": {}}  # 根据下面的分析生成
            # print i["poll_type"]
            handler = self.msg_handlers.get(i["poll_type"])
            # print "handler", handler
            if handler:
                handle_result = handler(i)
                if handle_result:
                    msgDic.update(handle_result)
            resultDic.append(msgDic)
        self.msg_pool.put(resultDic)

    def get_msg(self):
        msgs = self.msg_pool.get()
        # print __file__, msgs
        return Response(OK, msgs)

    def run(self):
        while True:
            # print self.online
            if self.online:
                try:
                    self.__get_msg()
                except Exception, e:
                    traceback.print_exc()

    def sendMsg2Buddy(self, buddyId, content, fontStyle=None):
        data = super(QQClient, self).sendMsg2Buddy(buddyId, content, fontStyle)
        # print data
        return Response(OK, "ok")

    def sendMsg2Group(self, groupId, content, fontStyle=None):
        data = super(QQClient, self).sendMsg2Group(groupId, content, fontStyle)
        return Response(OK, "ok")

    def deleteGroupMember(self, group_number, qq_number):
        res = super(QQClient, self).deleteGroupMember(group_number, qq_number)
        code = res
        res_code = ERROR
        if code == 0:
            result = u"删除成功"
            res_code = OK
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
        return Response(res_code, result)

    def allowAddFriend(self, qq, reject_reason, allow=True):
        super(QQClient, self).allowAddFriend(qq, reject_reason, allow)
        return Response(OK, "ok")

    def handleAddGroupMsg(self, req_uin, group_uin, msg="", allow=True):
        super(QQClient, self).handleAddGroupMsg(req_uin, group_uin, msg, allow)
        return Response(OK, "ok")
