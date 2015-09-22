# 第三方依赖库

**PyV8**

**requests**

# 程序启动

## 启动主程序

命令行下执行

    start_clinet.py qq号 密码 端口号

如：
    
    start_clinet.py 1234567 passwd 6666

端口是供插件程序调用QQ API用的，要与插件程序对应

## 启动插件程序

    start_plugin.py 端口号

如:

    start_plugin.py 6666

端口号要与主程序的对应

# 插件

所有插件都放在qqsdkplugins里面，插件编写方法参考`qqsdkplugins/example.py`和`qqsdkplugins/example2.py`

# api文档

制作中...
