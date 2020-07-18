import os
import requests
from nonebot import on_command, CommandSession
from nonebot.message import MessageSegment


@on_command("来点涩图", aliases=["涩图"], only_to_me=False, shell_like=False)
async def setu(session: CommandSession):
    # msg = MessageSegment.image("http://i.pixiv.cat/img-original/img/2017/10/14/00/25/45/65419898_p0.png")
    # print(msg)
    # await session.send(msg)
    res = requests.get("https://api.lolicon.app/setu/?apikey=733165695f1284f958d480").json()
    if res["code"] == 0:
        img_info = res["data"][0]
        pid = img_info["pid"]
        url = img_info["url"]
        file_path = "G:\\randomimg\\" + os.path.basename(url)
        if not os.path.exists(file_path):
            open(file_path, "wb").write(requests.get(url).content)
    # print(res)
        await session.send(MessageSegment.image("file://" + file_path))

