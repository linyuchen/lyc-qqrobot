# coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg


class AddedMeFriendMsg(BaseMsg):
    """
    对方已经添加了我为好友
    self.friend: Friend实例
    """

    def __init__(self, friend):

        super(AddedMeFriendMsg, self).__init__()
        self.friend = friend


class RequestAddMeFriend(BaseMsg):

    """
    对方请求添加我为好友
    要在两分钟内处理此消息，否则将被销毁
    self.requestQQ: int
    self.msg: string, 对方填的验证消息
    """
    EVENT_NAME = "RequsetAddMeFriend"

    def __init__(self, requestQQ):

        super(RequestAddMeFriend, self).__init__()
        self.requestQQ = requestQQ

    def allow(self):
        """
        同意
        :return:
        """
    def reject(self, reason):
        """
        拒绝
        :param reason: 拒绝理由
        :return:
        """
