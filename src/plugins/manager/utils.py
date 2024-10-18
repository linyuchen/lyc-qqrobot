from nonebot import get_loaded_plugins


def find_plugin_by_name(name: str):
    plugins = get_loaded_plugins()
    for plugin in plugins:
        if plugin.metadata.name == name:
            return plugin
    return None