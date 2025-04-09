@echo off
echo QQ查寝消息发送工具
echo ===================
echo.

set TARGET_QQ=替换为目标QQ号
set MESSAGE=查寝提醒：请在系统中填写查寝码%RANDOM:~-3%，若请假请忽略此条消息，谢谢。

python scripts/direct_sender.py --target %TARGET_QQ% --local --message "%MESSAGE%"

echo.
echo 按任意键退出...
pause > nul 