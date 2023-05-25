# 环境

## Python版本

Python3.11

## 第三方依赖库

`pip install -r requirements.txt`

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
