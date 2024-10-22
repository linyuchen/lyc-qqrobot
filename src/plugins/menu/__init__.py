from nonebot import on_fullmatch, get_driver
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.plugin import PluginMetadata, get_loaded_plugins
from src.plugins.menu.menu import generate_image, get_plugins, menu_image_path

__plugin_meta__ = PluginMetadata(
    name="菜单",
    description="显示功能菜单",
    usage="菜单",
)

menu_cmd = on_fullmatch('菜单')


@menu_cmd.handle()
async def _():
    # plugins = get_plugins()
    # menu_text = ''
    # for plugin in plugins:
    #     if not plugin.metadata:
    #         continue
    #     plugin_name = plugin.metadata.name
    #     menu_text += f'【{plugin_name}】\n'
    #     plugin_description = plugin.metadata.description
    #     plugin_usage = '指令：' + plugin.metadata.usage
    #     menu_text += f'  {plugin_description}\n  {plugin_usage}\n\n'
    # await menu_cmd.finish(menu_text)
    await menu_cmd.finish(MessageSegment.image(menu_image_path.read_bytes()))


@get_driver().on_startup
async def _():
    await generate_image()
