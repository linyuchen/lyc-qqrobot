#coding=UTF8

import fontstyle

class QQUser:
    """
    self.fontStyle: entity.FontStyle,字体实例
    self.friends : dict, key为uin，value为entity.Friend实例
    self.groups : dict, key为uin，value为entity.Group实例
    self.qq: int, QQ号
    self.gtk: string,
    self.nick: string
    """
    
    def __init__(self):

        self.fontStyle = fontstyle.FontStyle()
        self.qq = 0
        self.nick = ""
        self.friends = {}
        self.groups = {}
        self.gtk = ""



