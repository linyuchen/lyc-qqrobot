# coding=UTF8
import basemsg
BaseMsg = basemsg.BaseMsg


class AddFriendResultMsg(BaseMsg):
    """
    加别人好友得到的结果
    self.qq: int, 对方QQ
    self.name: string, 对方昵称
    self.msg: string, 消息结果
    """

    def __init__(self, qq, name):

        super(AddFriendResultMsg, self).__init__()
        self.qq = qq
        self.name = name
