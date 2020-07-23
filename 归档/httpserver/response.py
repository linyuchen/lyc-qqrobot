# -*- coding:UTF8 -*-

import json

import status_codes
import content_types


class Headers(object):
    """
    self.status_code: int, 状态码
    self.protocol: 协议版本
    self.content_length: int, body长度
    """

    def __init__(self):
        self.status_code = status_codes.OK
        self.protocol = "HTTP/1.1"
        self.content_length = 0
        self.__others = {}

    def make2str(self):
        headers = u"%s %d %s\r\n" % (self.protocol, self.status_code, status_codes.CODES[self.status_code])
        for key, value in self.__others.items():
            headers += u"%s: %s\r\n" % (key, value)
        headers += "Content-Length: %d\r\n" % (self.content_length)

        return headers

    def add(self, key, value):
        self.__others[key] = value

    def add_headers(self, headers):
        self.__others.update(headers)


class Body(object):
    """
    """

    def __init__(self, content, encoding="UTF8"):
        """
        @param content: body的内容
        @type content: str

        @param encoding: 编码, 默认是UTF-8
        @type encoding: str
        """
        self.content = content
        self.encoding = encoding

    def make2str(self):
        if self.encoding:
            self.content = self.content.encode(self.encoding)

        return self.content


class Response(object):
    """
    self.headers: Headers实例
    self.body: Body实例
    """

    def __init__(self):
        """
        """
        self.headers = None
        self.body = None

    def make2str(self):
        if self.body:
            self.headers.content_length = len(self.body.content)

        res = self.headers.make2str() + "\r\n" + self.body.make2str()
        return res


class HttpResponse(Response):

    def __init__(self, content):
        """
        @param content: unicode
        """
        self.content = content
        self.headers = Headers()
        self.body = Body(content)


class JsonResponse(HttpResponse):

    def __init__(self, content):
        content = json.dumps(content)
        super(JsonResponse, self).__init__(content)
        self.headers.add(content_types.KEY, content_types.JSON)


