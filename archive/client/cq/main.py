import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 19081))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(10)
while True:
    client, address = s.accept()
#
    while True:
        b = client.recv(1014)
        print(b)
#
    res = """{
    "status": "ok",
    "retcode": 0,
    "data": null,
}"""
    client.sendall(bytes(res, encoding="utf8"))
    print("send")
    client.close()
# from ws4py.websocket import WebSocket
#
# class Test(WebSocket):
#
#     def received_message(self, message):
#         print(message)



# import socketserver
# # from http.server import BaseHTTPRequestHandler
# #
# #
# class MyTCPHandler(socketserver.StreamRequestHandler):
#     def handle(self) -> None:
#         data = self.request.recv(1025)
#         print(data)
#             # print(data, repr(data))
#             # if data == "\r\n" or not data:
#             #     break

#
#
#
# with socketserver.TCPServer(("127.0.0.1", 19081), MyTCPHandler) as server:
#     server.serve_forever()

