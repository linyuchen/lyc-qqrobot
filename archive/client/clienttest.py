from qqsdk import entity
from qqsdk.entity import Group, GroupMember
from qqsdk.message import GroupMsg
from qqsdk.message.segment import MessageSegment
from qqsdk.qqclient import QQClientBase

TEST_GROUP_QQ = "123"
TEST_GROUP_NAME = "test group"
TEST_GROUP_MEMBER_QQ = "379450326"
TEST_GROUP_MEMBER_NAME = "test"


class ClientTest(QQClientBase):
    def get_friends(self) -> list[entity.Friend]:
        pass

    def get_groups(self) -> list[entity.Group]:
        pass

    TEST_GROUP_MEMBER = GroupMember(qq=TEST_GROUP_MEMBER_QQ, nick=TEST_GROUP_MEMBER_NAME)
    TEST_GROUP = Group(qq=TEST_GROUP_QQ, name=TEST_GROUP_NAME,
                       members=[TEST_GROUP_MEMBER])

    def __init__(self):
        super().__init__()
        self.qq_user.groups.append(self.TEST_GROUP)

    def _send_msg(self, qq: str, content: str | MessageSegment, is_group=False):
        print(content)

    def get_msg(self, data):
        msg = str(input("请输入消息:"))
        group_msg = GroupMsg(group=self.TEST_GROUP, group_member=self.TEST_GROUP_MEMBER,
                             msg=msg, msg_chain=MessageSegment.text(msg))
        group_msg.reply = lambda content, **kwargs: print(content)
        self.add_msg(group_msg)

    def start(self) -> None:
        super().start()
        while True:
            self.get_msg(data={})


if __name__ == "__main__":
    client = ClientTest()
    client.start()
