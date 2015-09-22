# -*- coding:UTF-8 -*-

from httpserver.app import HttpServer
from views import *
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


def main(qq, pwd, port):
    qq_client.qq = qq
    qq_client.pwd = pwd
    qq_client.first_login()
    app = HttpServer("127.0.0.1", port, urls)
    app.start()
