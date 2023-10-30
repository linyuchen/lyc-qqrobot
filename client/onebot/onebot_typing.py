
from typing import Literal, TypedDict


class _OnebotSelf(TypedDict):
    user_id: str
    platform: Literal["qq"]


class _OnebotMessageItemDataAt(TypedDict):
    mention: str  # at的qq号


class _OnebotMessageItemDataText(TypedDict):
    text: str


class _OnebotMessageItemDataImage(TypedDict):
    path: str


class _OnebotMessageItemDataReply(TypedDict):
    reply: str  # 回复的消息id


class _OnebotMessageItemAt(TypedDict):
    type: Literal["at"]
    data: _OnebotMessageItemDataAt


class _OnebotMessageItemText(TypedDict):
    type: Literal["text"]
    data: _OnebotMessageItemDataText


class _OnebotMessageItemImage(TypedDict):
    type: Literal["image"]
    data: _OnebotMessageItemDataImage


class _OnebotMessageItemReply(TypedDict):
    type: Literal["reply"]
    data: _OnebotMessageItemDataReply


class OnebotRespNewMessage(TypedDict):
    self: _OnebotSelf
    type: Literal["message"]
    detail_type: Literal["group", "private"]
    message: list[_OnebotMessageItemAt | _OnebotMessageItemText | _OnebotMessageItemImage | _OnebotMessageItemReply]
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
