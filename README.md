# QQ自动查寝消息发送工具

这个工具可以通过GitHub Actions自动定时发送QQ消息，适合用于宿舍查寝、定时提醒等场景。

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