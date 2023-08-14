import dataclasses
import tempfile
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from threading import Thread, Lock
from typing import Callable

import requests
from selenium import webdriver
from selenium.webdriver import Keys, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from msgplugins.stable_diffusion.sd import trans2en
from config import GFW_PROXY
from common.taskpool import TaskPool, Task
from common.utils.baidu_translator import trans, is_chinese

sd_url = 'https://discord.com/channels/1127887388648153118/1127887388648153121'

TIME_OUT = 60
# DEFAULT_PROMPT = "(masterpiece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2),"
DEFAULT_PROMPT = "masterpiece,"
proxy = {"https": GFW_PROXY}
USE_REMOTE_DEBUG = False

webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": GFW_PROXY,
    "sslProxy": GFW_PROXY,
    "proxyType": "manual"
}
options = ChromeOptions()
# chrome.exe --remote-debugging-port=9990 --user-data-dir=d:/
if USE_REMOTE_DEBUG:
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9990")
else:
    # tempdir = tempfile.gettempdir()
    tempdir = tempfile.mkdtemp()
    options.add_argument(f"user-data-dir={tempdir}")
    prefs = {"profile.managed_default_content_settings.images": 2}  # 不显示图片
    options.add_experimental_option("prefs", prefs)


@dataclass()
class Message:
    msg_id: str
    img_list: list[str]


@dataclasses.dataclass()
class DrawTask(Task):
    prompt: str
    callback: Callable[[list[Path]], None]
    img_urls: list[str] = None
    # img_paths: list[Path] = None


class SDDiscord(TaskPool[DrawTask]):
    driver = webdriver.Chrome(options=options)
    if not USE_REMOTE_DEBUG:
        driver.get(url=sd_url)
    username = "linyuchen"
    token = 'MTAxMjQ5NTUxMTA2MTc5NDg0Ng.G0Cus3.1YfxrcY7KGqsx8_KhSUx91c2yGUNWpVyl8bdok'
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
    driver.execute_script(js)
    ready = False

    def __init__(self):
        super().__init__()
        self.finished_messages: list[Message] = []  # 用于存放已经处理过的消息

    def _on_handling_putted(self, task):
        self.__send_text(task.prompt)

    def _on_task_finished(self, task: DrawTask):
        img_paths = self.__download_img(task.img_urls)
        task.callback(img_paths)
    
    def find_msg(self) -> list[Message]:
        result: list[Message] = []
        # 查找消息列表元素
        chat_messages_ele = self.driver.find_element(by=By.CSS_SELECTOR, value='ol[data-list-id="chat-messages"]')
        message_els = chat_messages_ele.find_elements(by=By.CSS_SELECTOR, value='li')

        for msg_ele in message_els:
            try:
                msg_id = msg_ele.get_attribute("id").split("-")[-1]
                txt_ele = msg_ele.find_element(by=By.ID, value=f"message-content-{msg_id}")
                # sd的机器人消息，第一个span是@谁，用这个来判断是不是回复自己,可能有更好的方法识别回复自己的消息
                at_txt = txt_ele.find_element(by=By.TAG_NAME, value="span").text
            except:
                continue
            # print(at_txt)
            # 如果是回复自己的消息，就把图片内容提取出来
            if at_txt.strip() == f"@{self.username}":
                message = Message(msg_id=msg_id, img_list=[])
                attachment_el = msg_ele.find_element(by=By.ID, value=f"message-accessories-{msg_id}").find_element(
                    by=By.TAG_NAME, value="div")
                img_list = attachment_el.find_elements(by=By.TAG_NAME, value="a")
                for img_ele in img_list:
                    # todo: 需要在url上加上分辨率，不然太大了
                    href = img_ele.get_attribute("href")
                    message.img_list.append(href)
                result.append(message)
        self._lock.acquire()
        if message_els and not self.ready:
            # 第一次获取到消息
            # 把获取到的消息放到finished_messages里面
            # 这样就不会把第一次获取到的消息当做结果返回给用户
            self.ready = True
            self.finished_messages = result
        self._lock.release()
        return result

    def run(self):
        # 处理discord的回复
        while True:
            time.sleep(1)
            try:
                messages = self.find_msg()
            except:
                # traceback.print_exc()
                continue
            messages.reverse()  # 反转一下，这样就能先判断最新的消息

            for msg in messages:
                msg: Message
                if list(filter(lambda m: m.msg_id == msg.msg_id, self.finished_messages)):
                    continue

                # 处理获取到的新回复
                self._lock.acquire()
                self.finished_messages.append(msg)
                self._lock.release()
                try:
                    if self.handling_tasks:
                        task = self.handling_tasks[0]
                        task.finished = True
                        task.img_urls = msg.img_list
                except:
                    pass

    def draw(self, text: str, callback: Callable[[list[Path]], None]):
        while not self.ready:
            time.sleep(1)
        if is_chinese(text):
            text = trans(text)
        task = DrawTask(prompt=text, callback=callback)
        self._join_task(task)

    def __download_img(self, img_urls: list[str]) -> list[Path]:
        result: list[Path] = []
        for img_url in img_urls:
            img_path = tempfile.mktemp(".png")
            img_url = img_url.replace("cdn.discordapp.com", "media.discordapp.net") + "?width=546&height=546"
            try_count = 0
            while True:
                try:
                    data = requests.get(img_url, proxies=proxy).content
                    try_count = 0
                    break
                except:
                    try_count += 1
                    if try_count > 3:
                        break
            if try_count > 3:
                continue
            with open(img_path, "wb") as f:
                f.write(data)
                f.close()
            result.append(Path(img_path))
        return result

    def __send_text(self, text):
        text_box = self.driver.find_element(by=By.CSS_SELECTOR, value='div[role=textbox]')
        text_box.send_keys("/dream")
        time.sleep(1)
        while True:
            try:
                cmds = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[data-text-variant="text-xs/normal"]')
                # for c in cmds:
                #     print(c.text)
                if len(cmds) > 1:
                    break
            except:
                pass
        text_box.send_keys(Keys.ENTER)
        text_box.send_keys(DEFAULT_PROMPT + text)
        text_box.send_keys(Keys.ENTER)


if __name__ == '__main__':
    sd = SDDiscord()
    sd.start()
    while True:
        _text = input("text:")
        if _text == 'exit':
            break
        sd.draw(_text, print)
