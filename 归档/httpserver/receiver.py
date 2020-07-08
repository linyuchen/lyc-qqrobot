# -*- coding:UTF8 -*-

import request


class Receiver(object):

    def __init__(self, client_sock, client_addr):

        self.client_sock = client_sock
        self.client_addr = client_addr

    def recv(self):

        current_byte = ""
        received_data = ""
        lines = 0
        while True:
            current_byte = self.client_sock.recv(1)
            received_data += current_byte
            if received_data[-4:] == "\r\n\r\n":
                break
        req = request.HeadersAnalyser(received_data).analysis()

        content_length = req.headers.get("Content-Length", 0)
        content_data = ""
        if content_length:
            content_length = int(content_length)
            content_data = self.client_sock.recv(content_length)

        req = request.BodyAnalyser(req, content_data).analysis()

        req.sock = self.client_sock
        req.addr = self.client_addr
        return req
