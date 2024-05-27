import httpx
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

box_office_cmd = on_command('票房', aliases={'电影票房', '票房排名', '票房排行'})


@box_office_cmd.handle()
async def _():
    url = "https://api.yujn.cn/api/piaofang.php?type=json"
    async with httpx.AsyncClient() as http:
        data = (await http.get(url)).json()
        text = f"{data.get('time')}电影票房排名\n\n"
        for i in data.get('data'):
            text += f"《{i['title']}》: {i['sumBoxDesc']}, {i['releaseInfo']}\n"
        await box_office_cmd.finish(text)


girl_video_cmd = on_command('来点视频', aliases={'小姐姐视频', '随机视频'})


@girl_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/zzxjj.php?type=video"
    await girl_video_cmd.finish(MessageSegment.video(url))


black_socks_video_cmd = on_command('黑丝', aliases={'黑丝视频', '来点黑丝'})


@black_socks_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/heisis.php?type=video"
    await black_socks_video_cmd.finish(MessageSegment.video(url))


white_socks_video_cmd = on_command('白丝', aliases={'白丝视频', '来点白丝'})


@white_socks_video_cmd.handle()
async def _():
    url = "http://api.yujn.cn/api/baisis.php?type=video"
    await white_socks_video_cmd.finish(MessageSegment.video(url))
