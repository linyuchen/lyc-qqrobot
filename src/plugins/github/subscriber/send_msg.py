from nonebot import get_bots
from src.db.models.github import Subscriber
from nonebot_plugin_alconna import UniMsg
from nonebot.adapters.onebot.v11.adapter import Adapter as OB11Adapter, Bot as OB11Bot
from nonebot.adapters.telegram.adapter import Adapter as TGAdapter, Bot as TGBot


async def send_msg_to_subscribers(subscribers: list[Subscriber], msg: UniMsg):
    bots = get_bots().values()
    msg.send()
    for s in subscribers:
        for bot in bots:
            if bot.adapter.get_name() == OB11Adapter.get_name() == s.platform:
                bot: OB11Bot
                await bot.send_group_msg(group_id=int(s.group_id), message=await msg.export(bot=bot))
            elif bot.adapter.get_name() == TGAdapter.get_name() == s.platform:
                bot: TGBot
                await bot.send_to(chat_id=int(s.group_id), message=await msg.export(bot=bot))
