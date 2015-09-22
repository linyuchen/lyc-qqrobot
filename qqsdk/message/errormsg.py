# -*- encoding:UTF8 -*-
import basemsg
BaseMsg = basemsg.BaseMsg

class ErrorMsg(BaseMsg):

    def __init__(self):
        super(ErrorMsg, self).__init__()
        self.summary = ""
