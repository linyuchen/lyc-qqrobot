#coding=UTF8

class SendMsgFilter(object):

    __doc__ = """
    用于过滤消息的发送
    """
    def __init__(self, filterFunc = None):

        if filterFunc:
            self.main = filterFunc

    def main(self, msgContent):
        """
        :msgContent: str, 发出去的消息内容
        :return: 返回布尔型， 
            True: 消息可以通过，正常发出
            False: 消息不准通过，不发出
        """
        raise NotImplementedError
