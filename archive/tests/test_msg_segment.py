from unittest import TestCase

from qqsdk.message import MsgHandler
from qqsdk.message.segment import MessageSegment


class TestMessageSegment(TestCase):

    def test_message_segment_add(self):
        r = MessageSegment.at("123") + (MessageSegment.image_path("456") + MessageSegment.image_path("789"))
        print(r)

    def test_msg_handler(self):
        MsgHandler(name="asdf")
        MsgHandler()
        print(len(MsgHandler.instances))
