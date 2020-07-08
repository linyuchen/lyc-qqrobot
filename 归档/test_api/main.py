<<<<<<< HEAD
<<<<<<< HEAD
# -*- coding:UTF-8 -*-
import sys
from views import *
from threading import Thread
urls = [
    (r"^/login$", login),
    (r"^/msgs$", get_msg),
    (r"^/input_vc$", inpust_vc),
    (r"^/friends$", get_friends),
    (r"^/groups$", get_groups),
    (r"^/uin2number$", uin2number),
    (r"^/send_msg2buddy$", send_msg2buddy),
    (r"^/send_msg2group$", send_msg2group),
    (r"^/delete_group_member$", delete_group_member),
    (r"^/handle_request_add_me_friend$", handle_request_add_me_friend),
    (r"^/handle_request_join_group$", handle_add_group_msg)
]


def main():
    app = HttpServer("127.0.0.1", 2999, urls)
    app.start()


if __name__ == "__main__":
    main()
    Thread(target=test_get_msg).start()
    note = u"""
    1: 发送好友消息
    2: 发送群消息
    q: 退出
    \n
    """
    while 1:
        cmd_index = raw_input(note).strip()

        if cmd_index == "1":
            msg = raw_input(u"发送好友消息:").strip()
            test_send_friend_msg(msg)
        elif cmd_index == "2":
            msg = raw_input(u"发送群消息:").strip()
            test_send_group_msg(msg)

        elif cmd_index == "q":
            sys.exit(0)


=======
# -*- coding:UTF-8 -*-
import sys
from views import *
from threading import Thread
urls = [
    (r"^/login$", login),
    (r"^/msgs$", get_msg),
    (r"^/input_vc$", inpust_vc),
    (r"^/friends$", get_friends),
    (r"^/groups$", get_groups),
    (r"^/uin2number$", uin2number),
    (r"^/send_msg2buddy$", send_msg2buddy),
    (r"^/send_msg2group$", send_msg2group),
    (r"^/delete_group_member$", delete_group_member),
    (r"^/handle_request_add_me_friend$", handle_request_add_me_friend),
    (r"^/handle_request_join_group$", handle_add_group_msg)
]


def main():
    app = HttpServer("127.0.0.1", 2999, urls)
    app.start()


if __name__ == "__main__":
    main()
    Thread(target=test_get_msg).start()
    note = u"""
    1: 发送好友消息
    2: 发送群消息
    q: 退出
    \n
    """
    while 1:
        cmd_index = raw_input(note).strip()

        if cmd_index == "1":
            msg = raw_input(u"发送好友消息:").strip()
            test_send_friend_msg(msg)
        elif cmd_index == "2":
            msg = raw_input(u"发送群消息:").strip()
            test_send_group_msg(msg)

        elif cmd_index == "q":
            sys.exit(0)


>>>>>>> cd04e7609aa41a427ce4bf4b29e124de6a13fa90
=======
# -*- coding:UTF-8 -*-
import locale
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from 归档.httpserver.app import HttpServer
from views import *
from threading import Thread
urls = [
    (r"^/login$", login),
    (r"^/msgs$", get_msg),
    (r"^/input_vc$", inpust_vc),
    (r"^/friends$", get_friends),
    (r"^/groups$", get_groups),
    (r"^/uin2number$", uin2number),
    (r"^/send_msg2buddy$", send_msg2buddy),
    (r"^/send_msg2group$", send_msg2group),
    (r"^/delete_group_member$", delete_group_member),
    (r"^/handle_request_add_me_friend$", handle_request_add_me_friend),
    (r"^/handle_request_join_group$", handle_add_group_msg)
]


def main():
    app = HttpServer("127.0.0.1", 4000, urls)
    app.start()


if __name__ == "__main__":
    main()
    Thread(target=test_get_msg).start()
    encoding = locale.getdefaultlocale()[1]
    note = u"""
    1: 发送好友消息
    2: 发送群消息
    q: 退出
    \n
    """
    while 1:
        cmd_index = raw_input(note.encode(encoding)).strip()

        if cmd_index == "1":
            msg = raw_input(u"发送好友消息:".encode(encoding)).strip()
            test_send_friend_msg(msg)
        elif cmd_index == "2":
            msg = raw_input(u"发送群消息:".encode(encoding)).strip()
            test_send_group_msg(msg)

        elif cmd_index == "q":
            sys.exit(0)

