# 基于 NoneBot2 的 QQ 机器人

## 功能
- [x] 知乎链接预览截图
- [x] github链接readme预览截图
- [x] 随机加速gif
- [x] 接入chatgpt聊天，可以设置AI人格
- [x] 发送B站视频链接或者BV、AV号进行分析视频并AI总结视频内容
- [x] 总结任意网页
- [x] 维基百科、萌娘百科搜索
- [x] 斗牛棋牌游戏
- [x] 21点棋牌游戏
- [x] 24点算数游戏
- [x] 活跃度系统，签到、连续签到获得额外奖励，活跃度有排行榜
- [x] 发送知乎链接自动截图预览，支持知乎专栏、知乎问答
- [x] 发送github链接自动截图预览readme
- [x] 聊天指令管理开关各个插件
- [ ] 文字转语音聊天
- [ ] 调用Midjourney实现AI绘画
- [ ] 调用StableDiffusion实现AI绘画
- [ ] 接入bing ai
- [x] ~~调用吐司在线画图实现AI绘画，吐司加了验证码，暂时放弃~~
- [x] ~~原神抽卡模拟，已不再更新~~
- [x] ~~戳戳群友头像随机发送即时生成的表情包~~
- [x] ~~调用Tim官方客户端发送群消息，避免风控发不出消息~~
 
# 环境

## Python版本

Python3.11以上

## 第三方依赖库

`pip install -r requirements.txt`

### 初始化

运行`init.bat`，会下载一些必要文件和登录知乎、B站


## 配置自带的插件参数

运行了`init.bat`之后会自动生成`config.json`

打开`config.json`修改对应参数

ChatGPT 的全局默认人格在 `data/chatgpt_default_prompt.txt`，首次运行 Bot 会自动生成

## 对接onebot(墙裂推荐)

配置LLOneBot,详情见[LLOneBot](https://github.com/linyuchen/LiteLoaderQQNT-OneBotApi)

# 启动

```shell
python bot.py
```

# 备份

需要备份`data`文件夹， 还有`config.json`
