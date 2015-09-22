#coding=UTF8

class MsgEvent(object):
    __doc__ = u"""
    MsgEvent是消息处理类
    请务必填写__doc__属性，方便生成插件说明
    该类必须有一个main方法，且此方法必须包含一个参数，此参数传入的消息实例
    构造函数可直接传入main方法

    self.qqClinet: 一个client实例
    """

    def __init__(self,main=None):
        if main:
            self.main = main
        self.qqClient = None


    def main(self,msg):
        """
        请复写此方法
        """
        raise NotImplementedError

    def setupQQInstance(self,qqInstance):
        """
        传入qq实例
        此方法为系统调用， 不可私自调用

        """

        self.qqClient = qqInstance



