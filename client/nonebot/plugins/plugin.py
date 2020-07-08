# coding=UTF8

from qqsdk.eventlistener import EventListener
from client.nonebot.main import QQClient
from qqsdk.message.msghandler import MsgHandler, BaseMsg
from qqsdk.message.friendmsg import FriendMsg
from nonebot import on_natural_language, NLPSession


class MsgHandlerTest(MsgHandler):
    bind_msg_types = (FriendMsg,)

    def handle(self, msg: BaseMsg):
        print("ok", msg.msg)


event_listener = EventListener(qq_client=QQClient(), msg_handlers=[MsgHandlerTest()])
event_listener.start()


@on_natural_language
async def test(session: NLPSession):
    print(session.msg_text)
    sub_type = session.event.sub_type
    msg = session.msg_text
    if sub_type == "friend":
        event_listener.add_msg(FriendMsg(friend=None, msg=msg))



