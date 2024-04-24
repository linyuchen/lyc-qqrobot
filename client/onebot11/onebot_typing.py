from enum import StrEnum
from typing import Literal, TypedDict, Optional


class MessageItemType(StrEnum):
    text = "text"
    image = "image"
    mface = "mface"
    at = "at"
    reply = "reply"


class _OnebotMessageItemDataAt(TypedDict):
    mention: str  # at的qq号
    qq: str  # at的qq号


class _OnebotMessageItemDataText(TypedDict):
    text: str


class _OnebotMessageItemDataImage(TypedDict):
    path: str
    file: str
    url: str


class _OnebotMessageItemDataReply(TypedDict):
    reply: str  # 回复的消息id
    id: str


class _OnebotMessageItemAt(TypedDict):
    type: Literal[MessageItemType.at]
    data: _OnebotMessageItemDataAt


class _OnebotMessageItemText(TypedDict):
    type: Literal[MessageItemType.text]
    data: _OnebotMessageItemDataText


class _OnebotMessageItemImage(TypedDict):
    type: Literal[MessageItemType.image]
    data: _OnebotMessageItemDataImage


class _OnebotMessageItemReply(TypedDict):
    type: Literal[MessageItemType.reply]
    data: _OnebotMessageItemDataReply


class OnebotRespNewMessage(TypedDict):
    self_id: str
    type: Literal["message"]
    message_type: Literal["group", "private"]
    message: list[_OnebotMessageItemAt | _OnebotMessageItemText | _OnebotMessageItemImage | _OnebotMessageItemReply]
    message_id: str
    group_id: str
    user_id: str


class OnebotRespGroupMember(TypedDict):
    user_id: str
    user_name: str
    user_display_name: str


class OnebotRespFriend(TypedDict):
    user_id: str
    user_name: str


class OnebotRespGroup(TypedDict):
    group_id: str
    group_name: str
