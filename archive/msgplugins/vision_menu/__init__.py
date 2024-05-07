from msgplugins.msgcmd.cmdaz import on_command
from qqsdk.message import MessageSegment, GeneralMsg, MsgHandler
from .util import create_menu_image


@on_command("菜单",
            alias=("help", "功能", "帮助"),
            param_len=0, desc="菜单", ignore_at_other=True)
def help_menu(msg: GeneralMsg, params: list[str]):
    if msg.quote_msg:
        return
    menu_list = []
    handlers: list[MsgHandler] = msg.qq_client.msg_handlers[:]
    handlers.sort(key=lambda x: x.name)
    for handler in handlers:
        if not handler.desc:
            continue
        if not handler.check_enabled():
            continue
        menu_list.append([handler.cmd_name, handler.desc, handler.example])
    menu_image_path = create_menu_image(menu_list)
    msg.reply(MessageSegment.image_path(menu_image_path))
