import subprocess
import tempfile
from pathlib import Path
from pprint import pprint
import gradio_client
import requests
from gradio_client.utils import encode_url_or_file_to_base64

from config import VITS_HTTP_API

root_url = VITS_HTTP_API
session = requests.Session()
session.timeout = 10

client = gradio_client.Client("zomehwh/vits-uma-genshin-honkai")


def tts(text):
    # res_base64 = session.post(root_url + "/tts/tencent", json={"text": text, "speaker": "可莉"}).json()
    # return res_base64.get("data")
    res = client.predict(text, "中文", "可莉", 0.6, 0.66, 1.2, fn_index=0)
    wav_path = res[1]
    pcm_path = tempfile.mktemp(suffix=".pcm")
    silk_path = tempfile.mktemp(suffix=".silk")
    current_path = Path(__file__).parent
    subprocess.call(f"{current_path}/ffmpeg -y -i {wav_path} -f s16le -ar 24000 -ac 1 {pcm_path}")
    subprocess.call(f"{current_path}/silk_v3_encoder.exe {pcm_path} {silk_path} -tencent")
    data = encode_url_or_file_to_base64(silk_path)
    return data


if __name__ == '__main__':
    print(tts("测试"))
    # pprint(rs)
