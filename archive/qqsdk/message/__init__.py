# coding=UTF8
from typing import Type

from qqsdk.message.basemsg import BaseMsg
from qqsdk.message.friendmsg import FriendMsg
from qqsdk.message.groupmsg import (GroupMsg, GroupNudgeMsg,
                                    GroupSendMsg, GroupAdminChangeMsg,
                                    GroupMemberCardChangedMsg)
from qqsdk.message.msghandler import MsgHandler
from qqsdk.message.types import MessageTypes
from qqsdk.message.segment import MessageSegment

GeneralMsg = Type[GroupMsg | FriendMsg]
