# -*- coding:UTF-8 -*-

import re
import json
import urllib

import content_types
from common import Protocol


class Url(object):
    """
    self.url, str, 请求的url
    self.path, str, 去掉了get参数的url
    self.param, dict, GET方法的参数
    """

    def __init__(self):
        self.url = ""
        self.path = ""
        self.param = {}


class Headers(object):
    """
    self.method, str, 请求方法
    self.protocol, str, http的协议版本
    """
    def __init__(self, param_str):

        self.__param_str = param_str
        self.__param = self.__analysis()

    def get(self, key, default=None):
        return self.__param.get(key, default)

    def __analysis(self):
        param =  re.findall("(.+?): (.+?)\r\n", self.__param_str)
        return dict(param)

    def __str__(self):
        return self.param_str


class Request(object):
    """
    客户端提交过来的请求
    self.method: str, 请求方法，注意都是大写的
    self.protocol: Protocol实例
    self.headers: Headers实例
    self.url: Url实例
    self.post_data: dict, POST的内容
    self.body: str, 包体
    self.body_json: dict, json格式的body, 并在头部声明了application/json才会有
    self.addr: tuple, (ip, port)
    self.sock: Socket实例
    """

    def __init__(self):
        self.method = ""
        self.headers = None
        self.url = None
        self.protocol = None
        self.post_data = {}
        self.body = ""
        self.body_json = {}
        self.addr = None
        self.sock = None

    def close(self):
        self.sock.close()


class Analyser(object):

    def analysis_form_params(self, param):

        """
        处理表单数据
        分析a=1&b=2这种格式的数据，GET、POST方法中常用到，
        @type param: str

        @return: {key: value, ...}
            key: str, value: str
        @rtype: dict
        """
    
        params = re.findall("([^&]+?)=([^&]*)", param)
        params = map(lambda p: (p[0], p[1]), params)
        return dict(params)


class HeadersAnalyser(Analyser):

    def __init__(self, headers_str):
        """
        @param headers_str: 头部字符串
        """
        self.headers_str = headers_str

    def __analysis_url(self, url):
        """
        提取url的path和GET方法的参数
        @type url: str

        @return: path, param
        @rtype: (str, dict)
        """
        url_object = Url()
        url_object.url = url
        pos = url.find("?")

        if pos == -1:
            url_object.param = {}
            url_object.path = url
            return url_object

        url_object.path = url[: pos]
        param = url[pos + 1:]
        url_object.param = self.analysis_form_params(urllib.unquote_plus(param))

        return url_object

    def __analysis_protocol(p):
        pos = p.find("/")
        if pos == -1:
            return None
        name = p[:pos]
        try:
            version = float(p[pos + 1:])
        except TypeError, e:
            raise e

        protocol = Protocol(name, version)
        return protocol
    
    def analysis(self):
        """
        分析头部字符串
        @return: Request实例
        """

        first_line = self.headers_str[: self.headers_str.find("\r\n")].split()
        if len(first_line) < 3:
            return None

        request = Request()
        request.method = first_line[0]
        request.url = self.__analysis_url(first_line[1])
        headers = Headers(self.headers_str)
        request.headers = headers

        return request


class BodyAnalyser(Analyser):

    def __init__(self, request, body_data):
        self.request = request
        self.request.body = body_data
        self.body_data = body_data

    def analysis(self):
        """
        @return: 分析好了body 的Request实例
        """
        method = self.request.method
        headers = self.request.headers
        content_type = headers.get(content_types.KEY)
        if method == "POST" and content_type == content_types.FORM:
            self.request.post_data = self.analysis_form_params(self.body_data)

        if content_type == content_types.JSON:
            try:
                self.request.body_json = json.loads(self.body_data)
            except ValueError, e:
                raise e

        return self.request






if __name__ == "__main__":
    url = Url()
    url.url = "1"
    print url
