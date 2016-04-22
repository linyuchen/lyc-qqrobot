# -*- coding: UTF8 -*-

import json
import math
import urllib2
import requests
# import requests


class QQApi(object):
    """
    buddyId: 如果是WebQQ，就是uin
        如果是PCQQ，就是QQ号
    """

    def __init__(self, port):
        self.verifyCode = ""  # 验证码
        self.needVerifyCode = False
        # self.http = requests  # .session()
        self.headers = {"Content-Type": "application/json"}
        # port = 6666
        self.host = "http://localhost:%d" % port
        self.login_url = "%s/login" % self.host
        self.input_vc_url = self.host + "/input_vc"
        self.get_friends_url = self.host + "/friends"
        self.get_groups_url = self.host + "/groups"
        self.get_msgs_url = self.host + "/msgs"
        self.uin2number_url = self.host + "/uin2number"
        self.send_msg2buddy_url = self.host + "/send_msg2buddy"
        self.send_msg2group_url = self.host + "/send_msg2group"
        self.delete_group_member_url = self.host + "/delete_group_member"
        self.handle_request_add_me_friend_url = self.host + "/handle_request_add_me_friend"
        self.handle_request_join_group_url = self.host + "/handle_request_join_group"

    def post_json(self, url, **kwargs):
        # req = urllib2.Request(url, data=json.dumps(kwargs), headers=self.headers)
        # http.headers = self.headers
        res = requests.get(url, kwargs)
        return res.json()

    def uin2number(self, uin):
        return self.post_json(self.uin2number_url, uin=uin)

    def getMyInfo(self):

        pass

    def login(self):

        self.online = True
        data = self.post_json(self.login_url)
        return data

    def inputVerifyCode(self, code):
        """
        @param code:验证码
        """
        data = self.post_json(self.input_vc_url, vc=code)
        return data

    def logout(self):
        """
        @return: 是否登出成功
        @rtype: bool
        """

    def getFriends(self):
        """
        获取好友列表
        {"data":{uin: {"uin": QQ临时号码, "groupId": 分组ID, "groupName": 分组名, "markName": 备注,
        "nick": 昵称}, ...}
        }
        """
        return self.post_json(self.get_friends_url)

    def getGroups(self):
        """
        获取群列表
        {群uin: 
            {"uin": uin, "name": 群名, "mask": 群消息接收屏蔽设置, "members": {群成员uin:{"nick": 昵称, "isAdmin": 是否管理员, "status": 在线状态, "card": 群名片, "uin": uin, "isCreator": 是否群主},...}}, ...
        }
        """
        return self.post_json(self.get_groups_url)

    def getMsg(self):
        """
        获取消息
        好友消息: {"Event": "FriendMsg", "Data": {"Sender": uin, "SendTime": 消息时间, "Message": 消息内容}}
        群消息: {"Event": "GroupMsg", "Data": {"GroupQQ": 群号, "ClusterNum": uin, "Sender": member_uin, "SenderQQ": member_qq, "Message": 消息内容, "SendTime": 发送时间}}
        """
        data = self.post_json(self.get_msgs_url)
        return data

    def sendTempMsgFromGroup(self, groupId, buddyId, content, fontStyle=None):
        """
        groupId: 群id
        buddyId: 对方id
        content: 要发送的内容，Unicode编码
        fontStyle: entity.FontStyle
        """


    def inputVerifyCode(self,code):
        """
        @param code:验证码
        验证码在当前目录下
        """

        self.verifyCode = code
        self.needVerifyCode = False
        return self.post_json(self.input_vc_url, vc=code)

    def sendMsg2Buddy(self, buddyId, content, fontStyle=None):
        """
        :param buddyId: 好友的id
        :param content: 要发送的内容，unicode编码
        """
        # print u"发送消息的对象uin",buddyId
        return self.post_json(self.send_msg2buddy_url, uin=buddyId, msg=content)


    def sendMsg2Group(self, groupId, content, fontStyle=None):
        """
        groupId:群的id
        content: 要发送的内容, unicode编码
        fontStyle: entity.FontStyle
        """
        # print groupId
        max_length = 600
        num = math.ceil(len(content) / float(600))
        for i in range(int(num)):
            msg = content[i * max_length: (i + 1) * max_length]
            self.post_json(self.send_msg2group_url, uin=groupId, msg=msg)

    def handleRequestAddMeFriend(self, qq, rejectReason="", allow=True):
        """
        处理别人加我为好友消息
        :param qq: 申请加我好友的人的QQ
        :param msg: 拒绝理由
        :param allow: 是否同意
        :return: dict
        """
        res = self.post_json(self.handle_request_add_me_friend_url, qq=qq, reject_reason=rejectReason, allow=allow)
        return res


    def handleAddGroupMsg(self,buddyId, groupId, rejectReason="",allow = True):
        """
        :param buddyId:
        :param groupId:
        :param rejectReason: 拒绝的理由, unicode编码
        :param allow: 是否同意
        """
        res = self.post_json(self.handle_request_join_group_url,
                             member=buddyId, group=groupId, reject_reason=rejectReason, allow=allow)
        return res

    def deleteGroupMember(self, group_number, qq_number):
        """
        @return 
            成功
            成员不存在
            权限不足
            群号错误
            网络错误
        """
        return self.post_json(self.delete_group_member_url, group=group_number, member=qq_number)["data"]


if __name__ == "__main__":
    test = QQApi(3000)
    # print test.login()["data"]
    # print test.inputVerifyCode("knke")["data"]
    # print test.getFriends()
    # print test.sendMsg2Buddy("2725528563", u"呵呵")
    # import time
    print test.getMsg()
