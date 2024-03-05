from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("来点视频",
            alias=("小姐姐视频", "来点随机视频"),
            desc="发送随机小视频",
            cmd_group_name="随机小视频"
            )
def girl_video(msg: GeneralMsg, args: list[str]):
    url = "http://api.yujn.cn/api/zzxjj.php?type=video"
    msg.reply(MessageSegment.video_url(url), at=False, quote=False)


@on_command("黑丝视频",
            alias=("来点黑丝视频", "黑丝"),
            desc="发送随机黑丝小视频",
            cmd_group_name="随机小视频"
            )
def black_socks_video(msg: GeneralMsg, args: list[str]):
    url = "http://api.yujn.cn/api/heisis.php?type=video"
    msg.reply(MessageSegment.video_url(url), at=False, quote=False)


@on_command("白丝视频",
            alias=("来点白丝丝视频", "白丝"),
            desc="发送随机白丝小视频",
            cmd_group_name="随机小视频"
            )
def white_socks_video(msg: GeneralMsg, args: list[str]):
    url = "http://api.yujn.cn/api/baisis.php?type=video"
    msg.reply(MessageSegment.video_url(url), at=False, quote=False)
