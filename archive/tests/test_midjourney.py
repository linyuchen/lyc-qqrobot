from unittest import TestCase

import config
from msgplugins.midjourney.midjourney_websocket_client import MidjourneyClient


class TestMidjourney(TestCase):
    def setUp(self) -> None:
        self.midjourney = MidjourneyClient(token=config.MJ_DISCORD_TOKEN,
                                           channel_id=config.MJ_DISCORD_CHANNEL_ID,
                                           guild_id=config.MJ_DISCORD_GUILD_ID,
                                           proxy=config.GFW_PROXY)

    def test_send(self):
        # self.midjourney.start()
        self.task_res = None

        def callback(res):
            if not self.task_res:
                self.midjourney.upscale(res, 1)

            self.task_res = res
            print(res)

        while True:
            prompt = input("prompt:")
            self.midjourney.draw(prompt, callback)
