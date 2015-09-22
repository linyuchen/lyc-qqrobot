# -*- coding:UTF-8 -*-


class Protocol(object):
    """
    self.protocol: str, 协议名，如'HTTP'，注意都是大写的
    self.version: float, 协议版本, 如'1.1'
    """
    def __init__(self, protocol, version):
        self.protocol = protocol
        self.version = version

    def __str__(self):
        return self.protocol + "/" + str(self.version)
