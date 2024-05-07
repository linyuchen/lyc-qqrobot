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
        # return f"https://thirdqq.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        return f"http://q2.qlogo.cn/headimg_dl?dst_uin={self.qq}&spec=640"

    @property
    def url2(self):
        # return f"https://thirdqq.qlogo.cn/g?b=qq&nk={self.qq}&s=640"
        return f"http://q2.qlogo.cn/headimg_dl?dst_uin={self.qq}&spec=100"

    @property
    def path(self):
        if self.__path and (time.time() - self.__last_update_time) < 60 * 10:
            return self.__path
        self.__last_update_time = time.time()
        path = tempfile.mktemp(suffix=".png")
        with open(path, "wb") as f:
            data = requests.get(self.url).content
            if len(data) < 3 * 1024:
                data = requests.get(self.url2).content
            f.write(data)
        self.__path = Path(path)
        return self.__path
