
from typing import Literal, TypedDict


class OnebotSelf(TypedDict):
    self_id: str
    platform: Literal["qq"]


class OnebotMessageItemDataAt(TypedDict):
    mention: str  # at的qq号


class OnebotMessageItemDataText(TypedDict):
    text: str


class OnebotMessageItemDataImage(TypedDict):
    path: str


class OnebotMessageItemDataReply(TypedDict):
    reply: str  # 回复的消息id


class OnebotMessageItemAt(TypedDict):
    type: Literal["at"]
    data: OnebotMessageItemDataAt


class OnebotMessageItemText(TypedDict):
    type: Literal["text"]
    data: OnebotMessageItemDataText


class OnebotMessageItemImage(TypedDict):
    type: Literal["image"]
    data: OnebotMessageItemDataImage


class OnebotMessageItemReply(TypedDict):
    type: Literal["reply"]
    data: OnebotMessageItemDataReply


class OnebotNewMessage(TypedDict):
    self: OnebotSelf
    type: Literal["message"]
    detail_type: Literal["group", "private"]
    message: list[OnebotMessageItemAt | OnebotMessageItemText | OnebotMessageItemImage | OnebotMessageItemReply]
    group_id: str
    user_id: str
