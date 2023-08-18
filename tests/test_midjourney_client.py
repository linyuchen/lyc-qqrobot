from unittest import TestCase
from msgplugins.midjourney.midjourney_client import MidjourneyClient, TaskCallbackResponse


class TestMidjourneyClient(TestCase):

    def setUp(self) -> None:
        url = "https://discord.com/channels/1127887388648153118/1127887388648153121"
        self.client = MidjourneyClient(url=url, debug_address="127.0.0.1:9990")

    def test_draw(self):
        def callback(param: TaskCallbackResponse):
            print("prompt:", param.prompt)
            print("error:", param.error)
            print("path:", param.image_path)

        while True:
            prompt = input("prompt:")
            if not prompt:
                break
            self.client.draw(prompt, callback)
