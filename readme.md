# 自写的一套QQ机器人框架

## 目前已经实现的功能
- [x] 调用Tim官方客户端发送消息，避免风控发不出消息
- [x] 调用Midjourney实现AI绘画
- [x] 调用StableDiffusion实现AI绘画
- [x] 调用吐司在线画图实现AI绘画
- [x] 接入chatgpt聊天，可以设置AI人格
- [x] 发送B站视频链接或者BV、AV号进行分析视频并AI总结视频内容
- [x] 总结任意网页
- [x] 维基百科、萌娘百科搜索
- [x] 聊天指令管理开关各个插件
- [x] 斗牛棋牌游戏
- [x] 21点棋牌游戏
- [x] 24点算数游戏
- [x] 活跃度系统，群成员发言一次加一点活跃度，签到、连续签到获得额外奖励，活跃度有排行榜
- [x] 文字转语音聊天
- [x] ~~原神抽卡模拟，已不再更新~~
# 环境

## Python版本

Python3.11

## 第三方依赖库

`pip install -r requirements.txt`

# mirai配置

## 安装`mirai`

下载[mcl-install](https://github.com/iTXTech/mcl-installer/releases)

运行`mcl-install`会自动下载依赖和`mcl`

## 安装`mirai-http-api`

```bash
./mcl
./mcl --update-package net.mamoe:mirai-api-http --channel stable-v2 --type plugin
```
重启mcl后退出mcl

## 配置mirai和mirai-http-api

编辑`config/Console/AutoLogin.yml`，添加QQ的账号密码

编辑`config/net.mamoe.mirai-api-http/setting.yml`

`adapters`添加`- webhook`
`adaptersSettings`添加
```yaml
webhook:
  destinations: 
    - 'localhost:5000/'
```


## 启动mirai

```bash
./mcl
```

如果提示需要滑动验证码，复制验证码链接，浏览器打开调试控制台，
粘贴验证码链接访问，验证通过之后，在控制台能看到一个`cap_union_new_verify`的请求，
它的response有一个**ticket**，复制下来，粘贴到mirai控制台回车即可。

# 对接第三方QQapi

这里我已经写好了一个对接mirai的，如果想使用mirai的http api直接使用[client/mirai_http/main.py](client/mirai_http/main.py)即可

一般第三方QQ框架都提供http api，

新建个类 继承`qqsdk\qqclient`，复写`get_friends`、`get_groups`, `send_msg`, 
这个三方法里调用第三方的http api

## 接受消息
复写 `get_msg`方法，
`get_msg`实际上是个`flask route`，路径是`/`，绑定的端口为config.json中的`listen_port`

在`get_msg`方法中, 当收到消息时，调用`qqclient.add_msg`添加消息


## 配置参数

所有参数可以在`config.py`看到，首次运行一下`config.py`会在同级目录生成一个`config.json`,最终拿到的参数配置就是在`config.json`里面

### 参数说明

**MIRAI_HTTP_API**: mirai端的http api地址

**MIRAI_HTTP_API_VERIFY_KEY**: mirai端http api的密钥


**QQ**: 机器人的QQ号

**ADMIN_QQ**: 机器人的管理员(主人)QQ号

**LISTEN_PORT**: 机器人的http api监听的端口，主要是用于mirai主动发送接收到的消息到本项目

**SEND2TIM**: 是否使用Tim进行发送消息，需要运行Tim的服务端，服务端项目地址 <https://github.com/linyuchen/qqrobot-server/>

**SEND2TIM_HTTP_API**: Tim服务端的http api地址

**SD_HTTP_API**: StableDiffusion的http api地址

**VITS_HTTP_API**: 文字转语音的VITS http api地址

**TTS_ENABLED**: 是否启用文字转语音，启用的时候机器人会在回复消息时加上语音，触发条件详见[msgplugins/chatgpt/__init__.py](msgplugins/chatgpt/__init__.py)

**MJ_DISCORD_TOKEN**: 开通了Midjourney的discord账号token，获取方式：打开浏览器登录到discord，跳出网络控制台，随便发送个消息然后查看请求头部的Authorization值

**MJ_DISCORD_CHANNEL_URL**: 添加了MJ机器人的频道地址

**TUSI_TOKENS**: 吐司在线画图的token

**CHATGPT**: chatgpt的相关配置

**GFW_PROXY**: 科学上网的HTTP代理服务器


## 启动

然后实例化刚刚复写的类，并执行它的start()

mirai的话直接使用[client/mirai_http/main.py](client/mirai_http/main.py)即可


# 备份
需要备份`msgplugins/superplugin/db.sqlite3`,`config.json`

# 相关文档

[mirai-http-api接口url文档](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)

[mirai-http-api接口请求和返回数据文档](https://docs.mirai.mamoe.net/mirai-api-http/api/API.html)

# TODO
- [ ] ~~mirai也使用docker~~
- [ ] ~~mirai和qqrobot使用docker network通信~~
- [x] 不同环境不同的配置文件
- [x] docker build脚本，自动识别cpu架构
- [ ] midjourney选图放大功能
- [ ] midjourney生成图功能
- [ ] 完善本文档
