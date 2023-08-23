# 配置参数说明

**QQ**: 机器人的QQ号，必填

**ADMIN_QQ**: 机器人的管理员(主人)QQ号

**MIRAI_HTTP_API**: mirai端的http api地址，必填否则无法启动

**MIRAI_HTTP_API_VERIFY_KEY**: mirai端http api的密钥，必填否则无法启动

**LISTEN_PORT**: 机器人的http api监听的端口，主要是用于mirai主动推送消息到本项目

**SEND2TIM**: 是否使用官方Tim进行发送群消息，需要运行Tim的服务端，服务端项目地址 <https://github.com/linyuchen/qqrobot-server/>

**SEND2TIM_HTTP_API**: Tim服务端的http api地址

**SD_HTTP_API**: StableDiffusion的http api地址

**VITS_HTTP_API**: 文字转语音的VITS http api地址

**TTS_ENABLED**: 是否启用文字转语音，启用的时候机器人会在回复消息时加上语音，触发条件详见[msgplugins/chatgpt/__init__.py](msgplugins/chatgpt/__init__.py)

**MJ_DISCORD_TOKEN**: 开通了Midjourney的discord账号token，获取方式：打开浏览器登录到discord，跳出网络控制台，随便发送个消息然后查看请求头部的Authorization值

**MJ_DISCORD_CHANNEL_ID**: Midjourney的discord频道ID，浏览器打开频道，查看URL中的频道ID, 如https://discord.com/channels/1127887388648153118/1127887388648153121,最后的1127887388648153121就是频道ID

**MJ_DISCORD_GUILD_ID**: ，频道URL中在频道ID前面的那个ID

**TUSI_TOKENS**: 吐司在线画图的token

**CHATGPT**: chatgpt的相关配置

**GFW_PROXY**: 科学上网的HTTP代理服务器
