from nonebot import on_fullmatch
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import UniMsg

__plugin_meta__ = PluginMetadata(
    name="小视频",
    description="美女短视频",
    usage="随机视频、黑丝视频、白丝视频",
)

girl_video_cmd = on_fullmatch(('小视频', '来点视频', '小姐姐视频', '随机视频'))


@girl_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/zzxjj.php?type=video"
    await girl_video_cmd.finish(await UniMsg.video(url=url).export())


black_socks_video_cmd = on_fullmatch(('黑丝', '黑丝视频', '来点黑丝'))


@black_socks_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/heisis.php?type=video"
    await black_socks_video_cmd.finish(await UniMsg.video(url=url).export())


white_socks_video_cmd = on_fullmatch(('白丝', '白丝视频', '来点白丝'))


@white_socks_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/baisis.php?type=video"
    await white_socks_video_cmd.finish(await UniMsg.video(url=url).export())
