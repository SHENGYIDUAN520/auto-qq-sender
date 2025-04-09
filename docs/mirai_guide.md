# Mirai 框架部署指南

本指南介绍如何使用 Mirai 框架替代 go-cqhttp 来实现 QQ 查寝消息的自动发送。

## 1. 安装必要条件

### 1.1 安装 Java 11 或更高版本

Mirai 需要 Java 11 或更高版本才能运行。

**Windows:**
1. 下载 JDK 11 安装包：[AdoptOpenJDK](https://adoptopenjdk.net/)
2. 运行安装程序，按照引导完成安装
3. 验证安装：`java -version`

### 1.2 下载 Mirai Console Loader (MCL)

1. 创建目录并下载 MCL：
```powershell
# Windows PowerShell
New-Item -Path "mirai" -ItemType Directory -Force
Set-Location -Path "mirai"
Invoke-WebRequest -Uri "https://github.com/iTXTech/mirai-console-loader/releases/download/v2.1.2/mcl-2.1.2.zip" -OutFile "mcl.zip"
Expand-Archive -Path "mcl.zip" -DestinationPath "." -Force
```

## 2. 配置 Mirai

### 2.1 首次启动 MCL

```powershell
.\mcl.cmd
```

首次启动会自动下载和安装必要的组件，包括 Mirai Console 和 Mirai Core。请等待安装完成。

### 2.2 安装 Mirai HTTP API 插件

在 MCL 控制台中输入：
```
./mcl --update-package net.mamoe:mirai-api-http --channel stable --type plugin
```

然后重启 MCL。

### 2.3 配置 Mirai HTTP API

1. 找到 `config/net.mamoe.mirai-api-http/setting.yml` 文件
2. 编辑配置如下：

```yaml
adapters:
  - http
  - webhook

enableVerify: true
verifyKey: 你的验证密钥  # 请修改为自定义的密钥

adapterSettings:
  http:
    host: 0.0.0.0
    port: 8080
    cors: [*]
```

### 2.4 登录 QQ 账号

在 MCL 控制台中输入：
```
login 你的QQ号 你的密码
```

如果出现验证码或设备验证，请按照提示完成验证。

## 3. 使用 Python 脚本发送消息

我们提供了 `scripts/mirai_sender.py` 脚本，可以通过 Mirai HTTP API 发送 QQ 消息。

```bash
python scripts/mirai_sender.py --target 目标QQ号 --verify-key 你的验证密钥 --message "查寝提醒：代码123，若请假请忽略此条消息，谢谢。"
```

### 参数说明：

- `--target`: 接收消息的目标QQ号
- `--api-url`: Mirai HTTP API 的地址，默认 http://localhost:8080
- `--verify-key`: 在配置文件中设置的验证密钥
- `--message`: 要发送的消息内容

## 4. 自动化部署

### 4.1 使用 Windows 计划任务

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置名称和描述
4. 设置触发器（例如，每天晚上 22:40）
5. 设置操作为运行程序，程序为 `python`，参数为：
   ```
   scripts/mirai_sender.py --target 目标QQ号 --verify-key 你的验证密钥
   ```

### 4.2 使用 GitHub Actions（需要公网服务器）

如果你有公网服务器，可以在服务器上部署 Mirai，然后使用 GitHub Actions 远程调用 API。

## 5. 常见问题与解决方案

### 5.1 登录失败

如果登录遇到"设备锁"或"滑块验证"：
1. 尝试使用手机QQ扫码登录
2. 在命令行使用 `login 你的QQ号 你的密码 protocol=ANDROID_PHONE` 切换登录协议
3. 可以尝试不同的协议：ANDROID_PHONE、ANDROID_PAD、MACOS 等

### 5.2 网络问题

1. 确保防火墙没有阻止 Mirai 的网络通信
2. 检查 Mirai HTTP API 端口是否开放

### 5.3 消息发送失败

1. 检查目标QQ是否为机器人的好友
2. 检查验证密钥是否正确
3. 查看 Mirai 控制台日志排查问题

## 6. 相关资源

- [Mirai 官方文档](https://github.com/mamoe/mirai/blob/dev/docs/README.md)
- [Mirai HTTP API 文档](https://github.com/project-mirai/mirai-api-http/blob/master/docs/api/API.md)
- [MCL 使用指南](https://github.com/iTXTech/mirai-console-loader/blob/master/README.md) 