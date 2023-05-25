# coding=UTF8

class FontStyle:

    def __init__(self, font_name="黑体", font_size=12, color=0xff0000, bold=False, italic=False, underline=False):
        """
        @param font_name:黑体 宋体 ...
        @type: str

        @param font_size:
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
        self.fontName = font_name
        self.fontSize = font_size
        self.fontStyle = [int(bold), int(italic), int(underline)]
        self.fontColor = color

    def __str__(self):
        string = "{\"name\":\"%s\",\"size\":\"%d\",\"style\":%s,\"color\":\"%d\"}" % (
        self.fontName, self.fontSize, str(self.fontStyle), self.fontColor)
        return string
