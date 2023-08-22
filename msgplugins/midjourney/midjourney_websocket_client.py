import asyncio
import random
import socket
import threading
from copy import deepcopy
from datetime import datetime

import aiohttp
import pytz
import requests
from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType

from common.logger import logger
from .midjourney_client import MidjourneyClientBase, Task, Message, TaskCallbackResponse, TaskType


class MidjourneyClient(MidjourneyClientBase):

    def __init__(self, token: str, channel_id: str, guild_id: str, proxy: str = None):
        self.token = token
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.url = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.heartbeat_interval = 0
        self.proxy = proxy
        self.ws: ClientWebSocketResponse | None = None
        super().__init__(proxy)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': self.token})
        self.session.proxies.update({'http': self.proxy, 'https': self.proxy})
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = threading.Thread(target=loop.run_until_complete, args=(self.start(),))
        thread.start()

    async def start(self):
        await self.__init_ws()
        h_task = asyncio.create_task(self.__heart())
        p_task = asyncio.create_task(self.__pool_event())
        await asyncio.gather(h_task, p_task)

    def __post_interaction(self, task: Task, payload: dict):
        for i in range(10):
            try:
                resp = self.session.post('https://discord.com/api/v9/interactions',
                                         json=payload)

                if resp.status_code == 204:
                    break
            except Exception as e:
                logger.error(e)

        else:
            with self._lock:
                self.tasks.remove(task)
                task.callback(TaskCallbackResponse(task=task, error='提交任务失败'))

    def __post_draw(self, task: Task):
        payload = {
            "channel_id": self.channel_id,  # 当前频道浏览器上方有
            "guild_id": self.guild_id,  # 当前频道浏览器上方有
            "session_id": "34a0d78eb9e624d31ac63cff92c2687b",  # 固定即可
            "application_id": "936929561302675456",  # 固定的
            "type": 2,
            'data': {
                "version": "1118961510123847772",  # 固定的
                "id": "938956540159881230",  # command id，固定的
                'name': 'imagine',
                'type': 1,
                'options': [{'type': 3, 'name': 'prompt', 'value': task.prompt}],
                'attachments': []}
        }
        self.__post_interaction(task, payload)

    def __post_upscale(self, task: Task):
        filename = task.reply_msg.attachment_urls[0].split("_")[-1]
        filename = filename.replace(".png", "")
        payload = {
            "type": 3,
            "nonce": random.randint(1142187534726463488, 1143187534726463488),
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 0,
            "message_id": task.reply_msg.msg_id,
            "application_id": "936929561302675456",
            "session_id": "34a0d78eb9e624d31ac63cff92c2687a",
            "data": {
                "component_type": 2,
                "custom_id": f"MJ::JOB::upsample::{task.upscale_index}::{filename}",
            }
        }
        self.__post_interaction(task, payload)

    def _handle_new_task(self, task: Task):
        """
        提交新的任务，用http接口
        """
        if task.task_type == TaskType.DRAW:
            self.__post_draw(task)
        elif task.task_type == TaskType.UPSCALE:
            self.__post_upscale(task)

    def upscale(self, reply_task: TaskCallbackResponse, index: int):
        task = deepcopy(reply_task.task)
        task.task_type = TaskType.UPSCALE
        task.datetime = datetime.now()
        task.upscale_index = index
        task.reply_msg = deepcopy(reply_task.reply_msg)
        self._putted_tasks.put(task)

    def _listen_msg(self):
        pass

    async def __init_ws(self):
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=0, family=socket.AF_INET),
            trace_configs=None,
        )
        kwargs = {
            'proxy_auth': None,
            'proxy': self.proxy,
            'max_msg_size': 0,
            'timeout': 30.0,
            'autoclose': False,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            },
            'compress': 0,
        }
        for i in range(30):
            try:
                ws = await session.ws_connect(
                    self.url,
                    **kwargs
                )
                await self.__login(ws)
                break
            except Exception as e:
                logger.error(e)
                await asyncio.sleep(1)
                continue

    async def __login(self, ws: ClientWebSocketResponse):
        auth = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": random.choice(["windows", "linux", "iOS"]),
                    "$browser": random.choice(["firefox", "chrome", "edge", "safari"]),
                    "$device": random.choice(["pc", "mobile"])
                }
            }
        }

        await ws.send_json(auth)
        hello_message = await ws.receive_json()
        self.heartbeat_interval = hello_message['d']['heartbeat_interval'] / 1000.0
        with self._lock:
            self.ws = ws

    async def __heart(self):
        while True:
            if self.heartbeat_interval and self.ws:
                try:
                    await self.ws.send_json({
                        "op": 1,
                        "d": "null"
                    })
                except Exception as e:
                    logger.error(e)
                await asyncio.sleep(self.heartbeat_interval)

    async def __receive_msg(self):
        data: WSMessage = await self.ws.receive()
        match data.type:
            case WSMsgType.CLOSED:
                await self.__init_ws()
            case WSMsgType.TEXT:
                try:
                    msg = data.json()
                except Exception as e:
                    raise e
                op = msg.get('op')
                data: dict = msg.get('d')
                seq = msg.get('s')
                event = msg.get('t')
                match event:
                    case "MESSAGE_CREATE" | "MESSAGE_UPDATE":
                        content = data.get("content", "")
                        for e in data.get("embeds", []):
                            content += f"\n{e.get('title', '')}\n{e.get('footer', {}).get('text', '')}\n{e.get('description', '')}\n"
                        attachment_urls = [a_data["proxy_url"] for a_data in data.get("attachments", [])]

                        time_str = data.get("timestamp")
                        if time_str:

                            utc_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                            local_timezone = pytz.timezone('Asia/Shanghai')  # 替换为本地时区
                            msg_datetime = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                        else:
                            msg_datetime = datetime.now()
                        new_msg = Message(msg_id=data.get("id"),
                                          content=content,
                                          sender_name=data.get("author", {}).get("username"),
                                          attachment_urls=attachment_urls,
                                          datetime=msg_datetime
                                          )
                        self._handle_new_msg(new_msg)

    async def __pool_event(self):
        await asyncio.sleep(2)
        while True:
            if not self.ws:
                await asyncio.sleep(0.2)
                continue
            try:
                await self.__receive_msg()
            except Exception as e:
                logger.error(e)
