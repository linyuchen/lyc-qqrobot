import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pytz
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys, ChromeOptions
from selenium.webdriver.common.by import By

from config import GFW_PROXY

# from msgplugins.stable_diffusion.sd import trans2en

TIME_OUT = 60
proxy = {"https": GFW_PROXY}


@dataclass()
class Message:
    msg_id: str
    sender_name: str
    datetime: datetime
    content: str = ""
    attachment_urls: list[str] = None


class DiscordClient:

    def __init__(self, url: str, token: str = "", debug_address: str = None, http_proxy: str = ""):
        """
        :param url: 要打开的频道地址，如https://discord.com/channels/1127887388648153118/1127887388648153121
        :param token: discord token
        :param debug_address: 调试地址，如127.0.0.1:9990, 启动Chrome时需要加参数，如chrome.exe --remote-debugging-port=9990 --user-data-dir=d:/
        :param http_proxy: http代理地址，如http://localhost:7890
        """
        super().__init__()
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
                attachment_urls = [a.get_attribute("href").replace("cdn.discordapp.com", "media.discordapp.net") for a in attachment_els]
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
        text_box.send_keys(cmd_args)
        text_box.send_keys(Keys.ENTER)

    def download_imgs(self, img_urls: list[str]) -> list[Path]:
        result: list[Path] = []
        for img_url in img_urls:
            img_path = tempfile.mktemp(".png")
            img_url = img_url.replace("cdn.discordapp.com", "media.discordapp.net") + "?width=546&height=546"
            try_count = 3
            data = ""
            for i in range(try_count):
                try:
                    data = requests.get(img_url, proxies=proxy).content
                    break
                except Exception as e:
                    continue

            if not data:
                raise Exception(f"download {img_url} failed")
            with open(img_path, "wb") as f:
                f.write(data)
                f.close()
            result.append(Path(img_path))
        return result
