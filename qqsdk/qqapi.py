# -*- coding: UTF8 -*-

import json
import time
import math
import requests


class QQApi(object):
    """
    buddyId: 如果是WebQQ，就是uin
        如果是PCQQ，就是QQ号
    """

    def __init__(self, port, host="localhost"):
        self.verifyCode = ""  # 验证码
        self.needVerifyCode = False
        self.port = port
        # self.http = requests  # .session()
        self.headers = {"Content-Type": "application/json"}
        # port = 6666
        self.host = "http://%s:%d" % (host, port)
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

    @staticmethod
    def post_json(self, url: str, **kwargs) -> dict:
        res = requests.get(url, kwargs)
        res = res.content
        try:
            return json.loads(res)
        except:
            return {}

    def uin2number(self, uin: str) -> str:
        """

        :param uin:
        :return: {data: qq}
        """
        return self.post_json(self.uin2number_url, uin=uin)

    def get_my_info(self):

        pass

    def login(self):

        self.online = True
        data = self.post_json(self.login_url)
        return data

    def logout(self):
        """
        @return: 是否登出成功
        @rtype: bool
        """

    def get_friends(self):
        """
        获取好友列表
        {"data":{"uin号码": {"uin": QQ临时号码, "groupId": 分组ID, "groupName": 分组名, "markName": 备注,
        "nick": 昵称}}
        }
        """
        return self.post_json(self.get_friends_url)

    def get_groups(self):
        """
        获取群列表
        {
        "data":
            {"群uin号码":
                {"uin": uin, "name": 群名, "mask": 群消息接收屏蔽设置, "members": {群成员uin:{"nick": 昵称, "isAdmin": 是否管理员, "status": 在线状态, "card": 群名片, "uin": uin, "isCreator": 是否群主},...}}, ...
            }
        }
        """
        return self.post_json(self.get_groups_url)

    def get_msg(self):
        """
        获取消息
        好友消息: {data: [{"Event": "FriendMsg", "Data": {"Sender": uin, "SendTime": 消息时间, "Message": 消息内容}},...]}
        群消息: {data: [{"Event": "GroupMsg", "Data": {"GroupQQ": 群号, "ClusterNum": uin, "Sender": member_uin, "SenderQQ": member_qq, "Message": 消息内容, "SendTime": 发送时间}},...]}
        SendTime是时间戳, uin 都是int型
        """
        data = self.post_json(self.get_msgs_url)
        return data

    def send_temp_msg_from_group(self, groupId: str, buddyId: str, content: str, fontStyle=None):
        """
        groupId: 群id
        buddyId: 对方id
        content: 要发送的内容，Unicode编码
        fontStyle: entity.FontStyle
        """

    def input_verify_code(self, code: str):
        """
        @param code:验证码
        验证码在当前目录下
        """

        self.verifyCode = code
        self.needVerifyCode = False
        return self.post_json(self.input_vc_url, vc=code)

    def __convertMsg(self, content: str) -> str:
        if self.port >= 3000:
            content = content.replace("\\","\\\\").replace("\r\n","\n").replace("\n","\\n").replace("\"","\\\"").replace("\t","\\t")

        return content

    def __split_send_msg(func):
        def send(self, receiverId, content, fontStyle=None):
            content = self.__convertMsg(content)
            max_length = 300
            num = math.ceil(len(content) / float(max_length))
            for i in range(int(num)):
                msg = content[i * max_length: (i + 1) * max_length]
                func(self, receiverId, msg, fontStyle)
                time.sleep(0.8)

        return send


    @__split_send_msg
    def send_buddy_msg(self, buddyId: str, content: str, fontStyle=None) -> dict:
        """
        :param buddyId: 好友的id
        :param content: 要发送的内容，unicode编码
        ?uin=buddyId&msg=content
        """
        # print u"发送消息的对象uin",buddyId
        return self.post_json(self.send_msg2buddy_url, uin=buddyId, msg=content)


    @__split_send_msg
    def send_group_msg(self, groupId: str, content: str, fontStyle=None) -> dict:
        """
        groupId:群的id
        content: 要发送的内容, unicode编码
        fontStyle: entity.FontStyle
        ?uin=groupId&msg=content
        """
        # print groupId
        return self.post_json(self.send_msg2group_url, uin=groupId, msg=content)

    def handle_request_new_friend(self, qq:str, rejectReason:str= "", allow:bool=True) -> dict:
        """
        处理别人加我为好友消息
        :param qq: 申请加我好友的人的QQ
        :param msg: 拒绝理由
        :param allow: 是否同意
        :return: dict
        """
        res = self.post_json(self.handle_request_add_me_friend_url, qq=qq, reject_reason=rejectReason, allow=allow)
        return res

    def handle_add_group_msg(self, buddyId, groupId, rejectReason="", allow = True):
        """
        处理加群消息
        :param buddyId:
        :param groupId:
        :param rejectReason: 拒绝的理由, unicode编码
        :param allow: 是否同意
        """
        res = self.post_json(self.handle_request_join_group_url,
                             member=buddyId, group=groupId, reject_reason=rejectReason, allow=allow)
        return res

    def delete_group_member(self, group_number: str, qq_number: str):
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
    test = QQApi(1000, "localhost")
    # test = QQApi(3004)
    # print test.login()["data"]
    # print test.inputVerifyCode("knke")["data"]
    print(test.get_friends())
    # print test.getGroups()
    print(test.send_buddy_msg("1412971608", u"1\n\t" * 200))
    # import time
    # msg = test.getMsg()
    # print msg
    # print msg["data"][0]["Data"]["Message"]
