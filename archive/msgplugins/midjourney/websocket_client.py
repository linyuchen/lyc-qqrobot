import asyncio
import json
import random
from dataclasses import dataclass

import websocket
import yaml


@dataclass
class Config:
    token: str

    @staticmethod
    def from_yaml(file_name: str):
        with open(file_name, "r") as file_stream:
            data = yaml.safe_load(file_stream)

        return Config(
            data["token"]
        )


class Bot:
    DISPATCH: int = 0
    HEARTBEAT: int = 1
    IDENTIFY: int = 2
    STATUS_UPDATE: int = 3
    VOICE_UPDATE: int = 4
    RESUME: int = 6
    RECONNECT: int = 7
    REQUEST_MEMBERS: int = 8
    INVALID_SESSION: int = 9
    HELLO: int = 10
    HEARTBEAT_ACK: int = 11
    WEBSOCKET_URL: str = "wss://gateway.discord.gg/?v=9&encoding=json"
    MAX_SIZE: int = 1_000_000_000

    def __init__(self):
        self.websocket: websockets.WebSocketClientProtocol = None
        self.interval: int = 0
        self.config: Config = Config.from_yaml("config.yaml")

        self.auth = {
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

    async def heartbeat(self) -> None:
        while True:
            await self.websocket.send(json.dumps({
                "op": self.HEARTBEAT,
                "d": "null"
            }))
            await asyncio.sleep(self.interval)

    async def login(self) -> None:
        await self.websocket.send(json.dumps(
            self.auth
        ))

    async def receive_messages(self) -> None:
        async for message in self.websocket:
            data: dict = json.loads(message)
            print(data)

    async def main(self) -> None:
        async with websocket.WebSocket().connect(
                self.WEBSOCKET_URL,
                max_size=self.MAX_SIZE,
            http_proxy_host="localhost",
            http_proxy_port=7890

        ) as self.websocket:
            event = await self.websocket.recv()
            self.interval = json.loads(event)["d"]["heartbeat_interval"] / 1000
            await self.login()

            tasks: [asyncio.tasks] = [
                asyncio.create_task(self.heartbeat()),
                asyncio.create_task(self.receive_messages())
            ]

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.main())
