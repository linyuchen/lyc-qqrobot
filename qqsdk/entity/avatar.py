import tempfile
import time
from pathlib import Path

import requests


class Avatar:

    def __init__(self, qq: str):
        self.qq = qq
        self.__path = None
        self.__last_update_time = 0

    @property
    def url(self):
        return f"https://thirdqq.qlogo.cn/g?b=qq&nk={self.qq}&s=640"

    @property
    def path(self):
        if self.__path and (time.time() - self.__last_update_time) < 60 * 10:
            return self.__path
        self.__last_update_time = time.time()
        path = tempfile.mktemp(suffix=".png")
        with open(path, "wb") as f:
            data = requests.get(self.url).content
            f.write(data)
        self.__path = Path(path)
        return self.__path
