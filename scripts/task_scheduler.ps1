# PowerShell 脚本：设置定时任务发送查寝消息

# 任务名称
$taskName = "QQ查寝消息"

# 脚本路径
$scriptPath = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "direct_sender.py"
$workDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

# 目标QQ号 - 请替换为实际的QQ号
$targetQQ = "替换为目标QQ号"

# Python执行路径
$pythonPath = "python"

# 命令参数
$scriptArgument = "$scriptPath --target $targetQQ --local"

# 创建任务动作 - 使用本地模式
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptArgument -WorkingDirectory $workDir

# 创建触发器 - 每天晚上22:40触发
$trigger = New-ScheduledTaskTrigger -Daily -At "22:40"

# 创建任务设置
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

# 注册任务
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force

Write-Host "查寝消息定时任务已创建，将在每天晚上 22:40 自动发送消息" -ForegroundColor Green
Write-Host "目标QQ号: $targetQQ" -ForegroundColor Yellow
Write-Host "使用本地模拟模式，只会在本地打印消息而不实际发送" -ForegroundColor Yellow
Write-Host "如需真实发送，请修改脚本参数并提供消息服务器URL和令牌" -ForegroundColor Yellow 