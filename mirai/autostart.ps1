$env:JAVA_HOME = 'C:\Program Files\Java\jdk-24'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# 启动 Mirai Console
Start-Process -FilePath "$env:JAVA_HOME\bin\java" -ArgumentList "-jar", "mcl.jar" -NoNewWindow

# 等待启动完成
Start-Sleep -Seconds 10

# 通过 mirai_sender.py 测试发送消息
# python ../scripts/mirai_sender.py --target 目标QQ号 --verify-key yourVerifyKey --message "查寝测试消息" 