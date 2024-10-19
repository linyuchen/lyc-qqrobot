import httpx
from nonebot import on_fullmatch

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="票房",
    description="查看票房排行",
    usage="票房、电影票房、票房排名、票房排行",
)

box_office_cmd = on_fullmatch(('票房', '电影票房', '票房排名', '票房排行'))


@box_office_cmd.handle()
async def _():
    url = "https://api.yujn.cn/api/piaofang.php?type=json"
    async with httpx.AsyncClient() as http:
        data = (await http.get(url)).json()
        text = f"{data.get('time')}电影票房排名\n\n"
        for i in data.get('data'):
            text += f"《{i['title']}》: {i['sumBoxDesc']}, {i['releaseInfo']}\n"
        await box_office_cmd.finish(text)
