# Message Sending Test Script

$workingDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptPath = Join-Path $workingDir "scripts\mirai_sender.py"

Write-Host "===== Check-in Message Sending Test ====="
Write-Host "Current directory: $workingDir"

# Run test mode
Write-Host "`nTest mode - No actual message will be sent:"
python $scriptPath --target 1234567890 --verify-key anykey --test

# Try to send a real message
$doRealSend = Read-Host "`nDo you want to try sending a real message? (y/n)"

if ($doRealSend -eq "y") {
    $targetQQ = Read-Host "Enter target QQ number"
    $verifyKey = Read-Host "Enter verification key"
    $message = Read-Host "Enter message content (leave empty for random code)"
    
    if ([string]::IsNullOrEmpty($message)) {
        python $scriptPath --target $targetQQ --verify-key $verifyKey
    } else {
        python $scriptPath --target $targetQQ --verify-key $verifyKey --message $message
    }
} else {
    Write-Host "Skipping actual message test"
}

Write-Host "`nTest completed!" 