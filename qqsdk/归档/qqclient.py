# -*-coding: UTF8-*-


import threading
import time
import traceback
from queue import Queue

from qqsdk import entity
from qqsdk import message
from qqsdk import eventlistener
from qqsdk.归档 import events
from qqsdk.归档.qqapi import QQApi

EventListener = eventlistener.EventListener


class QQClient(threading.Thread, QQApi):
    """
    self.loginSucCount: int, 登录成功的次数

    需要自己封装获取的消息，详情见__analysisMsg
    """

    def __init__(self, port, host):

        threading.Thread.__init__(self)
        QQApi.__init__(self, port, host)
        self.interval = 1.0
        self.qqUser = entity.QQUser()
        self.__qq_numbers = {}
        self.msg_handlers = {
            events.ERROR: self.addErrorMsg,
            events.LOGIN_SUCCESS: self.__handle_login_success,
            events.LOGOUT: self.__handle_logout,
            events.FRIEND_VOICE: self.__handle_friend_voice_msg,
            events.FRIEND_VIBRATION: self.__handle_friend_bration_msg,
            events.TEMP_MSG: self.__handle_temp_msg,
            events.DISCUSSION_GROUP_MSG: self.__handle_discussion_msg,
            events.FRIEND_STATUS_CHANGED: self.__handle_friend_status_changed_msg,
            events.FRIEND_SIGNATURE_CHANGED: self.__handle_friend_signature_msg,
            events.GROUP_MEMBER_CARD_CHANGED: self.__handle_group_member_card_changed_msg,
            events.REQUEST_JOIN_GROUP: self.__handle_request_join_group_msg,
            events.INVITED_TO_GROUP: self.__handle_invited_to_group_msg,
            events.REQUSET_ADD_ME_FRIEND: self.__handle_request_add_me_friend_msg,
            events.FRIEND_INPUTING: self.__handle_friend_inputing_msg,
            events.GROUP_ADMIN_CHANGED: self.__handle_group_admin_changed_msg,
            events.ADDED_ME_FRIEND: self.__handle_added_me_friend_msg,
            events.NEW_MEMBER_JOINED_GROUP: self.__handle_new_member_joined_group_msg,
            events.NEED_VC: self.__handle_need_verify_code_msg,
            events.GROUP_MEMBER_REMOVED: self.__handle_group_member_removed_msg,
            events.ADD_FRIEND_RESULT: self.__handle_add_friend_result_msg,
            events.FRIEND_MSG: self.__handle_friend_msg,
            events.GROUP_MSG: self.__handle_group_msg,
            events.GROUP_MEMBER_EXIT: self.__handle_group_member_exited_msg,
            events.LOGIN_FAILED: self.__handle_login_failed
        }
        self.online = True
#        self.__msgPool = []
        # events 列表,每个元素都是个MsgEvent实例
        self.groupMemberExitEvents = []
        self.newGroupMemberEvents = []
        self.groupAdminChangeEvents = []
        self.groupMsgEvents = []
        self.friendMsgEvents = []
        self.addedMeFiendEvents = []
        self.logoutEvents = []
        self.loginFailedEvents = []
        self.loginSuccessEvents = []
        self.needVerifyCodeEvents = []
        self.tempMsgEvents = []
        self.errorMsgEvents = []
        self.leaveGroupEvents = []
        self.friendStatusChangeEvents = []
        self.logMsgEvents = []
        self.sendBuddyEvents = []
        self.sendGroupEvents = []
        self.friendVoiceMsgEvents = []
        self.friendVibrationMsgEvents = []
        self.discussionGroupMsgEvents = []
        self.friendSignatureChangedEvents = []
        self.groupMemberCardChangedEvents = []
        self.friendInputingEvents = []
        self.groupRemoveMemberEvents = []
        self.meJoinedGroupEvents = []
        self.inviteMeToGroupEvents = []
        self.requestJoinGroupEvents = []
        self.requestAddMeFriendEvents = []
        self.addFriendResultEvents = []

        # msgs 列表，每个元素都是个message实例
        self.__groupMemberExitMsgs = Queue.Queue()
        self.__addFriendResultMsgs = Queue.Queue()
        self.__requestAddMeFriendMsgs = Queue.Queue()
        self.__requestJoinGroupMsgs = Queue.Queue()
        self.__inviteMeToGroupMsgs = Queue.Queue()
        self.__meJoinedGroupMsgs = Queue.Queue()
        self.__groupRemoveMemberMsgs = Queue.Queue()
        self.__friendInputingMsgs = Queue.Queue()
        self.__friendSignatureChangedMsgs = Queue.Queue()
        self.__discussionGroupMsgs = Queue.Queue()
        self.__friendVibrationMsgs = Queue.Queue()
        self.__needVerifyCodeMsgs = Queue.Queue()
        self.__loginSuccessMsgs = Queue.Queue()
        self.__loginFailedMsgs = Queue.Queue()
        self.__logoutMsgs = Queue.Queue()
        self.__addedMeFiendMsgs = Queue.Queue()
        self.__friendMsgs = Queue.Queue()
        self.__groupMsgs = Queue.Queue()
        self.__groupAdminChangeMsgs = Queue.Queue()
        self.__newGroupMemberMsgs = Queue.Queue()
        self.__tempMsgs = Queue.Queue()
        self.__leaveGroupMsgs = Queue.Queue()
        self.__friendStatusChangeMsgs = Queue.Queue()
        self.__friendVoiceMsgs = Queue.Queue()
        self.__groupMemberCardChangedMsgs = Queue.Queue()

        # 发出的消息过滤器
        self.__sendMsgFilter = []

        # log消息

        self.__logMsgs = Queue.Queue()
        self.__sendBuddyMsgs = Queue.Queue()
        self.__sendGroupMsgs = Queue.Queue()
        self.__errorMsgs = Queue.Queue()

        #

        self.__eventListen = True

        self.loginSucCount = 0  # 登录成功次数

        self.sendMsgFuncPool = Queue.Queue()

        threading.Thread(target=self.__startSendMsgFuncPool).start()
        self.__startListenEventsBeforLogin()
        self.__startListenEventsAfterLogin()
        try:
            self.getFriends()
            self.getGroups()
        except:
            traceback.print_exc()

    def addErrorMsg(self, data):
        """
        :data: Unicode， 错误描述
        """

        try:
            msg = message.ErrorMsg()
            msg.msg = data
            self.__errorMsgs.put(msg)
        except:
            traceback.print_exc()

    def addLogMsg(self, msgContent):

        logMsg = message.BaseMsg()
        logMsg.time = time.time()
        logMsg.msg = msgContent
        self.__logMsgs.put(logMsg)

    def addFriendMsg(self, msg):

        self.__friendMsgs.put(msg)

    def clearSendMsgFilter(self):

        del self.__sendMsgFilter[:]

    def clearEvents(self):
        """
        清空events
        """
        del self.addFriendResultEvents[:]
        del self.discussionGroupMsgEvents[:]
        del self.newGroupMemberEvents[:]
        del self.groupAdminChangeEvents[:]
        del self.groupMsgEvents[:]
        del self.groupRemoveMemberEvents[:]
        del self.groupMemberCardChangedEvents[:]
        del self.friendMsgEvents[:]
        del self.friendVoiceMsgEvents[:]
        del self.friendVibrationMsgEvents[:]
        del self.friendStatusChangeEvents[:]
        del self.friendSignatureChangedEvents[:]
        del self.friendInputingEvents[:]
        del self.addedMeFiendEvents[:]
        del self.logoutEvents[:]
        del self.loginFailedEvents[:]
        del self.loginSuccessEvents[:]
        del self.needVerifyCodeEvents[:]
        del self.tempMsgEvents[:]
        del self.errorMsgEvents[:]
        del self.leaveGroupEvents[:]
        del self.logMsgEvents[:]
        del self.sendBuddyEvents[:]
        del self.sendGroupEvents[:]
        del self.inviteMeToGroupEvents[:]
        del self.requestAddMeFriendEvents[:]
        del self.requestJoinGroupEvents[:]
        del self.meJoinedGroupEvents[:]

    def addSendMsgFilter(self, msgFilter):
        """
        :msgFilter: MsgFilter实例
        """

        self.__sendMsgFilter.append(msgFilter)

    def __addEvent(self, msgEvent, eventList):

        """
        """
        msgEvent.setupQQInstance(self)
        eventList.append(msgEvent)

    def addGroupMemberExitEvent(self, msgEvent):
        """
        添加处理有人退群的事件
        """
        self.__addEvent(msgEvent, self.groupMemberExitEvents)

    def addInviteMeToGroupEvent(self, msgEvent):

        """
        添加审核有人邀请我入群的事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.inviteMeToGroupEvents)

    def addMeJoinedGroupEvent(self, msgEvent):
        """
        添加处理我成功加入一个群的事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.meJoinedGroupEvents)

    def addGroupRemoveMemberEvent(self, msgEvent):
        """
        添加处理群成员被移出群的事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.groupRemoveMemberEvents)

    def addfriendInputingEvent(self, msgEvent):
        """
        添加处理好友正在输入的事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.friendInputingEvents)

    def addGroupMemberCardChangedEvent(self, msgEvent):
        """
        添加群员群名片改变的处理事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.groupMemberCardChangedEvents)

    def addFriendSignatureChangedEvent(self, msgEvent):
        """
        添加好友个性签名改变的处理事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.friendSignatureChangedEvents)

    def addDiscussionGroupMsgEvent(self, msgEvent):
        """
        添加处理讨论组消息的事件
        """

        self.__addEvent(msgEvent, self.discussionGroupMsgEvents)

    def addFriendVibrationEvent(self, msgEvent):
        """
        添加处理好友抖动的事件
        """
        self.__addEvent(msgEvent, self.friendVibrationMsgEvents)


    def addSendBuddyEvent(self, msgEvent):
        """
        添加处理发送buddy消息（好友，临时）的事件
        """
        self.__addEvent(msgEvent, self.sendBuddyEvents)

    def addSendGroupEvent(self, msgEvent):
        """
        添加处理发送群消息的事件
        """
        self.__addEvent(msgEvent, self.sendGroupEvents)

    def addFriendVoiceMsgEvent(self, msgEvent):
        """
        添加处理好友语音消息事件
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.friendVoiceMsgEvents)

    def addLogMsgEvent(self, msgEvent):
        """
        添加处理log信息的事件
        """
        self.__addEvent(msgEvent, self.logMsgEvents)

    def addErrorMsgEvent(self,msgEvent):
        """
        添加处理错误信息的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.errorMsgEvents)

    def addTempMsgEvent(self,msgEvent):
        """
        添加处理临时会话的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.tempMsgEvents)


    def addNewGroupMemberEvent(self, msgEvent):
        """
        添加有群员已经入群的处理事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.newGroupMemberEvents)


    def addRequestJoinGroupEvent(self, msgEvent):
        """
        添加处理新成员申请入群的事件，只有自己是管理才能收到此消息
        :param msgEvent:
        :return:
        """
        self.__addEvent(msgEvent, self.requestJoinGroupEvents)

    def addGroupAdminChangeEvent(self,msgEvent):
        """
        添加处理管理员变更的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.groupAdminChangeEvents)

    def addGroupMsgEvent(self,msgEvent):
        """
        添加处理群消息的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.groupMsgEvents)

    def addNeedVerifyCodeEvent(self,msgEvent):
        """
        添加处理需要验证码的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.needVerifyCodeEvents)

    def addLoginSuccessEvent(self,msgEvent):
        """
        添加处理登录成功的事件
        msgEvent: MsgEvent实例
        """

        self.__addEvent(msgEvent, self.loginSuccessEvents)

    def addLoginFailedEvent(self,msgEvent):
        """
        添加处理登录失败的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.loginFailedEvents)

    def addLogoutEvent(self,msgEvent):
        """
        添加处理掉线或者登出的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.logoutEvents)

    def addAddedMeFiendEvent(self,msgEvent):
        """
        添加处理别人加我好友的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.addedMeFiendEvents)

    def addFriendMsgEvent(self,msgEvent):
        """
        添加处理好友消息的事件
        msgEvent: MsgEvent实例
        """
        self.__addEvent(msgEvent, self.friendMsgEvents)

    def addLeaveGroupEvent(self,msgEvent):
        """
        添加我被踢出群事件
        """
        self.__addEvent(msgEvent, self.leaveGroupEvents)

    def addFriendStatusChangeEvent(self,msgEvent):
        """
        添加好友状态改变事件
        """
        self.__addEvent(msgEvent, self.friendStatusChangeEvents)

    def __startListenEventsBeforLogin(self):


        self.__listenEvent(self.__needVerifyCodeMsgs, self.needVerifyCodeEvents)
#        thread.start_new_thread(self.__listenEvent,(self.__loginSuccessMsgs, self.loginSuccessEvents))
        self.__listenEvent(self.__loginFailedMsgs, self.loginFailedEvents)
        self.__listenEvent(self.__errorMsgs, self.errorMsgEvents)

    def __startListenEventsAfterLogin(self):

        self.__listenEvent(self.__addedMeFiendMsgs, self.addedMeFiendEvents)
        self.__listenEvent(self.__friendMsgs, self.friendMsgEvents)
        self.__listenEvent(self.__logoutMsgs, self.logoutEvents)
        self.__listenEvent(self.__groupMsgs, self.groupMsgEvents)
        self.__listenEvent(self.__groupAdminChangeMsgs, self.groupAdminChangeEvents)
        self.__listenEvent(self.__newGroupMemberMsgs, self.newGroupMemberEvents)
        self.__listenEvent(self.__tempMsgs, self.tempMsgEvents)
        self.__listenEvent(self.__leaveGroupMsgs, self.leaveGroupEvents)
        self.__listenEvent(self.__friendStatusChangeMsgs, self.friendStatusChangeEvents)
        self.__listenEvent(self.__logMsgs, self.logMsgEvents)
        self.__listenEvent(self.__sendBuddyMsgs, self.sendBuddyEvents)
        self.__listenEvent(self.__sendGroupMsgs, self.sendGroupEvents)
        self.__listenEvent(self.__friendVoiceMsgs, self.friendVoiceMsgEvents)
        self.__listenEvent(self.__friendVibrationMsgs, self.friendVibrationMsgEvents)
        self.__listenEvent(self.__friendInputingMsgs, self.friendInputingEvents)
        self.__listenEvent(self.__discussionGroupMsgs, self.discussionGroupMsgEvents)
        self.__listenEvent(self.__friendSignatureChangedMsgs, self.friendSignatureChangedEvents)
        self.__listenEvent(self.__groupMemberCardChangedMsgs, self.groupMemberCardChangedEvents)
        self.__listenEvent(self.__inviteMeToGroupMsgs, self.inviteMeToGroupEvents)
        self.__listenEvent(self.__groupRemoveMemberMsgs, self.groupRemoveMemberEvents)
        self.__listenEvent(self.__meJoinedGroupMsgs, self.meJoinedGroupEvents)
        self.__listenEvent(self.__requestJoinGroupMsgs, self.requestJoinGroupEvents)
        self.__listenEvent(self.__requestAddMeFriendMsgs, self.requestAddMeFriendEvents)
        self.__listenEvent(self.__addFriendResultMsgs, self.addFriendResultEvents)
        self.__listenEvent(self.__groupMemberExitMsgs, self.groupMemberExitEvents)

    def __listenEvent(self, msgs, events):

        e = EventListener(msgs, events, self.addErrorMsg, self.interval, qq_client=self)
        e.start()

    def __analysisMsg(self, msg):
        """
        分析消息，把消息压入消息池
        """

        for msgDic in msg.get("data", []):
            self.__handleMsg(msgDic)

    def __handle_friend_voice_msg(self, data):
        qq = data["Sender"]
        voiceUrl = data["Url"]
        friend = self.getFriendByUin(qq)
        if not friend:
            return
        msg = message.FriendVoiceMsg(friend, voiceUrl)
        msg.time = data["SendTime"]
        self.__friendVoiceMsgs.put(msg)

    def __handle_friend_bration_msg(self, data):
        qq = data["Sender"]
        friend = self.getFriendByUin(qq)
        if not friend:
            return
        msg = message.FriendMsg(friend)
        msg.time = data["SendTime"]
        self.__friendVoiceMsgs.put(msg)

    def __handle_temp_msg(self, data):
        qq = data["Sender"]
        groupQQ = data["ClusterNum"]
        msg = message.TempMsg()
        msg.group = None
        if groupQQ:
            group = self.getGroupByUin(groupQQ)
            if not group:
                return
            msg.group = group
        msg.qq = qq
        msg.time = data["SendTime"]
        msg.msg = data["Message"]
        self.__tempMsgs.put(msg)

    def __handle_discussion_msg(self, data):
        msg = message.DiscussionGroupMsg(data["Sender"], data["SendName"], data["ClusterId"])
        msg.msg = data["Message"]
        msg.time = data["SendTime"]
        self.__discussionGroupMsgs.put(msg)

    def __handle_friend_status_changed_msg(self, data):
        qq = data["Sender"]
        friend = self.getFriendByUin(qq)
        if not friend:
            return
        friend.status = data["QQStatus"]
        msg = message.FriendStatusChangeMsg(friend)
        self.__friendStatusChangeMsgs.put(msg)

    def __handle_friend_signature_msg(self, data):
        qq = data["Sender"]
        friend = self.getFriendByUin(qq)
        if not friend:
            return
        msg = message.FriendSignatureChangedMsg(friend)
        msg.time = data["SendTime"]
        msg.msg = data["Message"]
        self.__friendSignatureChangedMsgs.put(msg)

    def __handle_group_member_card_changed_msg(self, data):
        groupQQ = data["ClusterNum"]
        groupMemberQQ = data["Sender"]
        group = self.getGroupByUin(groupQQ)
        if not group:
            return
        groupMember = self.getGroupMemberByUin(groupQQ, groupMemberQQ)
        groupMember.card = data["Card"]
        msg = message.GroupMemberCardChangedMsg(group, groupMember, data["SendName"])
        msg.time = data["SendTime"]

    def __handle_request_join_group_msg(self, data):
        group = self.getGroupByUin(data["ClusterNum"])
        if not group:
            return
        msg = message.RequestJoinGroupMsg(group, data["Sender"], data["Message"])
        msg.requestName = data["SendName"]
        msg.allow = lambda reqQQ=data["Sender"], groupQQ=group.qq: self.handleAddGroupMsg(reqQQ, groupQQ)
        msg.reject = lambda reason, reqQQ=data["Sender"], groupQQ=group.qq: self.handleAddGroupMsg(reqQQ, groupQQ, reason, False)
        self.__requestJoinGroupMsgs.put(msg)

    def __handle_invited_to_group_msg(self, data):
        """
        被邀请入群
        """
        msg = message.InviteMeToGroupMsg(data["ClusterNum"], data["ClusterName"], data["Sender"], data["SendName"])
        msg.time = data["SendTime"]
        msg.allow = lambda groupQQ=data["ClusterNum"]: self.handleInviteMeToGroupMsg(groupQQ)
        msg.reject = lambda reason, groupQQ=data["ClusterNum"]: self.handleInviteMeToGroupMsg(groupQQ, reason, False)
        self.__inviteMeToGroupMsgs.put(msg)

    def __handle_request_add_me_friend_msg(self, data):
        """
        请求加我为好友
        """

        requestQQ = data["Sender"]
        msg = message.RequestAddMeFriendMsg(requestQQ)
        msg.allow = lambda qq=requestQQ: self.handleRequestAddMeFriend(qq)
        msg.reject = lambda reason, qq=requestQQ: self.handleRequestAddMeFriend(qq, reason, False)
        self.__requestAddMeFriendMsgs.put(msg)

    def __handle_friend_inputing_msg(self, data):
        """
        好友正在输入
        """
        qq = data["Sender"]
        friend = self.getFriendByUin(qq)
        if not friend:
            return
        msg = message.FriendMsg(friend)
        msg.time = data["SendTime"]
        self.__friendInputingMsgs.put(msg)

    def __handle_group_admin_changed_msg(self, data):
        """
        群管理变更
        """
        groupQQ = data["ClusterNum"]
        group = self.getGroupByUin(groupQQ)
        if not group:
            return
        groupMemberQQ = data["Sender"]
        groupMember = self.getGroupMemberByUin(groupQQ, groupMemberQQ)
        groupMember.isAdmin = data["IsSet"]
        msg = message.GroupAdminChangeMsg(group, groupMember)
        self.__groupAdminChangeMsgs.put(msg)

    def __handle_added_me_friend_msg(self, data):
        """
        有人已经添加了我为好友
        """
        friend = self.getFriendByUin(data["Sender"])
        if not friend:
            return
        msg = message.AddedMeFriendMsg(friend)
        msg.time = data["SendTime"]
        self.__addedMeFiendMsgs.put(msg)

    def __handle_new_member_joined_group_msg(self, data):
        """
        有人已经加入了群
        """
        groupQQ = data["ClusterNum"]
        group = self.getGroupByUin(groupQQ)

        if not group:
            return
        groupMember = self.getGroupMemberByUin(groupQQ, data["Sender"])

        msg = message.NewGroupMemberMsg(group, groupMember)

        self.__newGroupMemberMsgs.put(msg)

    def __handle_need_verify_code_msg(self, data):
        qq = data["Sender"]
        msg = message.NeedVerifyCodeMsg(qq)
        msg.time = data["SendTime"]
        self.__needVerifyCodeMsgs.put(msg)

    def __handle_group_member_removed_msg(self, data):

        """
        有人被踢
        """
        groupQQ = data["ClusterNum"]
        group = self.getGroupByUin(groupQQ)
        if not group:
            return
        memberQQ = data["Sender"]
        memberName = data["SendName"]
        adminQQ = data["Operator"]
        groupAdmin = self.getGroupMemberByUin(groupQQ, adminQQ)
        msg = message.GroupRemoveMemberMsg(group, groupAdmin, memberQQ, memberName)
        self.__groupRemoveMemberMsgs.put(msg)

    def __handle_me_joined_group_msg(self, data):
        """
        我已经加入群
        """
        groupQQ = data["ClusterNum"]
        group = self.getGroupByUin(groupQQ)
        if not group:
            return

        adminQQ = data["Operator"]
        groupAdmin = self.getGroupMemberByUin(groupQQ, adminQQ)
        msg = message.MeJoinedGroupMsg(group, groupAdmin)
        self.__meJoinedGroupMsgs.put(msg)

    def __handle_add_friend_result_msg(self, data):
        """
        加别人好友的结果消息
        """
        msg = message.AddFriendResultMsg(data["Sender"], data["SendName"])
        msg.msg = data["Message"]
        msg.time = data["SendTime"]
        self.__addFriendResultMsgs.put(msg)

    def __handle_friend_msg(self, data):
        """
        好友消息
        """
        # print data
        friend = self.getFriendByUin(data["Sender"])
        if not friend:
            return
        msg = message.FriendMsg(friend)
        msg.time = data["SendTime"]
        msg.msg = data["Message"]
        # print "msg", msg.msg
        msg.reply = lambda content, fontStyle=None, qq=friend.uin: self.sendMsg2Buddy(qq, content)
        self.__friendMsgs.put(msg)

    def __handle_group_msg(self, data):
        """
        群消息
        """
#            print "收到群消息"
#         print data
        groupQQ = data["ClusterNum"]  # uin
        group = self.getGroupByUin(groupQQ)
        if not group:
            return
#            print group.qq
        group.qq = data["GroupQQ"]
        groupMember = self.getGroupMemberByUin(groupQQ, data["Sender"])
        groupMember.qq = data["SenderQQ"]
        msg = message.GroupMsg(group, groupMember, data["Message"])
        msg.time = data["SendTime"]
        msg.reply = lambda content, fontStyle=None, qq=group.uin: self.sendMsg2Group(qq, content)
        self.__groupMsgs.put(msg)

    def __handle_group_member_exited_msg(self, data):
        """
        有人退群
        """

        groupQQ = data["ClusterNum"]
        group = self.getGroupByUin(groupQQ)
        if not group:
            return
        memberName = data["SendName"]
        memberQQ = data["Sender"]
#            print group.qq
        msg = message.GroupMemberExitMsg(group, memberName, memberQQ)
        msg.time = data["SendTime"]
        self.__groupMemberExitMsgs.put(msg)

    def __handle_logout(self, data):
        """
        登出
        """
        self.online = False
        msg = message.BaseMsg()
        msg.msg = data
        self.__logoutMsgs.put(msg)

    def __handle_login_success(self, data):
        self.online = True
        msg = message.BaseMsg()
        msg.msg = data
        self.__loginSuccessMsgs.put(msg)

    def __handle_login_failed(self, data):
        self.online = False
        msg = message.BaseMsg()
        msg.msg = data
        self.__loginFailedMsgs.put(msg)

    def __handleMsg(self, msg):

        # dic = json.loads(msg)
        dic = msg
        """
        不管什么消息,都有以下键
            SendTime
            Event            
        """
        logMsg = "收到消息(全), " + msg
        # self.addLogMsg(logMsg)
        event = dic["Event"]
#        print "event", event, __file__
#         print dic
        data = dic.get("Data")
        event = self.msg_handlers.get(event)
        if event and data:
            event(data)
        else:
            pass
            # print(dic)

    def run(self):

        while True:
            time.sleep(self.interval)
            # print self.online
            if self.online:
                try:
                    msg = self.getMsg()
                    self.__analysisMsg(msg)

                except Exception:
                    msg = traceback.format_exc()
                    # print msg
                    self.addErrorMsg(msg)

    def getGroupByUin(self, uin):
        """
        @param uin: 群号
        @rtype: entity.Group实例
        """
        uin = int(uin)
        # print type(uin)
        # print uin
        for i in range(6):
            # self.qqUser.groups.get(uin)
            group = self.qqUser.groups.get(uin)
            # print self.qqUser.groups, uin, type(uin), type(self.qqUser.groups.keys()[0])
            if group:
                return group
            else:
                self.getGroups()

    def getFriendByUin(self, uin):
        """
        @param uin: qq号
        @rtype: entity.Friend实例
        """
        
        for i in range(1):
            if self.qqUser.friends.has_key(uin):
                friend = self.qqUser.friends[uin]
                if friend:
                    return friend
            else:
                self.getFriends()

    def __addSendBuddyMsg(self,buddyId,fontStyle,content):

        msg = message.SendBuddyMsg()
        msg.qq = buddyId
        msg.fontStyle = fontStyle
        msg.time = time.time()
        msg.content = content
        self.__sendBuddyMsgs.put(msg)
        logMsg = "发送消息给QQ:%d：%s"%(msg.qq,content)
        self.addLogMsg(logMsg)

    def __addSendGroupMsg(self, uin, fontStyle, content):

        msg = message.SendGroupMsg()
        group = self.getGroupByUin(uin)
        if not group:
            return
        msg.group = group
        msg.fontStyle = fontStyle
        msg.time = time.time()
        msg.content = content
        self.__sendGroupMsgs.put(msg)
        logMsg = "发送消息给群:%d：%s"%(msg.group.qq,content)
        self.addLogMsg(logMsg)

    def sendMsgFilter(self, msgContent):

        filterResult = True
        for f in self.__sendMsgFilter:
            filterResult = f.main(msgContent)
            if not filterResult:
                break

        return filterResult

    def __startSendMsgFuncPool(self):
        
        while True:
            # print self.online
            # if not self.online:
                # time.sleep(self.interval)
                # continue
            # print self.sendMsgFuncPool
            # st = time.clock()
            sendFunc = self.sendMsgFuncPool.get()
            try:
                # print sendFunc
                sendFunc()
            except Exception:
                # pass
                self.addErrorMsg(traceback.format_exc())
            # time.sleep(self.interval)

    def putFunc(self, func):
        """
        处理函数加入队列
        :param func:
        :return:
        """
        self.sendMsgFuncPool.put(func)

    def getGroupMemberByUin(self, groupUin, groupMemberUin):
        """
        @rtype: entity.GroupMember实例
        """

        group = self.getGroupByUin(groupUin)
        for i in range(6):  # 最多获取三次
            # print groupMemberUin, group.members, type(groupMemberUin), type(group.members.keys()[0])
            member = group.getMemberByUin(groupMemberUin)
            if not member:
                self.getGroups()
                group = self.getGroupByUin(groupUin)
            else:
                break
        return member

    def sendMsg2Buddy(self, buddyId, content, fontStyle=None):
        """
        # buddyId: 好友或陌生人的uin
        # content: 要发送的内容，unicode编码
        # fontStyle: entity.FontStyle
        """
        # print "sendmsg", buddyId

        if fontStyle:
            fontStyle = fontStyle.__str__()
        else:
            fontStyle = self.qqUser.fontStyle

        self.__addSendBuddyMsg(buddyId, fontStyle, content)

        self.sendMsgFuncPool.put(lambda qq=buddyId, c=content, f=fontStyle: QQApi.send_buddy_msg(self, qq, c, f))

    def sendMsg2Group(self, groupId, content, fontStyle=None):
        """
        groupId:群uin
        content: 要发送的内容, unicode编码
        fontStyle: entity.FontStyle实例
        """

        if fontStyle:
            fontStyle = fontStyle.__str__()
        else:
            fontStyle = self.qqUser.fontStyle
        # print groupId, content
        self.__addSendGroupMsg(groupId, fontStyle, content)

        self.sendMsgFuncPool.put(lambda qq=groupId, c=content, f=fontStyle: QQApi.send_group_msg(self, qq, c, f))

    # def api_sendMsg2Buddy(self, qq, content, fontstyle):
    #     QQApi.sendMsg2Buddy(self, qq, content)
    #
    # def api_sendMsg2Group(self, qq, contentu fontstyle):
    #     QQApi.sendMsg2Group(self, qq, content)

    def uin2number(self, uin):
        qq_number_dict = self.__qq_numbers
        # print uin
        if uin in qq_number_dict:
            return qq_number_dict[uin]
        qq = super(QQClient, self).uin2number(uin)["data"]
        # print type(qq)
        # print type(uin)
        # print qq
        if qq:
            qq_number_dict[uin] = qq
        return qq

    def getFriends(self):

        """
        获取好友，结果将放在self.qqUser.friends里面
            self.qqUser.friends是个dict，key是uin，value是entity.Friend实例
        """
        data = super(QQClient, self).getFriends()
        # print data
        for fuin, fobject_dict in data["data"].items():
            fobject = entity.Friend()
            fobject.get_qq = self.uin2number
            for fo_key, fo_value in fobject_dict.items():
                setattr(fobject, fo_key, fo_value)
            self.qqUser.friends[int(fuin)] = fobject
        # print self.qqUser.friends

    def getGroups(self):
        """
        结果保存在 self.qqUser.groups，self.qqUser.groups是个dict，key uin，value entity.Group实例
        """
        data = super(QQClient, self).getGroups()
        for guin, gobject_dict in data["data"].items():
            group_object = entity.Group()
            group_object.uin = guin
            group_object.name = gobject_dict["name"]
            group_object.mask = gobject_dict["mask"]
            for muin, m_dict in gobject_dict["members"].items():
                # print m_dict
                member = entity.GroupMember()
                member.get_qq = self.uin2number
                for m_key, m_value in m_dict.items():
                    setattr(member, m_key, m_value)
                group_object.members[member.uin] = member
            self.qqUser.groups[int(guin)] = group_object

        # print self.qqUser.groups


if __name__ == "__main__":

    test = QQClient()
