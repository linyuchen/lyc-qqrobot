#coding=UTF8

class FontStyle:

    def __init__(self,fontName=u"黑体",fontSize=12,color=0xff0000,bold=False,italic=False,underline=False):
        """
        @param fontName:黑体 宋体 ...
        @type: str

        @param fontSize:
        @type: int


        @param color: rbg颜色的十进制
        @type: int

        @param bold: 粗体
        @type: bool

        @param italic: 斜体
        @type: bool

        @param underline: 下划线
        @type: bool
        """
        self.fontName = fontName
        self.fontSize = fontSize
        self.fontStyle = [int(bold), int(italic), int(underline)]
        self.fontColor = color

    def __str__(self):
        
        string = "{\"name\":\"%s\",\"size\":\"%d\",\"style\":%s,\"color\":\"%d\"}"%(self.fontName,self.fontSize,str(self.fontStyle),self.fontColor)
        return string
