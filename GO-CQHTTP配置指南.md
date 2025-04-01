# go-cqhttp配置指南

本文档详细介绍如何配置go-cqhttp以便与GitHub Actions自动发送QQ消息配合使用。

## 什么是go-cqhttp

go-cqhttp是一个基于OneBot协议的QQ机器人实现，它可以：
- 接收并处理QQ消息
- 发送消息、图片、语音等内容
- 管理群组、好友等
- 提供HTTP API供外部程序调用

## 安装步骤

### 1. 下载go-cqhttp

访问[go-cqhttp官方仓库的Releases页面](https://github.com/Mrs4s/go-cqhttp/releases)，下载适合你系统的版本：
- Windows: 下载 `go-cqhttp_windows_*.zip`
- Linux: 下载 `go-cqhttp_linux_*.tar.gz`
- macOS: 下载 `go-cqhttp_darwin_*.tar.gz`

### 2. 配置go-cqhttp

1. 解压下载的文件到一个专用目录
2. 打开命令行，进入该目录
3. 首次运行go-cqhttp，会生成默认配置文件：
   - Windows: 双击`go-cqhttp.exe`
   - Linux/macOS: 执行`./go-cqhttp`

4. 编辑生成的`config.yml`文件，关键配置项：

```yaml
account:
  uin: 123456789 # 你的QQ账号
  password: '' # 密码留空会使用扫码登录

# 消息服务相关配置
servers:
  # HTTP 通信设置
  - http:
      host: 0.0.0.0 # 监听地址
      port: 5700 # 监听端口
      timeout: 5 # 反向 HTTP 超时时间, 单位秒
      post-format: array # 回复数据格式，建议设为array
      middlewares:
        access-token: '' # 填写访问令牌，用于验证请求的合法性

# 默认日志等级
log-level: info
```

### 3. 关键配置解析

#### 账号配置
- `uin`: 填写你的QQ号
- `password`: 可以留空使用扫码登录，或者填写密码（不推荐）

#### HTTP服务配置
- `host`: 设置为`0.0.0.0`可以监听所有网络接口
- `port`: 默认端口5700，可以根据需要修改
- `access-token`: 重要！设置一个复杂的令牌用于API验证

### 4. 启动go-cqhttp

配置完成后，再次运行go-cqhttp：
- 如果使用扫码登录，会显示二维码，用手机QQ扫描登录
- 如果使用密码登录，可能需要处理验证码等问题

### 5. 设置为服务（Linux）

如果你使用Linux服务器，建议将go-cqhttp设置为系统服务以确保持续运行：

1. 创建systemd服务文件：

```bash
sudo nano /etc/systemd/system/go-cqhttp.service
```

2. 添加以下内容（需要修改路径为你的实际路径）：

```
[Unit]
Description=go-cqhttp Bot Service
After=network.target

[Service]
Type=simple
User=你的用户名
WorkingDirectory=/path/to/go-cqhttp
ExecStart=/path/to/go-cqhttp/go-cqhttp
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

3. 启用并启动服务：

```bash
sudo systemctl enable go-cqhttp
sudo systemctl start go-cqhttp
```

### 6. 确保API可从外网访问

如果go-cqhttp运行在本地或私有服务器，需要确保GitHub Actions能够访问到它：

1. 配置端口转发（如果在家庭网络中）
2. 或使用内网穿透工具如frp、ngrok等
3. 或部署在公网可访问的云服务器上

不管使用哪种方式，请记得：
- 设置`access-token`以保证安全
- 将最终可访问的URL设置为GitHub Secrets中的`QQ_API_URL`

## API测试

配置完成后，可以使用以下命令测试API是否正常工作：

```bash
curl -X POST "http://your-server:5700/send_private_msg" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-access-token" \
     -d '{"user_id": 对方QQ号, "message": "测试消息"}'
```

如果一切正常，对方应该能收到"测试消息"。

## 常见问题解决

### 登录验证问题
- 首次登录可能需要验证，按照提示操作
- 频繁登录可能触发风控，建议固定IP使用
- 可以尝试扫码登录来减少风控概率

### 连接问题
- 确保服务器防火墙允许对应端口访问
- 检查网络连接是否稳定
- 使用`systemd`或`screen`等工具确保程序持续运行

### 安全问题
- 务必设置`access-token`
- 尽量不要暴露QQ号码
- 定期检查日志文件，关注异常访问

## 更多资源

- [go-cqhttp官方文档](https://docs.go-cqhttp.org/)
- [OneBot协议文档](https://github.com/howmanybots/onebot/blob/master/README.md)
- [go-cqhttp GitHub仓库](https://github.com/Mrs4s/go-cqhttp) 