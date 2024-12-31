import time

from nonebot import Bot, on_command
from nonebot.adapters import Event
from nonebot.message import event_preprocessor
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_alconna import UniMsg
from nonebot_plugin_uninfo import get_session
from src.common.bilicard.bilicard import COOKIE_PATH

__plugin_meta__ = PluginMetadata(
    name="B站链接",
    description="B站视频链接解析",
    usage="直接发送B站视频链接即可\n设置B站cookie <cookies>",
)


from src.common.bilicard import bilicard

cached = {}


def check_in_cache(bvid):
    if bvid in cached and time.time() - cached[bvid] < 60:
        return True
    cached[bvid] = time.time()
    return False


@event_preprocessor
async def _(bot: Bot, event: Event):
    session = await get_session(bot, event)
    # 如何跨平台的获取用户的id呢
    is_group = session.scene.is_group
    msg_text = event.get_plaintext()
    # 是否是QQ卡片分享，由于卡片附带了预览效果，如果没有简介或者字幕总结，没必要用机器人再发送一次
    is_from_card = "__from__card" in msg_text
    b32_url = bilicard.check_is_b23(msg_text)
    if b32_url:
        msg_text = await bilicard.b32_to_bv(b32_url[0])

    bvid = bilicard.get_bv_id(msg_text)
    avid = bilicard.get_av_id(msg_text)

    if bvid or avid:
        if bvid and len(bvid) < 6:
            return
        if avid and len(avid) < 6:
            return

        if bvid and check_in_cache(bvid):
            return
        video_info = await bilicard.get_video_info(bvid, avid)

        bvid = video_info.get("bvid", "")
        if check_in_cache(bvid + str(session.group.id) if is_group else str(session.user.id)):
            return
        img = await bilicard.gen_image(video_info)
        summary = await bilicard.get_video_summary_by_ai(video_info["aid"], video_info["cid"])
        # 没有简介内容或者简介等于标题的，且是卡片分享的，而且AI无法总结的就不需要发送了
        if ((len(video_info["desc"]) < 4 or video_info["desc"] == video_info["title"])
                and is_from_card and not summary):
            return
        summary = "AI总结：" + (summary if summary else "此视频不支持")
        url = f"https://bilibili.com/video/{bvid}" if bvid else f"https://bilibili.com/video/av{avid}"
        if img:
            reply_msg = UniMsg.image(img) + \
                        UniMsg.text("简介：" + video_info["desc"] + "\n\n" + summary +
                                            "\n\n" + url)
            await bot.send(event, await reply_msg.export())


set_cookie_cmd = on_command('设置B站cookie', permission=SUPERUSER)

@set_cookie_cmd.handle()
async def set_cookie(args = CommandArg()):
    msg_text = args.extract_plain_text()
    if not msg_text:
        await set_cookie_cmd.finish("请在命令后输入cookie")
    COOKIE_PATH.write_text(msg_text)
    await set_cookie_cmd.finish("设置成功")