from typing import Union, Literal, Type
import asyncio
import json

import websockets
import httpx

from src.common.utils.random_hash import generate_random_hash

host = 'fs.firefly.matce.cn'

ws_url = f"wss://{host}/queue/join"

speakers = []

LangType = Union[Literal['ZH'], Literal['EN'], Literal['JP'], None]


async def get_speakers():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://{host}/info')
        info = response.json()
        speakers_str: str = info['unnamed_endpoints']['1']['parameters'][0]['python_type']['description']
        speakers_str = speakers_str.replace('Option from: ', '').replace("'", '"').replace("(", "[").replace(")", "]")
        speakers_list = json.loads(speakers_str)  # [('说话人1', '说话人1')]
        speakers_list = [i[1] for i in speakers_list]
        speakers.extend(speakers_list)


def search_speaker(speaker: str, lang: LangType):
    for s in speakers:
        if s == f'{speaker}_{lang}':
            return s
        if s == speaker:
            return s


async def fs_tts(speaker: str, text: str, lang: LangType):
    if len(speakers) == 0:
        await get_speakers()
    speaker = search_speaker(speaker, lang)
    if not speaker:
        raise Exception(f'找不到角色 {speaker}')
    async with websockets.connect(ws_url) as websocket:
        # 发送消息
        # await websocket.send("Hello, Server!")
        # print(f"> Sent: Hello, Server!")

        # 发送 hash
        session_hash = generate_random_hash(8)

        while True:
            recv_data = await recv_json(websocket)
            msg = recv_data.get('msg')
            if msg == 'process_completed':
                # {"msg":"process_completed","output":{"data":[{"name":"/tmp/gradio/44c2af408ef6aef02ae7027a83a87dc805e3c263/audio.wav","data":null,"is_file":true,"orig_name":"audio.wav"},null],"is_generating":true,"duration":1.1233408451080322,"average_duration":1.5567657880754984},"success":true}
                wav_url = f'https://{host}/file=' + recv_data['output']['data'][0]['name']
                print(recv_data)
                return wav_url
            elif msg == 'send_hash':
                send_data = {"fn_index": 4, "session_hash": session_hash}
                await send_json(websocket, send_data)
                print('send hash')
            elif msg == 'send_data':
                # todo: 选定引导音频
                send_data = {"data":
                                 [text, True, None, "", 0, 90, 0.7, 1.5, 0.7, speaker], "event_data": None,
                             "fn_index": 4,
                             "session_hash": session_hash
                             }
                await send_json(websocket, send_data)


async def send_json(ws, data: dict):
    await ws.send(json.dumps(data))


async def recv_json(ws):
    res = await ws.recv()
    return json.loads(res)


if __name__ == '__main__':
    print(asyncio.run(fs_tts('可莉', '你好呀，我是可莉', 'ZH')))
