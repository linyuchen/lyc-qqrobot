import asyncio
import json
import os
import time
import traceback

import websockets

# socks.set_default_proxy(socks.PROXY_TYPE_HTTP, 'http://127.0.0.1', 7890)
# socket.socket = socks.socksocket
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'


class WebSocketConnection:
    def __init__(self):
        self.ws = None

    async def connect(self, token):
        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "Windows 11",
                    "$browser": "Google Chrome",
                    "$device": "Windows"
                }
            },
            "s": None,
            "t": None,
        }

        url = "wss://gateway.discord.gg/?v=9&encoding=json"
        while True:
            try:
                async with websockets.connect(url, max_size=10 ** 7) as ws:
                    print("WebSocket connected")
                    self.ws = ws
                    await ws.send(json.dumps(auth))
                    print("Auth data sent")

                    hello_message = json.loads(await ws.recv())
                    print(hello_message)
                    heartbeat_interval = hello_message['d']['heartbeat_interval'] / 1000.0
                    print(f"Heartbeat interval: {heartbeat_interval}")

                    heartbeat_task = asyncio.create_task(self.send_heartbeat(ws, heartbeat_interval))

                    print("Starting to process messages")
                    await self.process_messages(ws)

                    print("Cancelling heartbeat")
                    heartbeat_task.cancel()

            except Exception as e:
                traceback.print_exc()
                print(f"Unexpected exception: {e}")

            print("Reconnecting.")
            time.sleep(5)

    async def send_heartbeat(self, ws, interval):
        while True:
            await ws.send('{"op": 1, "d": null}')
            await asyncio.sleep(interval)

    async def process_messages(self, ws):
        print("Listening messages.")
        try:
            async for message in ws:
                # print(message) You can use this to see what is discord gateway returning and you can debug to see the content of messages.
                data = json.loads(message)

                if data['t'] == 'MESSAGE_CREATE':
                    content = data['d']['content']
                    print(f"Message created: {content}")
                    # Handle the rest of the logic

                elif data['t'] == 'MESSAGE_UPDATE':
                    print("Message updated")
                    # Handle the rest of the logic

                elif data['t'] == 'MESSAGE_DELETE':
                    print("Message deleted")
                    # Handle the rest of the logic

        except Exception as e:
            print(f"WebSocket error: {e}")


if __name__ == '__main__':
    asyncio.run(
        WebSocketConnection().connect("MTAxMzIwMzkzNzc1MjUyNjg3OA.GTgn6w.xkzYA_kPzuhZTHqePf5o8zwZTRQNuxeREdtTAQ"))
