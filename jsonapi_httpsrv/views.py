# -*- coding:UTF-8 -*-

from qqclient import QQClient
from httpserver.response import JsonResponse

qq_client = QQClient("", "")


def make_jsonresponse(api_func):
    def func(req):
        res = api_func(req)
        # print res
        return JsonResponse(res.make2dict())
    return func


@make_jsonresponse
def login(req):
    # print qq, pwd
    res = qq_client.login()
    return res


@make_jsonresponse
def get_msg(req):
    # print __file__, "get_msg"
    return qq_client.get_msg()


@make_jsonresponse
def get_friends(req):
    return qq_client.get_friends()


@make_jsonresponse
def get_groups(req):
    return qq_client.get_groups()


@make_jsonresponse
def inpust_vc(req):
    vc = req.body_json.get("vc")
    return qq_client.input_verify_code(vc)


@make_jsonresponse
def uin2number(req):
    uin = req.body_json.get("uin")
    return qq_client.uin2qq(uin)


@make_jsonresponse
def send_msg2buddy(req):
    uin = req.body_json.get("uin")
    msg = req.body_json.get("msg")
    # print u"发送好友消息", uin, msg
    res = qq_client.sendMsg2Buddy(uin, msg)
    # print res
    return res


@make_jsonresponse
def send_msg2group(req):
    uin = req.body_json.get("uin")
    msg = req.body_json.get("msg")
    return qq_client.sendMsg2Group(uin, msg)


@make_jsonresponse
def delete_group_member(req):
    group = req.body_json.get("group")
    member = req.body_json.get("member")
    return qq_client.deleteGroupMember(group, member)


@make_jsonresponse
def handle_request_add_me_friend(req):
    qq = req.body_json.get("qq")
    reject_reason = req.body_json.get("reject_reason")
    allow = req.body_json.get("allow")
    return qq_client.allowAddFriend(qq, reject_reason, allow)


@make_jsonresponse
def handle_add_group_msg(req):
    member = req.body_json.get("member")
    group = req.body_json.get("group")
    reject_reason = req.body_json.get("reject_reason")
    allow = req.body_json.get("allow")
    return qq_client.handleAddGroupMsg(member, group, reject_reason, allow)
