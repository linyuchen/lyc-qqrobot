# 基于 NoneBot2 的跨平台机器人

## 主要功能

* AI 聊天，支持多种 AI 引擎，如 ChatGPT，Gemini，Deepseek 等
* 支持不同的聊天对象设置不同的 AI 引擎
* 支持不同的聊天对象设置不同的 AI 人格
* B站链接预览，支持 AI 总结视频，需要先发送 `登录B站` 扫码登录
* 默认支持 TG 和 QQ，其他平台需要自行添加相应的 Adapter
* 其他功能发送`菜单`查看
 
# 环境

## Python版本

Python3.11以上

## 第三方依赖库

`pip install -r requirements.txt`

## 配置

修改 `.env` 文件，修改对应的参数

ChatGPT 的全局默认人格在 `data/chatgpt_prompt/default.txt`，首次运行 Bot 会自动生成

其他设置的自定义人格也在 `data/chatgpt_prompt/` 下

## 对接onebot(墙裂推荐)

配置LLOneBot,详情见[LLOneBot](https://github.com/linyuchen/LiteLoaderQQNT-OneBotApi)

.env 配置参考[OneBot V11适配器](https://onebot.adapters.nonebot.dev/docs/guide/setup)

## 对接 Telegram

.env 参考[TGAdapter](https://github.com/nonebot/adapter-telegram/blob/beta/MANUAL.md)

注意设置修改 `.env` 的 `SUPERUSERS` 添加自己的 TG ID 

# 启动

```shell
python bot.py
```

# 备份

需要备份`data`文件夹

# 常见问题

## 如何安装其他 NoneBot2 插件

使用 `pip install 插件名`

## B站视频没有 AI 总结

需要先发送 `登录B站` 扫码登录

## GitHub 链接无法预览，ChatGPT Gemini 等需要翻墙的服务无法使用

修改 `.env` 的 `HTTP_PROXY` 配置代理

## 修改了 config.json 但是没有生效

新版本重构了配置文件，所有的配置都放到了 .env，config.json已弃用！
