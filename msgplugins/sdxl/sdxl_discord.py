import tempfile
import time
import traceback
from dataclasses import dataclass
from queue import Queue
from threading import Thread, Lock

import requests
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from msgplugins.stable_diffusion.sd import trans2en
from config import GFW_PROXY

sd_url = 'https://discord.com/channels/1002292111942635562/1101178553900478464'

TIME_OUT = 60
# DEFAULT_PROMPT = "(masterpiece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2),"
DEFAULT_PROMPT = "masterpiece,"
proxy = {"https": GFW_PROXY}

webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": GFW_PROXY,
    "sslProxy": GFW_PROXY,
    "proxyType": "manual"
}
options = Options()
tempdir = tempfile.gettempdir()
options.add_argument(f"user-data-dir={tempdir}")


@dataclass()
class Message:
    msg_id: str
    img_list: list[str]


class SDDiscord(Thread):
    driver = webdriver.Chrome(options=options)
    driver.get(url=sd_url)
    username = "linyuchen"
    token = 'OTcxNjU4ODc5MzM3MzkwMTEx.Gt5JCd.iuJrUQwSSeZT9f9Tsc-u2bJy2LbhotwbeNTL3s'
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
    is_first = True

    def __init__(self):
        super().__init__()
        self.messages = []
        self.res_queue = Queue(maxsize=1)  # 用于存放结果
        self.req_queue = Queue(maxsize=1)  # 用于存放请求
        self.lock = Lock()

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
        return result

    def run(self):
        time.sleep(60)
        while True:
            time.sleep(1)
            try:
                messages = self.find_msg()
            except:
                # traceback.print_exc()
                continue
            messages.reverse()
            self.lock.acquire()
            if self.is_first:
                self.messages = messages
                self.is_first = False
                self.lock.release()
                continue
            self.lock.release()
            for msg in messages:
                if list(filter(lambda m: m.msg_id == msg.msg_id, self.messages)):
                    continue
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                try:
                    self.res_queue.put(msg, timeout=1)
                except:
                    pass
            # print(self.messages)
            # self.driver.refresh()

    def draw(self, text: str) -> list[str]:
        try:
            # text = trans2en(text)
            self.req_queue.put(text, timeout=TIME_OUT)
            self.__send_text(text)
            res = self.res_queue.get(timeout=TIME_OUT)
            self.req_queue.get(timeout=1)
            return self.__download_img(res)
        except:
            try:
                self.res_queue.get(timeout=1)
            except:pass
            try:
                self.req_queue.get(timeout=1)
            except:pass
            traceback.print_exc()
            return []

    def __download_img(self, msg: Message) -> list[str]:
        result = []
        for img_url in msg.img_list:
            img_path = tempfile.mktemp(".png")
            # img_url = img_url.replace("cdn.discordapp.com", "media.discordapp.net") + "?width=546&height=546"
            data = requests.get(img_url, proxies=proxy).content
            with open(img_path, "wb") as f:
                f.write(data)
            result.append(img_path)
            # 只保存一张
            continue
        return result

    def __send_text(self, text):
        text_box = self.driver.find_element(by=By.CSS_SELECTOR, value='div[role=textbox]')
        text_box.send_keys("/dream")
        time.sleep(2)
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
        _res = sd.draw(_text)
        print(_res)
