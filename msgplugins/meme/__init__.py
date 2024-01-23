import asyncio
import random
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Callable

from filetype import filetype
from meme_generator import get_memes
from meme_generator.cli import get_meme
from meme_generator.utils import render_meme_list, TextProperties

from config import get_config, set_config
from msgplugins.msgcmd import on_command, CMDPermissions
from qqsdk.message import GroupNudgeMsg, MessageSegment, GroupMsg, GeneralMsg
from .generate import generate


def create_meme_func(key: str, texts: list[str] = None,
                     args: dict[str, any] | Callable[[None], dict] = None,
                     images_len=1, images_reversed=False):
    if not texts:
        texts = []
    if not args:
        args = {}
    if callable(args) and not isinstance(args, dict):
        args = args()

    def meme(msg: GroupNudgeMsg | GroupMsg) -> Path:
        if isinstance(msg, GroupNudgeMsg):
            from_member = msg.from_member
            target_member = msg.target_member
        else:
            from_member = msg.group_member
            target_member = msg.at_member
        new_texts = texts[:]
        for index, text in enumerate(texts):
            new_text = text.replace("{from_name}", from_member.get_name())
            new_text = new_text.replace("{target_name}", target_member.get_name())
            new_texts[index] = new_text

        _meme = get_meme(key)
        loop = asyncio.new_event_loop()
        images = []
        match images_len:
            case 1:
                images = [target_member.avatar.path]
            case 2:
                images = [target_member.avatar.path, from_member.avatar.path]
                if images_reversed:
                    images = images[::-1]
        result = loop.run_until_complete(_meme(images=images, texts=new_texts, args=args))
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
    create_meme_func("hammer"),  # 锤
    create_meme_func("hit_screen"),  # 打穿屏幕
    create_meme_func("hold_tight"),  # 抱紧
    create_meme_func("hug_leg"),  # 抱大腿
    create_meme_func("hutao_bite"),  # 胡桃啃
    create_meme_func("incivilization"),  # 你刚才说的话不礼貌
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
    create_meme_func("chanshenzi", texts=["你那叫喜欢吗？", "你那是馋她身子", "{target_name}下贱！"], images_len=0),
    # 馋身子
    create_meme_func("interview", images_len=2),  # 你刚才说的话不礼貌
    create_meme_func("jiujiu"),
    create_meme_func("karyl_point"),
    create_meme_func("kick_ball"),
    create_meme_func("kirby_hammer"),
    create_meme_func("kiss", images_len=2),
    create_meme_func("klee_eat", images_len=1),
    create_meme_func("knock", images_len=1),
    create_meme_func("listen_music", images_len=1),
    create_meme_func("little_angel", images_len=1),
    create_meme_func("loading", images_len=1),
    create_meme_func("look_flat", images_len=1),
    create_meme_func("look_this_icon", images_len=1),
    create_meme_func("love_you", images_len=1),
    create_meme_func("luoyonghao_say", images_len=0, texts=["{target_name}"]),
    create_meme_func("luxun_say", images_len=0, texts=["{target_name}"]),
    create_meme_func("maikease", images_len=0,
                     texts=["美国前五星上将麦克阿瑟", "曾这样评价道", "如果让我去阻止{target_name}",
                            "那么我宁愿去阻止上帝"]),
    create_meme_func("mihoyo", images_len=1),
    create_meme_func("mourning", images_len=1, args={"black": True}),
    create_meme_func("my_friend", images_len=1, texts=["来点涩图"]),
    create_meme_func("my_wife", images_len=1),
    create_meme_func("need", images_len=1),
    create_meme_func("nekoha_holdsign", images_len=0, texts=["{target_name}"]),
    create_meme_func("nijika_holdsign", images_len=0, texts=["{target_name}"]),
    create_meme_func("no_response", images_len=1),
    create_meme_func("nokia", images_len=0, texts=["{target_name}"]),
    create_meme_func("not_call_me", images_len=0, texts=["{target_name}"]),
    create_meme_func("note_for_leave", images_len=1),
    create_meme_func("oshi_no_ko", images_len=1),
    create_meme_func("overtime", images_len=1),
    create_meme_func("paint", images_len=1),
    create_meme_func("painter", images_len=1),
    create_meme_func("pass_the_buck", images_len=1, texts=["你的！"]),
    create_meme_func("pat", images_len=1),
    create_meme_func("perfect", images_len=1),
    create_meme_func("petpet", images_len=1, args={"circle": True}),
    create_meme_func("play", images_len=1),
    create_meme_func("play_game", images_len=1),
    create_meme_func("police", images_len=1),
    create_meme_func("police1", images_len=1),
    create_meme_func("pound", images_len=1),
    create_meme_func("printing", images_len=1),
    create_meme_func("prpr", images_len=1),
    create_meme_func("punch", images_len=1),
    create_meme_func("raise_image", images_len=1),
    create_meme_func("raise_image", images_len=1),
    create_meme_func("raise_sign", images_len=0, texts=["{target_name}带带我"]),
    create_meme_func("read_book", images_len=1),
    create_meme_func("repeat", images_len=2, texts=["来点涩图"]),
    create_meme_func("rip", images_len=2, images_reversed=True),
    create_meme_func("rip_angrily", images_len=1),
    create_meme_func("rise_dead", images_len=1),
    create_meme_func("roll", images_len=1),
    create_meme_func("rub", images_len=2),
    create_meme_func("safe_sense", images_len=1),
    create_meme_func("scratch_head", images_len=1),
    create_meme_func("scroll", images_len=0, texts=["{target_name}"]),
    create_meme_func("shock", images_len=1),
    create_meme_func("sit_still", images_len=1),
    create_meme_func("smash", images_len=1),
    create_meme_func("step_on", images_len=1),
    create_meme_func("suck", images_len=1),
    create_meme_func("support", images_len=1),
    create_meme_func("symmetric", images_len=1, args={"direction": "left"}),
    create_meme_func("symmetric", images_len=1, args={"direction": "right"}),
    create_meme_func("symmetric", images_len=1, args={"direction": "top"}),
    create_meme_func("symmetric", images_len=1, args={"direction": "bottom"}),
    create_meme_func("tankuku_raisesign", images_len=1),
    create_meme_func("taunt", images_len=1),
    create_meme_func("teach", images_len=1),
    create_meme_func("tease", images_len=1),
    create_meme_func("think_what", images_len=1),
    create_meme_func("throw", images_len=1),
    create_meme_func("throw_gif", images_len=1),
    create_meme_func("thump", images_len=1),
    create_meme_func("thump_wildly", images_len=1),
    create_meme_func("tightly", images_len=1),
    create_meme_func("together", images_len=1),
    create_meme_func("trance", images_len=1),
    create_meme_func("turn", images_len=1),
    create_meme_func("twist", images_len=1),
    # create_meme_func("vibrate", images_len=1),
    create_meme_func("wallpaper", images_len=1),
    create_meme_func("walnut_pad", images_len=1),
    create_meme_func("walnut_zoom", images_len=1),
    create_meme_func("wave", images_len=1),
    create_meme_func("what_I_want_to_do", images_len=1),
    create_meme_func("what_he_wants", images_len=1),
    create_meme_func("why_at_me", images_len=1),
    create_meme_func("windmill_turn", images_len=1),
    create_meme_func("wooden_fish", images_len=1),
    create_meme_func("worship", images_len=1),
)

test_nudge_memes = (
    create_meme_func("rip", images_len=2, images_reversed=True),
)

touch_history = {}  # key: group_qq+'g'+member_qq, value: last_touch_time

CONFIG_KEY_MEME_INTERVAL = "meme_interval"
meme_interval_config: dict = get_config(CONFIG_KEY_MEME_INTERVAL, {})


@on_command("拍一拍",
            alias=("戳一戳", "摸一摸", "拍拍", "摸摸", "戳戳"),
            desc="@群员后发送 拍一拍 生成表情包",
            example="@喵了个咪 拍一拍",
            # desc="手机双击群员头像随机发送表情包",
            param_len=0,
            bind_msg_type=(GroupNudgeMsg, GroupMsg),
            auto_destroy=False,
            is_async=True,
            ignore_at_other=False,
            cmd_group_name="戳一戳表情")
def meme_touch(msg: GroupNudgeMsg | GroupMsg, args: list[str]):
    meme = random.choice(nudge_memes)
    # meme = random.choice(test_nudge_memes)
    # paths = []
    # for meme in nudge_memes:
    #     file_path = meme(msg)
    #     paths.append(file_path)
    # print(paths)
    # member_id = msg.group.qq + "g" + msg.from_member.qq
    # last_time = touch_history.get(member_id, 0)
    # interval = meme_interval_config.get(msg.group.qq, 30)
    # if time.time() - last_time < interval:
    #     return
    # touch_history[member_id] = time.time()
    if isinstance(msg, GroupMsg):
        if not msg.at_member:
            return
    file_path = meme(msg)
    reply_msg = MessageSegment.image_path(file_path)
    msg.reply(reply_msg, quote=False)
    file_path.unlink()


@on_command("设置戳一戳表情频率", param_len=1,
            desc="设置戳一戳表情频率 秒数,如 设置戳一戳表情频率 30",
            bind_msg_type=(GroupMsg,),
            permission=CMDPermissions.GROUP_ADMIN
            )
def set_meme_interval(msg: GroupMsg, params: list[str]):
    interval = params[0]
    if not interval.isdigit():
        return msg.reply("请输入正常的频率，频率为秒数")
    meme_interval_config[msg.group.qq] = int(interval)
    set_config(CONFIG_KEY_MEME_INTERVAL, meme_interval_config)
    msg.reply("戳一戳表情频率设置成功")


@on_command("", cmd_group_name="表情包", ignore_at_other=False)
def meme_generate(msg: GeneralMsg, params: list[str]):
    images = msg.msg_chain.get_image_paths()

    if isinstance(msg, GroupMsg):
        if msg.at_member:
            images.append(msg.at_member.avatar.path)
        images.append(msg.group_member.avatar.path)

    image_path = generate(msg.msg.strip(), images)
    if image_path:
        msg.reply(MessageSegment.image_path(image_path))
        image_path.unlink()


@on_command("表情包列表", alias=("表情列表", ), cmd_group_name="表情包",
            example="表情包列表", desc="查看表情包列表")
def meme_list(msg: GeneralMsg, params: list[str]):
    meme_list_image_bytes_io = render_meme_list([(m, TextProperties()) for m in get_memes()])
    image_path = Path(tempfile.mktemp(suffix=".png"))
    image_path.write_bytes(meme_list_image_bytes_io.getvalue())
    msg.reply(MessageSegment.image_path(image_path), quote=False)


@on_command("表情包详情", alias=("表情详情",), cmd_group_name="表情包", param_len=1,
            example="表情包详情 二次元入口", desc="查看表情包详情")
def meme_info(msg: GeneralMsg, params: list[str]):
    loop = asyncio.new_event_loop()
    keyword = params[0]
    for meme in get_memes():
        if keyword in meme.keywords:
            image_length = f"{meme.params_type.min_images} ~ {meme.params_type.max_images}"
            if meme.params_type.min_images == meme.params_type.max_images:
                image_length = str(meme.params_type.min_images)

            text_length = f"{meme.params_type.min_texts} ~ {meme.params_type.max_texts}"
            if meme.params_type.min_texts == meme.params_type.max_texts:
                text_length = str(meme.params_type.min_texts)
            info = (f"关键字: {','.join(meme.keywords)}\n"
                    f"需要图片数目: {image_length}\n"
                    f"需要文字数目: {text_length}\n")
            preview: BytesIO = loop.run_until_complete(meme.generate_preview())
            preview_ext = filetype.guess_extension(preview.getvalue())
            preview_image_path = Path(tempfile.mktemp(suffix=f".{preview_ext}"))
            preview_image_path.write_bytes(preview.getvalue())
            msg.reply(MessageSegment.text(info) + MessageSegment.image_path(preview_image_path))
            return
