import asyncio
import datetime
import random
import re
import secrets
import string
import time
import traceback
from pathlib import Path

import aiohttp

from common.utils.htmlhelper import get_tag_html, get_tag_attrs


class PostImagCC:
    def __init__(self):
        pass

    @staticmethod
    def __get_common_post_data(html: str):
        token = re.findall(r'["\']token["\'].*?[\'"](\w+)["\']', html)
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ui = f'[24,2294,960,"true","","","{now}"]'
        upload_session = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        session_upload = str(time.time() * 1000000)
        gallery = get_tag_html(html, tag="select", attrs={"name": "gallery"})
        if not gallery:
            gallery = ""
        else:
            gallery = get_tag_attrs(gallery[0], tag="option")[0].get("value")
        post_data = {
            "token": token[0],
            "upload_session": upload_session,
            "numfiles": "1",
            "ui": ui,
            "optsize": "0",
            "session_upload": session_upload[0],
            "gallery": gallery,
        }
        return post_data

    async def post_url(self, url: str, resp_short: bool = True):
        """
        通过url发送图片
        :param url: 图片的url
        :param resp_short: 是否返回短链接，短链接无法直接用于MJ
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://postimages.org/web") as resp:
                html = await resp.text()

            data = self.__get_common_post_data(html)
            data.update({"url": url})
            async with session.post("https://postimages.org/json/rr", data=data) as resp:
                res = await resp.json()
            if res.get("status") != "OK":
                raise Exception("上传失败")
            res_url = res["url"]
            if resp_short:
                return res_url
            direct_url = await self.__get_direct_url(res_url)
            return direct_url

    async def post_file(self, file_path: Path, resp_short: bool = False):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://postimages.org") as resp:
                html = await resp.text()

            data = self.__get_common_post_data(html)
            form = aiohttp.FormData()
            form.add_field("file", file_path.open("rb"))
            for key, value in data.items():
                form.add_field(key, value)
            async with session.post("https://postimages.org/json/rr", data=form) as resp:
                res = await resp.json()
                short_url = res["url"]
            if resp_short:
                return short_url
            direct_url = await self.__get_direct_url(short_url)
            return direct_url

    @staticmethod
    async def __get_direct_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
        direct_url = get_tag_attrs(html, tag="input", attrs={"id": "code_direct"})[0]["value"]
        return direct_url


if __name__ == '__main__':
    t = PostImagCC()
    # asyncio.run(t.post_url(""))
    test_path = Path(r"C:\Users\linyu\Desktop\640.png")
    asyncio.run(t.post_file(test_path))
