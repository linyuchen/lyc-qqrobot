from msgplugins.msgcmd import on_command
from qqsdk.message import GeneralMsg, MessageSegment
from .browser_screenshot import search_baidu


@on_command("百度",
            param_len=1,
            desc="百度 搜索内容",
            cmd_group_name="百度"
            )
def baidu(msg: GeneralMsg, params: list[str]):
    """
    百度搜索
    """
    img_path = search_baidu(params[0])
    msg.reply(MessageSegment.image_path(img_path))
    img_path.unlink()
