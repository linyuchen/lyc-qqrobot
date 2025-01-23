
from nonebot import on_type, Bot
from nonebot.adapters.github import StarCreated, StarDeleted, Event
from nonebot_plugin_alconna import UniMsg

from src.plugins.github.subscriber.depends import Subscribers
from src.plugins.github.subscriber.send_msg import send_msg_to_subscribers

on_stared = on_type(
    (StarCreated,), block=True
)



@on_stared.handle()
async def handle_stared(event: StarCreated, subscribers: Subscribers):
    print(event, subscribers)
    await send_msg_to_subscribers(subscribers, UniMsg.text('stared'))
    await on_stared.finish()
