import requests
from config import VITS_HTTP_API

root_url = VITS_HTTP_API
session = requests.Session()
session.timeout = 10


def tts(text):
    res_base64 = session.post(root_url + "/tts/tencent", json={"text": text, "speaker": "可莉"}).json()
    return res_base64.get("data")


if __name__ == '__main__':
    print(tts("测试"))
