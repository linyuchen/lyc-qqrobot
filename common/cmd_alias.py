import re

CMD_ALIAS_DRAW = ("画图", "画画", "绘图", re.compile(r"^画一\w"),
                  "画个", "画张", "画只", "画头", "画条", "画幅",
                  "给我画", "帮我画")
