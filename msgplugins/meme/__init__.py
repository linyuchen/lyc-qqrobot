import asyncio
import random
import tempfile
from functools import reduce
from pathlib import Path
from typing import Callable, Dict, Any

from filetype import filetype
from meme_generator.cli import get_meme

from msgplugins.msgcmd import on_command
from qqsdk.message import GroupNudgeMsg, MessageSegment


def create_meme_func(key: str, texts: list[str] = None,
                     args: dict[str, str] | Callable[[None], dict] = None,
                     images_len=1):
    if not texts:
        texts = []
    if not args:
        args = {}
    if callable(args) and not isinstance(args, dict):
        args = args()

    def meme(msg: GroupNudgeMsg) -> Path:
        for index, text in enumerate(texts):
            new_text = text.replace("{from_name}", msg.from_member.get_name())
            new_text = new_text.replace("{target_name}", msg.target_member.get_name())
            texts[index] = new_text
        _meme = get_meme(key)
        loop = asyncio.new_event_loop()
        images = []
        match images_len:
            case 1:
                images = [msg.target_member.avatar.path]
            case 2:
                images = [msg.target_member.avatar.path, msg.from_member.avatar.path]
        result = loop.run_until_complete(_meme(images=images, texts=texts, args=args))
        content = result.getvalue()
        ext = filetype.guess_extension(content)
        file_path = tempfile.mktemp(suffix=f".{ext}")
        file_path = Path(file_path)
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

    return meme


nudge_memes = (
    create_meme_func("acg_entrance"),  # 二次元入口
    create_meme_func("always", args={"mode": "loop"}),  # 要我一直吗
    create_meme_func("anti_kidnap"),  # 远离
    create_meme_func("applaud"),  # 鼓掌
    create_meme_func("back_to_work"),  # 继续打工
    create_meme_func("beat_head"),  # 打头
    create_meme_func("bite"),  # 啃
    create_meme_func("blood_pressure"),  # 高血压
    create_meme_func("bocchi_draft"),  # 波奇手稿
    create_meme_func("caoshen_bite"),  # 草神啃
    create_meme_func("capoo_draw"),  # 咖波画
    create_meme_func("capoo_rip"),  # 咖波撕
    create_meme_func("capoo_rub"),  # 咖波蹭
    create_meme_func("capoo_strike"),  # 咖波头槌
    create_meme_func("charpic"),  # 字符画头像
    create_meme_func("chase_train"),  # 追火车
    create_meme_func("confuse"),  # 思考，妈妈生的
    create_meme_func("coupon"),  # 陪睡券
    create_meme_func("cover_face"),  # 捂脸
    create_meme_func("divorce"),  # 离婚协议
    create_meme_func("dog_of_vtb"),  # 管人痴
    create_meme_func("dont_go_near"),  # 不要靠近
    create_meme_func("dont_touch"),  # 别碰这东西
    create_meme_func("eat"),  # 吃
    create_meme_func("fill_head"),  # 满脑子都是他
    create_meme_func("flash_blind"),  # 闪屏
    create_meme_func("funny_mirror"),  # 哈哈镜
    create_meme_func("garbage"),  # 垃圾桶
    create_meme_func("genshin_start"),  # 原神启动
    create_meme_func("fencing", images_len=2),  # 两熊猫打架
    create_meme_func("crawl", args=lambda: {"number": random.randint(1, 92)}),  # 爬
    create_meme_func("alike", args={"model": "loop"}),  # 永远喜欢
    create_meme_func("bubble_tea", args={"position": "right"}),  # 右手奶茶
    create_meme_func("bubble_tea", args={"position": "left"}),  # 左手奶茶
    create_meme_func("bubble_tea", args={"position": "both"}),  # 双手奶茶
    create_meme_func("anya_suki", texts=["{from_name}喜欢{target_name}"]),  # 阿尼亚喜欢
    create_meme_func("ask", texts=["{target_name}"]),  # 让xx告诉你吧
    create_meme_func("douyin", texts=["{target_name}"], images_len=0),  # 让xx告诉你吧
    create_meme_func("fanatic", texts=["{target_name}"], images_len=0),  # 狂热粉
    create_meme_func("follow", texts=["{target_name}"]),  # 关注了你
    create_meme_func("chanshenzi", texts=["你那叫喜欢吗？", "你那是馋她身子", "{target_name}下贱！"], images_len=0),  # 馋身子
)


@on_command("",
            bind_msg_type=(GroupNudgeMsg, ),
            auto_destroy=False,
            is_async=True,
            cmd_group_name="戳一戳表情")
def meme_touch(msg: GroupNudgeMsg, args: list[str]):
    meme = random.choice(nudge_memes)
    # paths = []
    # for meme in nudge_memes:
    #     file_path = meme(msg)
    #     paths.append(file_path)
    # print(paths)
    file_path = meme(msg)
    reply_msg = MessageSegment.image_path(file_path)
    msg.reply(reply_msg)
    file_path.unlink()
