# -*- coding:UTF-8 -*-

import json


class Response(object):
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def make2dict(self):
        result = {
            "code": self.code,
            "data": self.data
        }
        return result
