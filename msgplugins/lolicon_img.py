import requests

from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("冲", alias=("冲冲冲", "来点色图", "来点涩图"),
            param_len=-1, is_async=True, cmd_group_name="来点色图")
def lolicon_img(msg: GeneralMsg, msg_params: list[str]):
    try:
        api_url = "https://api.lolicon.app/setu/v2?size=regular"
        if msg_params:
            api_url += "&tag=" + "&tag=".join(msg_params)
        data = requests.get(api_url).json()["data"]
        img_url = data[0]["urls"]["regular"]
    except Exception as e:
        return msg.reply(f"图片获取失败 {e}")
    msg.reply(MessageSegment.image(img_url))
