# 使用Python编写的一套QQ机器人框架

## 功能
- [x] 随机加速gif
- [x] 戳戳群友头像随机发送即时生成的表情包
- [x] 调用Tim官方客户端发送群消息，避免风控发不出消息
- [x] 调用Midjourney实现AI绘画
- [x] 调用StableDiffusion实现AI绘画
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
- [x] 发送知乎链接自动截图预览，支持知乎专栏、知乎问答
- [x] 发送github链接自动截图预览readme
- [x] ~~调用吐司在线画图实现AI绘画，吐司加了验证码，暂时放弃~~
- [x] ~~原神抽卡模拟，已不再更新~~
 
# 环境

## Python版本

Python3.11

## 第三方依赖库

`pip install -r requirements.txt`

### 初始化

运行`init.bat`，会下载一些必要文件和登录知乎

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

## 配置自带的插件参数

打开`config.json`修改对应参数, 运行了`init.bat`之后会自动生成`config.json`

[参数文档](doc/config.md)

## 启动本框架

运行[client/mirai_http/main.py](client/mirai_http/main.py)即可


# 备份

需要备份`msgplugins/superplugin/db.sqlite3`,`config.json`

# 相关文档

[mirai-http-api接口url文档](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)

[mirai-http-api接口请求和返回数据文档](https://docs.mirai.mamoe.net/mirai-api-http/api/API.html)

# 插件开发

参考[msgplugins/example.py](msgplugins/example.py)

# TODO
- [ ] 完善本文档
- [ ] MJ图生图自动识别宽高比例
- [ ] SD画图识别关键字自动添加lora
- [ ] 命令菜单使用图片生成并美化
- [ ] 画图引擎切换命令

# 许可证

```
Copyright (C) 2019-2023.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
