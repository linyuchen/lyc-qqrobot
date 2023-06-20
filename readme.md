# 环境

## Python版本

Python3.11

## 第三方依赖库

`pip install -r requirements.txt`

# mirai配置

## 安装`mirai`

下载(mcl-install)[https://github.com/iTXTech/mcl-installer/releases]

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

一般第三方QQ框架都提供http api，

新建个类 继承`qqsdk\qqclient`，复写`get_friends`、`get_groups`, `send_msg`, 
这个三方法里调用第三方的http api

## 接受消息
复写 `get_msg`方法，
`get_msg`实际上是个`flask route`，路径是`/`，绑定的端口为`listen_port`

在`get_msg`方法中, 当收到消息时，调用`qqclient.add_msg`添加消息

## 启动

然后实例化刚刚复写的类，并执行它的start()

# supserplugin插件文档

有活跃度功能，和群管理功能

活跃度相当于群里面游戏的货币（积分）

# 备份
只需要备份`msgplugins/superplugin/db.sqlite3`

# 相关文档

[mirai-http-api接口url文档](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)

[mirai-http-api接口请求和返回数据文档](https://docs.mirai.mamoe.net/mirai-api-http/api/API.html)

# TODO
- [ ] ~~mirai也使用docker~~
- [ ] ~~mirai和qqrobot使用docker network通信~~
- [x] 不同环境不同的配置文件
- [x] docker build脚本，自动识别cpu架构