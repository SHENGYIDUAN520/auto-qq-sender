# Mirai 快速安装指南

## 1. 安装 Java 11

1. 下载 AdoptOpenJDK: https://adoptium.net/temurin/releases/
2. 选择 Java 11 (LTS)，Windows x64 installer
3. 安装并重启电脑

## 2. 安装 Mirai

1. 创建 Mirai 目录:
```powershell
New-Item -Path "mirai" -ItemType Directory -Force
Set-Location -Path "mirai"
```

2. 下载 MCL:
```powershell
Invoke-WebRequest -Uri "https://github.com/iTXTech/mirai-console-loader/releases/download/v2.1.2/mcl-2.1.2.zip" -OutFile "mcl.zip"
Expand-Archive -Path "mcl.zip" -DestinationPath "." -Force
```

3. 启动 MCL:
```powershell
.\mcl.cmd
```

4. 安装 Mirai HTTP API 插件:
在 MCL 控制台中输入:
```
./mcl --update-package net.mamoe:mirai-api-http --channel stable --type plugin
```

5. 重启 MCL 后登录 QQ:
```
login 你的QQ号 你的密码
```

## 3. 配置 HTTP API

1. 编辑 `config/net.mamoe.mirai-api-http/setting.yml`:
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

## 4. 发送消息测试

```powershell
python scripts/mirai_sender.py --target 目标QQ号 --verify-key 你的验证密钥 --message "查寝测试消息"
```

## 5. 设置自动任务

1. 打开任务计划程序
2. 创建任务，设置每日晚上22:40执行
3. 操作设置为:
   - 程序: `python`
   - 参数: `scripts/mirai_sender.py --target 目标QQ号 --verify-key 你的验证密钥`
   - 起始位置: 项目目录 