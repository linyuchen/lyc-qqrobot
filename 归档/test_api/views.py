<<<<<<< HEAD
# -*- coding:UTF-8 -*-
from Queue import Queue
from status_codes import *
from test_config import *
msgs = Queue()
send_msgs = Queue()
send_group_msgs = Queue()


def test_send_friend_msg(msg):
    data = {"data": [{"Event": "FriendMsg", "Data": {"Sender": TEST_QQ, "SendTime": time.time(), "Message": msg}}]}
    msgs.put(data)


def test_send_group_msg(msg):
    data = {"data": [{"Event": "GroupMsg", "Data":
        {"GroupQQ": TEST_GROUP_QQ, "ClusterNum": TEST_GROUP_QQ, "Sender": TEST_QQ, "SenderQQ": TEST_QQ,
         "Message": msg, "SendTime": time.time()}}]}

    msgs.put(data)


def test_get_msg():
    while 1:
        msg = send_msgs.get()
        print(msg)


def login(req):
    # print qq, pwd
    res = JsonResponse({})
    return res


def get_msg(req):
    # print __file__, "get_msg"
    while 1:
        res = msgs.get()
        res = JsonResponse(res)
        return res


def get_friends(req):
    res = {"data": {"%d" % TEST_QQ:
                         {"uin": TEST_QQ,
                          "groupId": 1, "groupName": 1, "markName": 1, "nick": str(TEST_QQ)}}}
    return JsonResponse(res)


def get_groups(req):
    res = {"data":
               {str(TEST_GROUP_QQ):
                    {"uin": TEST_GROUP_QQ, "name": u"测试群", "mask": 0, "members":
                        {TEST_QQ: {"nick": str(TEST_QQ), "isAdmin": True, "status": "online",
                                   "card": str(TEST_QQ), "uin": TEST_QQ, "isCreator": True
                                   }
                         }
                     }
                }
           }
    return JsonResponse(res)


def inpust_vc(req):
    res = {}
    return res


def uin2number(req):
    uin = req.url.param.get("uin")
    return JsonResponse({"data": uin})


def send_msg2buddy(req):
    msg = req.url.param.get("msg")
    # print msg
    send_msgs.put(msg)
    return JsonResponse({})
    # print u"发送好友消息", uin, msg


def send_msg2group(req):
    msg = req.url.param.get("msg")
    send_msgs.put(msg)
    return JsonResponse({})


def delete_group_member(req):
    res = {}
    return JsonResponse({})


def handle_request_add_me_friend(req):
    res = {}
    return JsonResponse({})


def handle_add_group_msg(req):
    return JsonResponse({})
=======
# -*- coding:UTF-8 -*-
import time
from Queue import Queue
from 归档.httpserver.response import JsonResponse
from status_codes import *
from test_config import *
msgs = Queue()
send_msgs = Queue()
send_group_msgs = Queue()


def test_send_friend_msg(msg):
    data = {"data": [{"Event": "FriendMsg", "Data": {"Sender": TEST_QQ, "SendTime": time.time(), "Message": msg}}]}
    msgs.put(data)


def test_send_group_msg(msg):
    data = {"data": [{"Event": "GroupMsg", "Data":
        {"GroupQQ": TEST_GROUP_QQ, "ClusterNum": TEST_GROUP_QQ, "Sender": TEST_QQ, "SenderQQ": TEST_QQ,
         "Message": msg, "SendTime": time.time()}}]}

    msgs.put(data)


def test_get_msg():
    while 1:
        msg = send_msgs.get()
        print(msg)


def login(req):
    # print qq, pwd
    res = JsonResponse({})
    return res


def get_msg(req):
    # print __file__, "get_msg"
    while 1:
        res = msgs.get()
        res = JsonResponse(res)
        return res


def get_friends(req):
    res = {"data": {"%d" % TEST_QQ:
                         {"uin": TEST_QQ,
                          "groupId": 1, "groupName": 1, "markName": 1, "nick": str(TEST_QQ)}}}
    return JsonResponse(res)


def get_groups(req):
    res = {"data":
               {str(TEST_GROUP_QQ):
                    {"uin": TEST_GROUP_QQ, "name": u"测试群", "mask": 0, "members":
                        {TEST_QQ: {"nick": str(TEST_QQ), "isAdmin": True, "status": "online",
                                   "card": str(TEST_QQ), "uin": TEST_QQ, "isCreator": True
                                   }
                         }
                     }
                }
           }
    return JsonResponse(res)


def inpust_vc(req):
    res = {}
    return res


def uin2number(req):
    uin = req.url.param.get("uin")
    return JsonResponse({"data": uin})


def send_msg2buddy(req):
    msg = req.url.param.get("msg")
    # print msg
    send_msgs.put(msg)
    return JsonResponse({})
    # print u"发送好友消息", uin, msg


def send_msg2group(req):
    msg = req.url.param.get("msg")
    send_msgs.put(msg)
    return JsonResponse({})


def delete_group_member(req):
    res = {}
    return JsonResponse({})


def handle_request_add_me_friend(req):
    res = {}
    return JsonResponse({})


def handle_add_group_msg(req):
    return JsonResponse({})
>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90
