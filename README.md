# 自动发送QQ查寝消息

本项目用于自动发送QQ查寝消息，支持定时发送和手动触发。

## 当前状态与问题

目前遇到以下问题：

1. QQ账号登录需要签名服务器，出现"Code 45"错误和"账号被限制登录"提示
2. 无法通过Docker运行签名服务器
3. 花生壳内网穿透设置成功，但访问时显示"不支持Web访问方式"

## 解决方案

### 方案1：使用最新版go-cqhttp并配置签名服务器

1. 下载最新版go-cqhttp: https://github.com/Mrs4s/go-cqhttp/releases/latest
2. 安装Docker并运行签名服务器:
   ```
   docker run -d --restart=always --name qsign -p 8080:8080 -e ANDROID_ID=1234567890abcdef -e QQ_VERSION=8.9.70 xzhouqd/qsign:1.1.6
   ```
3. 在config.yml中配置签名服务器:
   ```yaml
   sign-servers: 
     - url: 'http://127.0.0.1:8080/sign?key=114514'
       key: '114514'
       authorization: '-'
   ```

### 方案2：使用Mirai框架 (推荐)

我们已创建基于Mirai框架的替代方案，这是一个更稳定的QQ机器人框架。

详细安装步骤：
- [快速安装指南](docs/setup_guide.md)
- [详细配置文档](docs/mirai_guide.md)

主要优势：
- 更稳定的登录机制
- 更灵活的API
- 丰富的插件生态
- 跨平台支持

使用示例：
```bash
python scripts/mirai_sender.py --target 目标QQ号 --verify-key 你的验证密钥 --message "查寝提醒：代码123"
```

### 方案3：使用其他平台API

1. 企业微信: https://work.weixin.qq.com/
2. 钉钉: https://www.dingtalk.com/

## 脚本使用方法

1. 直接发送消息:
   ```
   py scripts/send_message_direct.py --target 目标QQ号 --api-url http://1064ju811jp02.vicp.fun:13701
   ```

2. 定时发送查寝消息通过GitHub Actions:
   ```yaml
   name: 定时发送QQ查寝消息
   on:
     schedule:
       - cron: '40 14 * * *'  # 每天晚上22:40 (UTC+8)
   ```

## 关于花生壳内网穿透

花生壳内网穿透已经配置:
- 外网域名: 1064ju811jp02.vicp.fun
- 外网端口: 13701
- 内网主机: 192.168.249.19
- 内网端口: 5700

但访问时显示"不支持Web访问方式"，可能需要其他内网穿透方案，如frp或ngrok。

## 功能特点

- 🕒 支持定时发送消息（默认每天晚上10点）
- 📱 支持批量发送给多个QQ联系人
- 🔒 通过GitHub Secrets安全存储账号信息
- 🤖 使用go-cqhttp框架与QQ通信
- 🚀 零成本部署（使用GitHub免费服务）

## 使用步骤

### 1. 部署go-cqhttp

首先需要部署go-cqhttp作为QQ机器人框架：

1. 从[go-cqhttp官方仓库](https://github.com/Mrs4s/go-cqhttp/releases)下载适合你系统的版本
2. 按照[官方指南](https://docs.go-cqhttp.org/guide/quick_start.html)配置go-cqhttp：
   - 使用QQ扫码或账号密码登录
   - 在config.yml中开启HTTP API功能
   - 设置`post_format`为`array`
   - 配置访问令牌（access-token）用于安全验证

### 2. 准备GitHub仓库

1. Fork或克隆本仓库到你的GitHub账号
2. 在仓库设置中添加以下Secrets:
   - `QQ_API_URL`: go-cqhttp的API地址，如`http://your-server:5700`
   - `QQ_API_TOKEN`: API访问令牌（与go-cqhttp的配置保持一致）
   - `QQ_TARGETS`: 目标QQ号列表，多个用逗号分隔，如`123456789,987654321`

### 3. 自定义消息内容（可选）

修改`scripts/send_message.py`文件中的`message`变量，自定义你的查寝消息内容。

### 4. 调整发送时间（可选）

GitHub Actions使用UTC时间，而中国是UTC+8时区。默认配置为每天晚上10点发送消息：

- 在`.github/workflows/send_qq.yml`文件中修改cron表达式
- 默认值`0 14 * * *`表示UTC 14:00（即北京时间22:00）

## 常见问题

### 如何在本地测试？

1. 克隆仓库到本地
2. 安装依赖：`pip install -r requirements.txt`
3. 设置环境变量或创建`.env`文件：
```
QQ_API_URL=http://your-server:5700
QQ_API_TOKEN=your-access-token
QQ_TARGETS=123456789,987654321
```
4. 运行脚本：`python scripts/send_message.py`

### go-cqhttp部署问题

- 建议使用Linux服务器长期运行go-cqhttp
- 可以使用screen或systemd等工具保持后台运行
- 确保服务器防火墙允许对应端口访问

### 消息没有发送成功？

检查以下几点：
- go-cqhttp是否正常运行并在线
- API地址是否可以从外网访问
- 访问令牌是否配置正确
- GitHub Secrets是否设置正确

## 注意事项

- QQ可能会对频繁自动化操作的账号进行风控，建议使用小号
- 请合理使用此工具，避免骚扰他人
- GitHub Actions每月有有限的免费额度，但对于这个应用场景通常已经足够 