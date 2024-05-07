import asyncio
import re
import tempfile
from pathlib import Path
from typing import Callable

import aiohttp
import pandas as pd
from retry import retry

from common.utils.translator import trans, is_chinese
from .exceptions import MidjourneyException

default_json = {
    "authorization": "",
    "channelid": "1127887388648153121",  # 当前频道浏览器上方有
    "guild_id": "1127887388648153118",  # 当前频道浏览器上方有
    "session_id": "e7de53b801a3670887aa7cfb36d68de0",  # 未知
    "version": "1118961510123847772",  # 固定的
    "id": "938956540159881230",  # command id，固定的
    "application_id": "936929561302675456",  # 固定的
    "flags": "--v 5",
    # "http://127.0.0.1:10809"
    "proxy": "http://127.0.0.1:7890",
    "timeout": 120
}


class MidjourneyClient:

    def __init__(self):

        params = default_json
        self.channelid = params['channelid']
        self.authorization = params['authorization']
        self.application_id = params['application_id']
        self.guild_id = params['guild_id']
        self.session_id = params['session_id']
        self.version = params['version']
        self.id = params['id']
        self.flags = params['flags']

        self.headers = {
            'authorization': self.authorization
        }
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None
        self.retry_count = 10

    async def send(self, prompt):

        prompt = prompt.replace('_', ' ')
        prompt = " ".join(prompt.split())
        prompt = re.sub(r'[^a-zA-Z0-9\s:-]+', '', prompt)
        prompt = prompt.lower()
        # 多个空格变一个空格
        prompt = re.sub(r'\s+', ' ', prompt)

        payload = {'type': 2,
                   'application_id': self.application_id,
                   'guild_id': self.guild_id,
                   'channel_id': self.channelid,
                   'session_id': self.session_id,
                   'data': {
                       'version': self.version,
                       'id': self.id,
                       'name': 'imagine',
                       'type': 1,
                       'options': [{'type': 3, 'name': 'prompt', 'value': prompt}],
                       'attachments': []}
                   }

        async with aiohttp.ClientSession() as session:
            for i in range(self.retry_count):
                try:
                    async with session.post('https://discord.com/api/v9/interactions',
                                            json=payload, headers=self.headers,
                                            proxy=self.proxy) as resp:
                        if resp.status == 204:
                            break
                except Exception as e:
                    print(e)
            else:
                raise MidjourneyException("发送画图请求失败！")

        return prompt

    async def retrieve_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={10}',
                                   headers=self.headers, proxy=self.proxy) as response:
                jsonn = await response.json()
        return jsonn

    async def message_listener(self):
        while True:
            messages = await self.retrieve_messages()
            await asyncio.sleep(1)


class Receiver:

    def __init__(self,
                 prompt
                 ):

        self.prompt = prompt

        self.sender_initializer()

        self.df = pd.DataFrame(columns=['prompt', 'url', 'filename', 'is_downloaded'])

    def sender_initializer(self):

        params = default_json
        self.channelid = params['channelid']
        self.authorization = params['authorization']
        self.headers = {'authorization': self.authorization}
        if params['proxy'] != "":
            # 代理服务器的IP地址和端口号
            self.proxy = params['proxy']
        else:
            self.proxy = None
        self.timeout = params['timeout']

    @retry(tries=3)
    async def retrieve_messages(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={10}',
                                   headers=self.headers, proxy=self.proxy) as response:
                jsonn = await response.json()
        return jsonn

    async def collecting_results(self) -> tuple[str, str]:
        # tmp_json = {
        #     "code": 0,
        #     "url": ""
        # }

        message_list = await self.retrieve_messages()
        self.awaiting_list = pd.DataFrame(columns=['prompt', 'status'])
        for message in message_list:
            try:
                # 如果这条消息是由"Midjourney Bot"发送的，并且包含双星号（**），则它是一个需要处理的请求
                # print(message)
                if (message['author']['username'] == 'Midjourney Bot') and ('**' in message['content']):
                    # print("找到了消息")
                    if len(message['attachments']) > 0:
                        # 如果该消息包含图像附件，则获取该附件的URL和文件名，并将其添加到df DataFrame中
                        if (message['attachments'][0]['filename'][-4:] == '.png') or (
                                '(Open on website for full quality)' in message['content']):
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            origin_url = message['attachments'][0]['proxy_url']
                            url = message['attachments'][0]['proxy_url'] + "?width=1024&height=1024"
                            filename = message['attachments'][0]['filename']

                            # print(f"prompt2=[{prompt}]")

                            # 判断prompt是否匹配
                            if self.prompt == prompt:
                                # DataFrame的索引是消息ID，因此我们可以根据消息ID来确定哪个请求与哪个消息相对应
                                if id not in self.df.index:
                                    self.df.loc[id] = [prompt, url, filename, 0]
                                    # print("filename=" + filename)
                                    # print("url=" + url)
                                    # tmp_json["url"] = url
                                    return url, origin_url
                        # 如果消息中没有图像附件，则将该请求添加到awaiting_list DataFrame中，等待下一次检索。
                        else:
                            id = message['id']
                            prompt = message['content'].split('**')[1].split(' --')[0]
                            if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                                try:
                                    status = re.findall("(\w*%)", message['content'])[0]
                                except:
                                    status = 'unknown status'
                            self.awaiting_list.loc[id] = [prompt, status]

                    else:
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        if '(Waiting to start)' in message['content']:
                            status = 'Waiting to start'
                        self.awaiting_list.loc[id] = [prompt, status]
            except Exception as e:
                print(e)

        return None

    async def check_result(self):
        for i in range(int(self.timeout / 3)):
            try:
                ret = await self.collecting_results()
            except Exception as e:
                print(e)
                continue
            if ret != None:
                return ret
            # for i in self.df.index:
            #         return self.df.loc[i].url
            # 睡眠3s
            await asyncio.sleep(3)
        return None

    async def download_img(self, url) -> Path:
        async with aiohttp.ClientSession() as session:
            for i in range(10):
                try:
                    async with session.get(url, headers=self.headers, proxy=self.proxy) as response:
                        data = await response.read()
                        tmp_path = tempfile.mktemp(".png")
                        open(tmp_path, 'wb').write(data)
                        return Path(tmp_path)
                except Exception as e:
                    print(e)


async def __send(prompt, callback: Callable[[Path, str], None]):
    sender = MidjourneyClient()
    prompt = await sender.send(prompt)

    # print(f"prompt=[{prompt}]")

    receiver = Receiver(prompt)
    try:
        thumb_url, origin_url = await receiver.check_result() or (None, None)
    except Exception as e:
        return str(e)

    try:
        if thumb_url is not None:
            # print(f"result=[{thumb_url}]")
            result = await receiver.download_img(thumb_url)
            callback(result, origin_url)
    except Exception as e:
        # print(e)
        return str(e)


def draw(prompt: str, callback: Callable[[Path, str], None]):
    prompt = prompt.split("-", 1)
    params = ""
    if len(prompt) > 1:
        prompt, params = prompt
        params = " -" + params
    else:
        prompt = prompt[0]
    if is_chinese(prompt):
        prompt = trans(prompt)
    prompt = prompt + params
    return asyncio.run(__send(prompt, callback))
