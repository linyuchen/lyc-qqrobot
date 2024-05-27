from typing import TypedDict, Literal

import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, MessageEvent
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot_plugin_waiter import waiter

from src.plugins.common.rules import rule_args_num


class SongDetail(TypedDict):
    songname: str
    name: str  # 歌手
    pay: Literal['免费']
    songid: int
    cover: str  # 封面链接
    songurl: str  # 歌曲详情页
    src: str  # 音频地址


class SearchResult(TypedDict):
    code: int  # 0 为成功
    msg: str
    data: list[SongDetail]


music_qq_cmd = on_command("点歌", force_whitespace=True, rule=rule_args_num(min_num=1))

TIMEOUT = 20


@music_qq_cmd.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    # send_res = await music_qq_cmd.send("正在为您搜索QQ音乐...")
    # prompt_msg_id = send_res['message_id']
    msg_id = event.message_id
    song_name = args.extract_plain_text()
    try:
        url = f'https://api.xingzhige.com/API/QQmusicVIP/?name={song_name}'
        res = await httpx.AsyncClient().get(url)
        search_result: SearchResult = res.json()
        if search_result['code'] != 0:
            raise Exception(f"{search_result['msg']}")
        song_list_data = search_result['data']
        song_list = [f'{i + 1}.{s["songname"]} - {s["name"]}' for i, s in enumerate(search_result['data'])]
        send_res = await music_qq_cmd.send("\n".join(song_list) + f"\n\n{TIMEOUT}秒内输入歌曲序号播放歌曲")
        song_list_msg_id = send_res["message_id"]

        @waiter(waits=["message"], keep_session=True)
        async def check(event: MessageEvent):
            return event.get_plaintext()

        song_index = -1
        async for resp in check(timeout=TIMEOUT):
            if resp is None:
                # await bot.delete_msg(message_id=song_list_msg_id)
                return await music_qq_cmd.send(MessageSegment.reply(song_list_msg_id) + "点歌超时，已取消")
            if not resp.isdigit():
                continue
            song_index = resp
            try:
                song_index = int(song_index)
                if song_index <= 0 or song_index > len(song_list_data):
                    continue
                break
            except Exception as e:
                continue

        song: SongDetail = (await httpx.AsyncClient().get(url + f'&n={song_index}')).json()['data']
        await music_qq_cmd.send(MessageSegment.music_custom(
            url=song['songurl'],
            audio=song['src'],
            title=song['songname'],
            content=song['name'],
            img_url=song['cover']
        ))
        await bot.delete_msg(message_id=song_list_msg_id)

    except Exception as e:
        await music_qq_cmd.finish(f"点歌出错: {e}")
