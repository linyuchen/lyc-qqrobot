from nonebot import get_loaded_plugins, Bot, get_driver, on_fullmatch, on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.internal.adapter import Message
from nonebot.internal.permission import Permission
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin import Plugin

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="插件管理",
    description="在当前群启用和关闭插件，也可全局（全部群）启用和关闭插件",
    usage="插件列表，启用插件 插件名，禁用插件 插件名，全局启用插件 插件名，全局禁用插件 插件名",
)

from src.plugins.common.permission import add_inject_permission_checker, check_super_user, check_group_admin
from src.plugins.manager.util import find_plugin_by_name, init_plugin_manager_config, check_group_enable, \
    check_global_enable, \
    set_global_enable, set_group_enable

driver = get_driver()

plugin_list_cmd = on_fullmatch('插件列表')
global_cmd = on_command('全局禁用插件', aliases={'全局启用插件'}, permission=SUPERUSER)
group_cmd = on_command('启用插件', aliases={'禁用插件'}, permission=check_group_admin)


@plugin_list_cmd.handle()
async def _(event: Event):
    user_id = event.get_user_id()
    is_super_user = check_super_user(user_id)
    plugins = get_loaded_plugins()
    plugins = sorted(plugins, key=lambda x: x.metadata.name if x.metadata else x.id_)
    group_id = getattr(event, 'group_id')
    res = '插件列表：\n'
    for plugin in plugins:
        if plugin.id_ == 'common':
            continue
        plugin_name = plugin.metadata.name if plugin.metadata else plugin.id_
        res += f'【{plugin_name}】'
        # 群里是否已开启
        if check_group_enable(plugin.id_, group_id):
            res += '[√]'
        else:
            res += '[×]'
        if is_super_user:
            # 全局是否已开启
            if check_global_enable(plugin.id_):
                res += '，全局[√]'
            else:
                res += '，全局[×]'
        res += '\n'
    await plugin_list_cmd.finish(res)


@global_cmd.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    plugin_name = args.extract_plain_text().strip()
    plugin = find_plugin_by_name(plugin_name)
    if not plugin:
        return await global_cmd.finish(f'插件{plugin_name}不存在')
    plugin_id = plugin.id_
    enable = event.get_plaintext().strip().startswith('全局启用')
    set_global_enable(plugin_id, enable)
    await global_cmd.finish(f'插件 {plugin_name} 已全局{"启用" if enable else "禁用"}')


@group_cmd.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    plugin_name = args.extract_plain_text().strip()
    plugin = find_plugin_by_name(plugin_name)
    if not plugin:
        return await group_cmd.finish(f'插件{plugin_name}不存在')

    enable = event.get_plaintext().strip().startswith('启用')
    if group_id := getattr(event, 'group_id'):
        set_group_enable(plugin.id_, group_id, enable)

    await group_cmd.finish(f'插件 {plugin_name} 在本群已{"启用" if enable else "禁用"}')


def manager_permission(matcher: Matcher, bot: Bot, event: Event):
    plugin: Plugin = matcher.plugin
    plugin_name = plugin.metadata.name if plugin.metadata else plugin.id_
    plugin_id = plugin.id_
    if not check_global_enable(plugin_id):
        return False
    if not check_group_enable(plugin_id, getattr(event, 'group_id')):
        return False
    return True


@driver.on_startup
async def _():
    plugin_ids = [p.id_ for p in get_loaded_plugins()]
    init_plugin_manager_config(plugin_ids)
    add_inject_permission_checker(manager_permission)
