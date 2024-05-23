# 对接第三方QQapi

这里我已经写好了一个对接mirai的，如果想使用mirai的http api直接使用[client/mirai_http/main.py](../archive/client/mirai_http/main.py)即可

一般第三方QQ框架都提供http api，

新建个类 继承`qqsdk\qqclient`，复写`get_friends`、`get_groups`, `send_msg`, 
这个三方法里调用第三方的http api

## 接受消息
复写 `get_msg`方法，
`get_msg`实际上是个`flask route`，路径是`/`，绑定的端口为config.json中的`listen_port`

在`get_msg`方法中, 当收到消息时，调用`qqclient.add_msg`添加消息


## 配置参数

所有参数可以在`config.py`看到，首次运行一下`config.py`会在同级目录生成一个`config.json`,最终拿到的参数配置就是在`config.json`里面
## 启动

然后实例化刚刚复写的类，并执行它的start()

mirai的话直接使用[client/mirai_http/main.py](../archive/client/mirai_http/main.py)即可

