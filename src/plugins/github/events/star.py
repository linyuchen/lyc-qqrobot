
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
    repo = event.payload.repository
    await send_msg_to_subscribers(subscribers, UniMsg.text(f'{event.payload.sender.name} stared {repo.owner}/{repo.name}, {repo.stargazers_count} stars'))
    await on_stared.finish()
