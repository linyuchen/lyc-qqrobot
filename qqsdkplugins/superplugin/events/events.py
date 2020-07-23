# -*- coding:utf8 -*-


class Event(object):
    name = ""
    qq = ""
    msg = ""
    time = ""


class PersonalMsgEvent(Event):
    name = "personal_msg"
    pass


class GroupMsgEvent(Event):
    name = "group_msg"
    group_qq = ""
