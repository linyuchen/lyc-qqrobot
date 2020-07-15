from nonebot.message import MessageSegment
from qqsdk.message import MsgHandler, GroupMsg
from .randomimg import random_img
from ..cmdaz import CMD


class RandomImg(MsgHandler):
    bind_msg_types = (GroupMsg, )

    def __init__(self, qq_client):
        super(RandomImg, self).__init__(qq_client)

    def handle(self, msg: GroupMsg):
        print(msg)
        if CMD("冲").az(msg.msg):
            img_path = random_img()
            print(img_path)
            reply_msg = MessageSegment.image("file://" + img_path)
            print(self.qq_client)
            msg.reply(reply_msg)
