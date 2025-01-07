"""
将OneBot V11 的 message_sent 事件转成 message 事件，
从而能够将自己发送的消息当做普通消息处理。
"""

from nonebot.internal.adapter import Event
from nonebot.message import event_preprocessor
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Bot, MessageEvent


@event_preprocessor
async def _(bot: Bot, event: Event):
    if event.post_type == 'message_sent':
        sent_event = event.model_dump()
        sent_event['post_type'] = 'message'
        sent_event = MessageEvent(**sent_event)
        await Bot.handle_event(bot, sent_event)
