import abc
import asyncio
import random
import socket
import tempfile
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import aiohttp
import pytz
import requests
from aiohttp import ClientWebSocketResponse, WSMessage, WSMsgType
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys, ChromeOptions
from selenium.webdriver.common.by import By

from common.logger import logger

# from msgplugins.stable_diffusion.sd import trans2en

TIME_OUT = 60


@dataclass()
class Attachment:
    url: str  # cnd.discordapp.com开头的，不能分享给别人查看
    proxy_url: str  # media.discordapp.net开头的，可以分享给别人查看
    filename: str
    size: int  # 字节
    height: int | None = None
    width: int | None = None


@dataclass()
class Message:
    origin_data: dict  # 原始消息数据
    msg_id: str
    sender_name: str
    datetime: datetime
    content: str = ""
    attachment_urls: list[str] = field(default_factory=list)
    attachments: list[Attachment] = field(default_factory=list)
    read = False


class DiscordWebsocketClientBase:

    def __init__(self, token: str, channel_id: str, guild_id: str, proxy: str = None):
        self.token = token
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.url = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.heartbeat_interval = 0
        self.proxy = proxy
        self.ws: ClientWebSocketResponse | None = None
        self.session = requests.Session()
        self.session.headers.update({'Authorization': self.token})
        self.session.proxies.update({'http': self.proxy, 'https': self.proxy})
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = threading.Thread(target=loop.run_until_complete, args=(self.start(),), daemon=True)
        thread.start()

    async def start(self):
        await self.__init_ws()
        h_task = asyncio.create_task(self.__heart())
        p_task = asyncio.create_task(self.__pool_event())
        await asyncio.gather(h_task, p_task)

    def _post_interaction(self, payload: dict):
        for i in range(10):
            try:
                resp = self.session.post('https://discord.com/api/v9/interactions',
                                         json=payload)

                if resp.status_code == 204:
                    break
            except Exception as e:
                logger.error(e)

        else:
            logger.error(f"post interaction failed, {payload}")

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
        while True:
            try:
                logger.debug(f"discord重连...")
                ws = await session.ws_connect(
                    self.url,
                    **kwargs
                )
                await self.__login(ws)
                logger.debug(f"discord重连成功")
                break
            except Exception as e:
                logger.debug(f"discord重连失败{e}")
                await asyncio.sleep(1)

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
                    await self.__init_ws()
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

                        attachment_urls = []
                        attachments = []
                        attachment_datas = data.get("attachments", [])
                        """
                        {'width': 256, 
                        'url': 'https://cdn.discordapp.com/attachments/1127887388648153121/1143808736423596042/2cc56801-852a-417d-b9fc-cbe355b4ea0f_grid_0.webp', 
                        'size': 17676, 
                        'proxy_url': 'https://media.discordapp.net/attachments/1127887388648153121/1143808736423596042/2cc56801-852a-417d-b9fc-cbe355b4ea0f_grid_0.webp', 
                        'id': '1143808736423596042', 
                        'height': 512, 
                        'filename': '2cc56801-852a-417d-b9fc-cbe355b4ea0f_grid_0.webp', 
                        'content_type': 'image/webp'}
                        """
                        for attachment_data in attachment_datas:
                            attachments.append(Attachment(
                                url=attachment_data.get("url", ""),
                                proxy_url=attachment_data.get("proxy_url", ""),
                                filename=attachment_data.get("filename", ""),
                                size=attachment_data.get("size", 0),
                                height=attachment_data.get("height"),
                                width=attachment_data.get("width"),
                            ))
                            attachment_urls.append(attachment_data["proxy_url"])

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
                                          attachments=attachments,
                                          datetime=msg_datetime,
                                          origin_data=data
                                          )
                        logger.debug(f"MJ收到新消息{new_msg.content}")
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

    @abc.abstractmethod
    def _handle_new_msg(self, new_msg: Message):
        pass


class DiscordSeleniumClient:

    def __init__(self, url: str, token: str = "", debug_address: str = None, http_proxy: str = ""):
        """
        :param url: 要打开的频道地址，如https://discord.com/channels/1127887388648153118/1127887388648153121
        :param token: discord token
        :param debug_address: 调试地址，如127.0.0.1:9990, 启动Chrome时需要加参数，如chrome.exe --remote-debugging-port=9990 --user-data-dir=d:/
        :param http_proxy: http代理地址，如http://localhost:7890
        """
        self.http_proxy = http_proxy
        if http_proxy:
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": http_proxy,
                "sslProxy": http_proxy,
                "proxyType": "manual"
            }
        options = ChromeOptions()
        if debug_address:
            # chrome.exe --remote-debugging-port=9990 --user-data-dir=d:/
            options.add_experimental_option("debuggerAddress", debug_address)
        else:
            # tempdir = tempfile.gettempdir()
            tempdir = tempfile.gettempdir()
            options.add_argument(f"user-data-dir={tempdir}")
            prefs = {"profile.managed_default_content_settings.images": 2}  # 不显示图片
            options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)
        if not debug_address:
            self.driver.get(url=url)
        if token:
            self.set_token(token)
        self.ready = False
        self.finished_messages: list[Message] = []  # 用于存放已经处理过的消息
        self.start_time = datetime.now()

    def set_token(self, token):
        # 注入token
        js = f"""
            const token = "{token}";
            setInterval(() => {{
                document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
            }}, 50);
            setTimeout(() => {{
                location.reload();
            }}, 2500);
        """

        self.driver.execute_script(js)

    def get_msgs(self) -> list[Message]:
        result: list[Message] = []
        # 查找消息列表元素
        try:
            chat_messages_ele = self.driver.find_element(by=By.CSS_SELECTOR, value='ol[data-list-id="chat-messages"]')
            message_els = chat_messages_ele.find_elements(by=By.CSS_SELECTOR, value='li')
        except NoSuchElementException:
            return result
        msg_sender_name = None
        msg_datetime = None
        for msg_ele in message_els:
            try:
                msg_id = msg_ele.get_attribute("id").split("-")[-1]
            except Exception as e:
                msg_id = None
                continue

            # 获取发送者名字
            try:
                msg_sender_ele = msg_ele.find_element(by=By.CSS_SELECTOR, value="span[id^='message-username'] > span")
                msg_sender_name = msg_sender_ele.text
            except Exception:
                # 没有找到的可能是消息合并，需要在上一条消息中查找
                pass

            # 消息时间
            try:
                time_str = msg_ele.find_element(by=By.TAG_NAME, value="time").get_attribute("datetime")
            except Exception:
                # 没有找到的可能是消息合并，需要在上一条消息中查找
                pass
            else:
                utc_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                local_timezone = pytz.timezone('Asia/Shanghai')  # 替换为本地时区
                msg_datetime = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                # if msg_datetime < self.start_time:
                #     continue
            # 消息的文字内容元素
            try:
                msg_content_ele = msg_ele.find_element(by=By.ID, value=f"message-content-{msg_id}")
                msg_content = msg_content_ele.text
            except Exception:
                msg_content = ""
            if not msg_content:
                try:
                    article_ele = msg_ele.find_element(by=By.TAG_NAME, value="article")
                    msg_content = article_ele.text
                except NoSuchElementException:
                    msg_content = ""

            # 附件元素
            try:
                # attachment_el = msg_ele.find_element(by=By.XPATH,
                #                                      value=f"//*[starts-with(@class, 'mediaAttachmentsContainer')]")
                attachment_el = msg_ele.find_element(by=By.ID, value=f"message-accessories-{msg_id}")
                attachment_els = attachment_el.find_elements(by=By.TAG_NAME, value="a")
                attachment_urls = [a.get_attribute("href").replace("cdn.discordapp.com", "media.discordapp.net") for a
                                   in attachment_els]
                attachment_urls = list(filter(bool, attachment_urls))
            except Exception:
                # print(NoSuchElementException("没有找到附件"))
                attachment_el = None
                attachment_urls = []

            result.append(Message(msg_id=msg_id,
                                  sender_name=msg_sender_name,
                                  datetime=msg_datetime,
                                  content=msg_content,
                                  attachment_urls=attachment_urls
                                  ))
        return result

    def send_cmd(self, cmd_name: str, cmd_args: str):
        text_box = self.driver.find_element(by=By.CSS_SELECTOR, value='div[role=textbox]')
        text_box.send_keys(f"{cmd_name}")
        while True:
            try:
                cmds = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[data-text-variant="text-xs/normal"]')
                if len(cmds) > 1:
                    break
            except NoSuchElementException:
                pass
            time.sleep(0.5)
        text_box.send_keys(Keys.ENTER)
        time.sleep(0.5)
        text_box.send_keys(cmd_args)
        text_box.send_keys(Keys.ENTER)


def download_images(img_urls: list[str],
                    http_proxy="",
                    compress_width: int = 546,
                    compress_height: int = 546) -> list[Path]:
    result: list[Path] = []
    logger.debug(f"download images: {img_urls}")
    start_time = time.time()
    for img_url in img_urls:
        img_path = tempfile.mktemp(".png")
        if compress_width and compress_height:
            symbol_q = "" if "?" in img_url else "?"
            symbol_and = "" if img_url.endswith("&") else "&"
            img_url = img_url + symbol_q + symbol_and + f"width={compress_width}&height={compress_height}"
            img_url = img_url.replace("cdn.discordapp.com",
                                      "media.discordapp.net")
        try_count = 10
        data = ""

        for i in range(try_count):
            try:
                data = requests.get(img_url,
                                    proxies={"http": http_proxy, "https": http_proxy} if http_proxy else {}).content
                break
            except Exception as e:
                continue

        if not data:
            raise Exception(f"download {img_url} failed")
        with open(img_path, "wb") as f:
            f.write(data)
            f.close()
        result.append(Path(img_path))
    end_time = time.time()
    logger.debug(f"download images cost: {int(end_time - start_time)}s")
    if not result:
        logger.error(f"download images failed: {img_urls}")
    return result
