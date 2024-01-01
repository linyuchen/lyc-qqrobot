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

# 相关文档

[mirai-http-api接口url文档](https://docs.mirai.mamoe.net/mirai-api-http/adapter/HttpAdapter.html)

[mirai-http-api接口请求和返回数据文档](https://docs.mirai.mamoe.net/mirai-api-http/api/API.html)
