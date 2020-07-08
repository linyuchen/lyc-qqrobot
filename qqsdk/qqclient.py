# coding=UTF8
from qqsdk import entity


class QQClientBase:
    def __init__(self):

        self.qq_user = entity.QQUser(friends=[], groups=[])
        self.online = True

    def send_msg(self, qq: str, content: str, is_group=False):
        """
        # qq: 好友或陌生人或QQ群号
        # content: 要发送的内容，unicode编码
        """
        raise NotImplementedError

    def get_friends(self):
        """
        获取好友，结果将放在self.qq_user.friends里面
        """

    def get_groups(self):
        """
        结果保存在 self.qq_user.groups
        """

