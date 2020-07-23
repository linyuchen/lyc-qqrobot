# 环境

## Python版本

采用Python3.7，并配置virtual env，文件夹为**venv**

## 酷Q

下载酷Q，[安装cqhttp插件](https://github.com/richardchien/coolq-http-api)

配置与nonebot对接，修改`data\app\io.github.richardchien.coolqhttpapi\config`下的{qq}.json

```json
{
    "$schema": "https://cqhttp.cc/config-schema.json",
    "host": "0.0.0.0",
    "port": 57000,
    "use_http": true,
    "ws_host": "0.0.0.0",
    "ws_port": 6700,
    "use_ws": true,
    "ws_reverse_url": "ws://127.0.0.1:19081/ws/",
    "use_ws_reverse": true,
    "enable_heartbeat": true,
    "ws_reverse_reconnect_interval": 3000,
    "ws_reverse_reconnect_on_code_1000": true,
    "post_url": "",
    "access_token": "",
    "secret": "",
    "post_message_format": "string",
    "serve_data_files": false,
    "update_source": "global",
    "update_channel": "stable",
    "auto_check_update": false,
    "auto_perform_update": false,
    "show_log_console": true,
    "log_level": "info"
}
```


## 第三方依赖库

`pip install -r pip-pkgs.txt`

# 程序启动

`start.bat`


# api文档
继承`qqsdk\qqclient`，复写`get_friends`、`get_groups`, `send_msg`

当收到消息时，调用`qqclient.add_msg`

# supserplugin插件文档

有活跃度功能，和群管理功能

活跃度相当于群里面游戏的货币（积分）

# 备份
只需要备份`msgplugins/superplugin/db.sqlite3`
