import requests

from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment
from .girlvideo import *


@on_command("票房",
            alias=("电影票房", "票房排名", "票房排行"),
            desc="当前电影票房排名",
            cmd_group_name="票房"
            )
def box_office(msg: GeneralMsg, args: list[str]):
    url = "https://api.yujn.cn/api/piaofang.php?type=json"
    data = requests.get(url).json()
    text = f"{data.get('time')}电影票房排名\n\n"
    for i in data.get('data'):
        text += f"《{i['title']}》: {i['sumBoxDesc']}, {i['releaseInfo']}\n"
    msg.reply(text, at=False, quote=False)
