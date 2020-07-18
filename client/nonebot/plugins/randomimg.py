import requests
import random
import os
from nonebot import on_command, CommandSession
from nonebot.message import MessageSegment


@on_command("冲", aliases=["冲冲冲", "来点涩图"], only_to_me=False, shell_like=True)
async def random_img(session: CommandSession):
    IMG_ROOT_PATH = "f:\\randomimg"
    file_name = random.choice(os.listdir(IMG_ROOT_PATH))
    await session.send(MessageSegment.image("file://" + os.path.join(IMG_ROOT_PATH, file_name)))
    res = requests.get("https://api.lolicon.app/setu/?apikey=733165695f1284f958d480").json()
    if res["code"] == 0:
        img_info = res["data"][0]
        pid = img_info["pid"]
        url = img_info["url"]
        file_path = os.path.join(IMG_ROOT_PATH, os.path.basename(url))
        if not os.path.exists(file_path):
            open(file_path, "wb").write(requests.get(url).content)
        await session.send(MessageSegment.image("file://" + file_path))
