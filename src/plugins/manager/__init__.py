from contextlib import AsyncExitStack
from typing import Optional

from nonebot import get_loaded_plugins, Bot, get_driver, on_fullmatch
from nonebot.adapters import Event
from nonebot.typing import T_DependencyCache
from nonebot.plugin import Plugin
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent

from src.plugins.common import check_super_user
from src.plugins.manager.utils import find_plugin_by_name

driver = get_driver()

'''
{
    '<plugin_id>': {
        'disable_global': False,
        'disable_groups': []
    }
}
'''
manager_data = {

}


plugin_list_cmd = on_fullmatch('插件列表')

@plugin_list_cmd.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    is_super_user = check_super_user(user_id)
    plugins = get_loaded_plugins()
    res = '已加载插件列表：\n'
    for plugin in plugins:
        res += f'{plugin.metadata.name}({plugin.id_})'
        # 群里是否已开启
        plugin_manager_data = manager_data.get(plugin.id_, {})
        if str(getattr(event, 'group_id')) in plugin_manager_data.get('disable_groups', []):
            res += '[已禁用]'
        else:
            res += '[已启用]'
        if is_super_user:
            # 全局是否已开启
            if not plugin_manager_data.get('disable_global'):
                res += '，全局[已启用]'
            else:
                res += '，全局[已禁用]'
    await plugin_list_cmd.finish(res)


enable_global_cmd = on_fullmatch(('全局启用插件', '全局禁用插件'), permission=SUPERUSER)
@enable_global_cmd.handle()
async def _(event: MessageEvent, args: CommandArg()):
    plugin_name = args.extract_plain_text().strip()
    plugin = find_plugin_by_name(plugin_name)
    if not plugin:
        return await enable_global_cmd.finish(f'插件{plugin_name}不存在')
    plugin_id = plugin.id_
    disable = event.get_plaintext().strip().startswith('全局禁用')
    manager_data.setdefault(plugin_id, {'disable_global': False, 'disable_groups': []})['disable_global'] = disable




def manager_permission(matcher: Matcher, bot: Bot, event: Event):
    plugin: Plugin = matcher.plugin
    plugin_name = plugin.metadata.name
    plugin_id = plugin.id_
    if manager_data.get(plugin_id, {}).get('disable_global'):
        return False
    if getattr(event, 'group_id') in manager_data.get(plugin_id, {}).get('disable_groups', []):
        return False
    return True


@driver.on_startup
async def _():
    plugins = get_loaded_plugins()
    for p in plugins:
        for m in p.matcher:
            def p_func(bot, event, matcher=m):
                return manager_permission(matcher=matcher, bot=bot, event=event)
            m.permission = m.permission | p_func
