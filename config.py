import json
from pathlib import Path

config_path = Path(__file__).parent / "config.json"


def save_config():
    with config_path.open("w", encoding="utf-8") as fw:
        json.dump(config_data, fw, indent=4, ensure_ascii=False)


config_data = {
    "GFW_PROXY": "http://192.168.1.4:7890",
    "MIRAI_HTTP_API": "http://localhost:8080",
    "MIRAI_HTTP_API_VERIFY_KEY": "1234567890",
    "QQ": 721011692,
    # QQ = 1577491075,
    "ADMIN_QQ": 379450326,  # 机器人主人的QQ号,
    "LISTEN_PORT": 5000,
    "SEND2TIM": True,
    "SEND2TIM_HTTP_API": "http://localhost:8088/",
    "SD_HTTP_API": "http://192.168.1.4:7860",
    "VITS_HTTP_API": "http://192.168.1.4:7862",
    "TTS_ENABLED": False,
    "TUSI_TOKENS": [

    ],
    "plugins": {
        "group_plugin_manager": {
            "exclude_groups": [""],  # 列表中的群号将不会启用此插件
            "can_group_manage": False,  # 是否可以被群插件管理器管理,默认为True
            "enable": True,  # 是否启用,默认为True，这个是全局的
        },
        "global_plugin_manager": {
            "can_group_manage": False,
        },
        "blacklist": {
            "can_group_manage": False
        },
        "menu": {
            "summary": "显示菜单功能",
            "exclude_groups": [""]
        },
        "bilicard": {
            "summary": "显示B站视频信息",
            "exclude_groups": [""]
        },
        "bull_fight": {
            "exclude_groups": [""]
        },
        "dailynews": {
            "summary": "每日新闻",
            "exclude_groups": [""]
        },
        "game21": {
            "exclude_groups": [""]
        },
        "game24": {
            "exclude_groups": [""]
        },
        "running_time": {
            "summary": "显示机器人运行时间",
            "exclude_groups": [""]
        },
        "superplugins": {
            "summary": "活跃度功能",
            "exclude_groups": [""]
        },
        "stable_diffusion": {
            "summary": "AI画图",
            "exclude_groups": [""]
        },
        "sdxl": {
            "summary": "AI画图(sdxl版本)",
            "exclude_groups": [""]
        },
        "chatgpt": {
            "summary": "AI聊天功能",
            "exclude_groups": [""]
        }
    },
}

if config_path.exists():
    with config_path.open("r", encoding="utf-8") as fr:
        config_data.update(json.load(fr))
    save_config()
else:
    save_config()


def __getattr__(name):
    return config_data.get(name)


def __setattr__(name, value):
    config_data[name] = value
    save_config()
