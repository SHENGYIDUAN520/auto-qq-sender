# 查寝消息测试脚本

$workingDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptPath = Join-Path $workingDir "scripts\mirai_sender.py"

Write-Host "===== 查寝消息发送测试 ====="
Write-Host "当前工作目录: $workingDir"

# 运行测试模式
Write-Host "`n测试模式 - 不实际发送消息:"
python $scriptPath --target 1234567890 --verify-key anykey --test

# 尝试实际发送
$doRealSend = Read-Host "`n是否尝试实际发送消息? (y/n)"

if ($doRealSend -eq "y") {
    $targetQQ = Read-Host "请输入目标QQ号"
    $verifyKey = Read-Host "请输入验证密钥"
    $message = Read-Host "请输入消息内容 (留空则使用随机代码)"
    
    if ([string]::IsNullOrEmpty($message)) {
        python $scriptPath --target $targetQQ --verify-key $verifyKey
    } else {
        python $scriptPath --target $targetQQ --verify-key $verifyKey --message $message
    }
} else {
    Write-Host "跳过实际发送测试"
}

Write-Host "`n测试完成!" 