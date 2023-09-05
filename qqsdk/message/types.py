# -*- coding: utf-8 -*-
from enum import StrEnum


class MessageTypes(StrEnum):
    FRIEND = "FriendMsg"
    FRIEND_SIGNATURE = "FriendSignatureChanged"
    FRIEND_STATUS = "FriendStatusChanged"
    FRIEND_VOICE = "FriendVoice"
    TEMP = "temp"  # 临时会话
    ADDED_ME_FRIEND = "AddedMeFriend"
    REQUEST_ADD_ME_FRIEND = "RequestAddMeFriend"
    ADD_ME_FRIEND_RESULT = "AddMeFriendResult"

    GROUP = "GroupMsg"
    GROUP_ADMIN_CHANGE = "GroupAdminChange"
    GROUP_MEMBER_CARD_CHANGE = "GroupMemberCardChange"
    GROUP_REQUEST_JOIN = "GroupRequestJoin"
    GROUP_NEW_MEMBER = "GroupNewMember"
    GROUP_JOINED = "GroupJoined"  # 我加入群成功
    GROUP_NUDGE = "GroupNudge"  # 群戳一戳
