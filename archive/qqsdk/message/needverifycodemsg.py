# -*- encoding:UTF8 -*-
from qqsdk.message.basemsg import BaseMsg
from dataclasses import dataclass


@dataclass
class NeedVerifyCodeMsg(BaseMsg):
    """
    self.qq:    需要验证码的QQ 或者群 或者 其他
    """
    def __init__(self, sender):
        super(NeedVerifyCodeMsg, self).__init__()
        self.qq = sender

