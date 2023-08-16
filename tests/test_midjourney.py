import asyncio

from msgplugins.midjourney.midjourney import MidjourneyClient

midjourney = MidjourneyClient()
asyncio.run(midjourney.send("asdfasdf --arv 1:2"))
asyncio.run(midjourney.message_listener())
