from msgplugins.msgcmd import on_command, CMDPermissions
from qqsdk.message import GeneralMsg, MessageSegment


@on_command("/send_video",
            param_len=1,
            permission=CMDPermissions.SUPER_ADMIN)
def debug_cmd(msg: GeneralMsg, args: list[str]):
    url = args[0].strip()
    msg.reply(MessageSegment.video_url(url), quote=False, at=False)
