from qqsdk.message import MsgHandler, GroupMsg
from qqsdk.message.segment import MessageSegment
from .randomimg import random_img
from ..cmdaz import CMD
from ..superplugins import GroupPointAction


class RandomImg(MsgHandler):
    bind_msg_types = (GroupMsg, )

    def __init__(self, qq_client):
        super(RandomImg, self).__init__(qq_client)
        self.once_point = 50  # 调用一次所需活跃度
        self.group_point_action = GroupPointAction()

    def handle(self, msg: GroupMsg):
        for cmd_name in ["冲", "冲冲冲", "来点色图", "来点涩图"]:
            if CMD(cmd_name).az(msg.msg):
                if self.group_point_action.get_point(msg.group.qq, msg.group_member.qq) < self.once_point:
                    return msg.reply(f"【{msg.group_member.get_name()}】的活跃度不足{self.once_point}")
                img_path = random_img()
                reply_msg = MessageSegment.image_path(img_path)
                msg.reply(reply_msg)
                self.group_point_action.add_point(msg.group.qq, msg.group_member.qq, -self.once_point)
