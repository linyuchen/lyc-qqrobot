import tempfile
from pathlib import Path

import requests


class Avatar:

    def __init__(self, qq: str):
        self.qq = qq
        self.__path = None

    @property
    def url(self):
        return f"https://q1.qlogo.cn/g?b=qq&nk={self.qq}&s=640"

    @property
    def path(self):
        if self.__path:
            return self.__path
        path = tempfile.mktemp(suffix=".png")
        with open(path, "wb") as f:
            data = requests.get(self.url).content
            f.write(data)
        self.__path = Path(path)
        return self.__path
