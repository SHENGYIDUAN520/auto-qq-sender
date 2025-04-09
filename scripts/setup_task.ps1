$taskName = "AutoQQSender"
$workingDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptPath = Join-Path $workingDir "scripts\mirai_sender.py"
$action = New-ScheduledTaskAction -Execute "python" -Argument "$scriptPath --target 目标QQ号 --verify-key yourVerifyKey --test" -WorkingDirectory $workingDir

# 设置每天晚上22:40执行
$trigger = New-ScheduledTaskTrigger -Daily -At 22:40

# 创建任务
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Description "自动发送QQ查寝消息" -RunLevel Highest 