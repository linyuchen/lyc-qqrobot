import random
import os
from nonebot import on_command, CommandSession
from nonebot.message import MessageSegment


@on_command("冲", aliases=["冲冲冲"], only_to_me=False, shell_like=True)
async def random_img(session: CommandSession):
    IMG_ROOT_PATH = "d:\\randomimg"
    file_name = random.choice(os.listdir(IMG_ROOT_PATH))
    await session.send(MessageSegment.image("file://" + os.path.join(IMG_ROOT_PATH, file_name)))
