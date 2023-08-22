import datetime
import re
import secrets
import string
import time

import aiohttp

from common.utils.htmlhelper import get_tag_html, get_tag_attrs


class PostImagCC:
    def __init__(self):
        pass

    async def post(self, url: str):
        """
        通过url发送图片
        :param url: 图片的url
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://postimages.org/web") as resp:
                html = await resp.text()
        # open("test.html", "w", encoding="utf-8").write(html)
            token = re.findall(r"'token':'(\w+)'", html)
            if not token:
                raise Exception("获取token失败")
            token = token[0]
            # 生成一个随机的32位字符串
            characters = string.ascii_letters + string.digits
            upload_session = ''.join(secrets.choice(characters) for _ in range(32))
            gallery = get_tag_html(html, tag="select", attrs={"name": "gallery"})
            if not gallery:
                gallery = ""
            else:
                gallery = get_tag_attrs(gallery[0], tag="option")[0].get("value")
            # gallery = ""
            now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            ui = f'[24,2294,960,"true","","","{now}"]'
            data = {
                "token": token,
                "upload_session": upload_session,
                "gallery": gallery,
                "ui": ui,
                "numfiles": "1",
                "optsize": "0",
                "session_upload": str(int(time.time() * 1000)),
                "url": url
            }
            async with session.post("https://postimages.org/json/rr", data=data) as resp:
                res = await resp.json()
            if res["status"] != "OK":
                raise Exception("上传失败")
            res_url = res["url"]
            direct_url = await self.get_direct_url(res_url)
            return direct_url

    async def get_direct_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
        direct_url = get_tag_attrs(html, tag="input", attrs={"id": "code_direct"})[0]["value"]
        return direct_url
