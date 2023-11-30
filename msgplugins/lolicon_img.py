import tempfile
from pathlib import Path

import requests

from common.utils.nsfw_detector import nsfw_detect
from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("冲", alias=("色图", "涩图", "冲冲冲", "来点色图", "来点涩图"),
            desc="来点色图",
            param_len=-1, is_async=True, cmd_group_name="来点色图")
def lolicon_img(msg: GeneralMsg, msg_params: list[str]):
    try:
        api_url = "https://api.lolicon.app/setu/v2?size=medium"
        if msg_params:
            api_url += "&tag=" + "&tag=".join(msg_params)
        data = requests.get(api_url).json()["data"]
        img_url = data[0]["urls"]["medium"]
        img_data = requests.get(img_url).content
        img_path = tempfile.mktemp(".png")
        img_path = Path(img_path)
        with open(img_path, "wb") as f:
            f.write(img_data)
        if nsfw_detect(img_path):
            img_path.unlink()
            return msg.reply("图片违规，已删除~")
    except Exception as e:
        return msg.reply(f"图片获取失败 {e}")

    msg.reply(MessageSegment.image_path(img_path))
    img_path.unlink()
