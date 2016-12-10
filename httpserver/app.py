# -*- coding:UTF8 -*-

import traceback
import threading
import re
import socket
import Queue

from receiver import Receiver


class HttpServer(threading.Thread):

    def __init__(self, ip, port, urls):

        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((ip,port))
        self.socket.listen(0)
        threading.Thread.__init__(self)
        self.requsets = Queue.Queue()
        self.running = True
        self.urls = urls

    def error_handle(self):
        """
        socket.accept()的错误处理
        """
        traceback.print_exc()

    def run(self):

        while self.running:
            try:
                client_sock, addr = self.socket.accept()
                threading.Thread(target=lambda c=client_sock, a=addr: self.recv(c, a)).start()
            except:
                self.error_handle()

    def recv(self, client_sock, addr):

        request = Receiver(client_sock, addr).recv()
        for url_pattern, func in self.urls:
            if re.match(url_pattern, request.url.path):
                res = func(request)
                request.sock.send(res.make2str())
                request.close()
                return
        
        request.close()


if __name__ == "__main__":
    from response import HttpResponse
    from response import JsonResponse
    def test(req):
        print req.addr
#        return JsonResponse(req)
        return JsonResponse({"1":2})
    urls = [
            (r"^/$", test)
            ]
    app = HttpServer("127.0.0.1", 8088, urls)
    app.start()
