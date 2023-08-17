import json
import random
import threading
import time

import websocket

websocket.enableTrace(True)


class DiscordClient():

    def __init__(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(
            "wss://gateway.discord.gg/?v=6&encoding=json",
            http_proxy_host="localhost",
            http_proxy_port=7890,
            on_message=self.recv
        )
        threading.Thread(target=self.heart).start()
        self.login()

    def login(self):
        auth = {
            "op": 2,
            "d": {
                "token": "",
                "properties": {
                    "$os": random.choice(["windows", "linux", "iOS"]),
                    "$browser": random.choice(["firefox", "chrome", "edge", "safari"]),
                    "$device": random.choice(["pc", "mobile"])
                }
            }
        }
        auth2 = {
            "op": 2,
            "d": {
                "token": "",
                "capabilities": 16381,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "zh-CN",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                    "browser_version": "115.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 219839,
                    "client_event_source": None
                },
                "presence": {
                    "status": "unknown",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                    "private_channels_version": "0",
                    "api_code_version": 0
                }
            }
        }
        self.ws.send(json.dumps(auth))
        # print(self.ws.recv())
        data = {
            "guild_id": "1127887388648153118",
            "typing": True,
            "threads": True,
            "activities": True,
            "members": [],
            "channels": {},
            "thread_member_lists": []
        }
        self.ws.send(json.dumps(data))
        print(self.ws.recv())

    def recv(self, ws):
        event = ws.recv()
        print(event)

    def heart(self):
        pass
        # while True:
            # self.ws.send(json.dumps({
            #     "op": 1,
            #     "d": "null"
            # }))
            # time.sleep(30)


DiscordClient()
input()
