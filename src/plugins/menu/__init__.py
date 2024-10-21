import httpx
from nonebot import on_fullmatch

from nonebot.plugin import PluginMetadata, get_loaded_plugins

__plugin_meta__ = PluginMetadata(
    name="菜单",
    description="显示功能菜单",
    usage="菜单",
)

menu_cmd = on_fullmatch('菜单')


@menu_cmd.handle()
async def _():
    plugins = get_loaded_plugins()
    plugins = sorted(plugins, key=lambda x: x.metadata.name if x.metadata else x.id_)
    # 生成菜单截图
    menu_text = ''
    for plugin in plugins:
        if not plugin.metadata:
            continue
        plugin_name = plugin.metadata.name
        menu_text += f'【{plugin_name}】\n'
        plugin_description = plugin.metadata.description
        plugin_usage = '指令：' + plugin.metadata.usage
        menu_text += f'  {plugin_description}\n  {plugin_usage}\n\n'
    await menu_cmd.finish(menu_text)
