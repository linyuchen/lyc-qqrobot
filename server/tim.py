import base64
import time
import queue
import threading
import traceback
from enum import Enum
from io import BytesIO
from typing import TypedDict

import win32api
import win32clipboard
import win32con
import win32gui
from PIL import Image
from pywinauto import keyboard
from flask import Flask, request


TEXT_MAX_LEN = 3000


class MsgType(Enum):
    TEXT = "Plain"
    IMAGE = "Image"


class MessageData(TypedDict):
    type: MsgType
    data: str


class Message(TypedDict):
    qq_group_name: str
    data: list[MessageData]


def paste(data, is_image):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
    except:
        paste(data, is_image)
        return
    try:
        if is_image:
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        else:
            if len(data) > TEXT_MAX_LEN:
                data = data[:TEXT_MAX_LEN]
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
    except:
        paste(data, is_image)
        return
    # keyboard.send_keys("^v")  # 这个在Hyper-V虚拟机中不好使
    win32api.keybd_event(17, 0, 0, 0)                           # ctrl的键位码是17
    win32api.keybd_event(86, 0, 0, 0)                           # v的键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

    try:
        win32clipboard.CloseClipboard()
    except:
        pass


def send_msg(msg: Message):
    interval = 1
    window_handle = win32gui.FindWindow(None, msg["qq_group_name"])
    win32gui.SetForegroundWindow(window_handle)
    time.sleep(interval)

    for msg_data in msg["data"]:
        if msg_data.get("type") == MsgType.TEXT.value:
            text = msg_data["data"]
            paste(text, False)
        elif msg_data.get("type") == MsgType.IMAGE.value:
            image_data = base64.decodebytes(msg_data["data"].encode("utf-8"))
            fp = BytesIO(image_data)
            im = Image.open(fp)
            output = BytesIO()
            im.save(output, format="BMP")
            data = output.getvalue()[14:]
            paste(data, True)
            time.sleep(1)
        time.sleep(interval)

    keyboard.send_keys("{ENTER}")


# 新建一个flask app，监听http请求，然后获取post的数据，然后调用send_msg函数


app = Flask(__name__)

# 创建一个队列对象
message_queue = queue.Queue()


@app.route('/', methods=['POST'])
def handle_post():
    # 解析 POST 请求中的 JSON 数据
    data = request.get_json()
    # 将 JSON 数据转换为 Message 类型
    # if data.get("key") == "linyuchen":
    message = Message(**data)
    # 将消息放入队列中
    message_queue.put(message)
    # 返回响应
    return 'OK'


def handle_queue():
    while True:
        message = message_queue.get()
        try:
            send_msg(message)
        except:
            traceback.print_exc()
        time.sleep(0.1)


# 创建一个新线程，用于处理消息队列
queue_thread = threading.Thread(target=handle_queue)
# queue_thread.daemon = True
queue_thread.start()

if __name__ == '__main__':
    test_msg = Message(qq_group_name="test group", data=[{"type": MsgType.TEXT, "data": "hello"}])
    # send_msg("机器人test", msg)
    # image_base64 = base64.b64encode(open("test.jpg", "rb").read()).decode("utf-8")
    # test_msg = Message(qq_group_name="test group",
    #                    data=[
    #                        {"type": MsgType.TEXT, "data": "hellokitty"},
    #                        {"type": MsgType.IMAGE, "data": image_base64},
    #                        {"type": MsgType.TEXT, "data": "hellokitty"},
    #                    ])
    # send_msg(test_msg)
app.run(host='0.0.0.0', port=8088)
