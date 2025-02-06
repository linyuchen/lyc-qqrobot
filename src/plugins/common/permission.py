from nonebot import get_driver, Bot
from nonebot.internal.adapter import Event
from nonebot_plugin_uninfo import get_session


def check_super_user(user_id: str):
    return user_id in get_driver().config.superusers


async def check_group_admin(bot: Bot, event: Event):
    session = await get_session(bot, event)

    if not session.scene.is_group:
        return check_super_user(str(session.user.id))
    else:
        if session.adapter.value == 'OneBot V11':
            member_info = await bot.get_group_member_info(group_id=session.group.id, user_id=session.user.id)
            is_admin = member_info.get('role') in ['admin', 'owner']
        else:
            # todo: add other platform support
            is_admin = False
        return check_super_user(str(session.user.id)) or is_admin
