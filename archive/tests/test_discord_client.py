from unittest import TestCase

from common.discord_client.discord_client import DiscordSeleniumClient


class TestDiscordClient(TestCase):

    def setUp(self) -> None:
        url = "https://discord.com/channels/1127887388648153118/1127887388648153121"
        self.client = DiscordSeleniumClient(url=url, debug_address="127.0.0.1:9990")

    def test_get_msgs(self):
        self.client.get_msgs()
