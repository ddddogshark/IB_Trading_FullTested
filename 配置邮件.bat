@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo TQQQ策略邮件配置工具
echo ========================================
echo.

echo 此工具将帮助您配置163邮箱的SMTP密码
echo 注意: 您需要在163邮箱中开启SMTP服务并获取授权码
echo.

echo 配置说明:
echo 1. 登录163邮箱网页版
echo 2. 进入设置 - 客户端授权密码
echo 3. 开启SMTP服务
echo 4. 获取授权码（不是登录密码）
echo.

set /p confirm=是否继续配置? (Y/N): 
if /i not "%confirm%"=="Y" goto exit

echo.
echo 请输入163邮箱的SMTP授权码:
echo 注意: 这是授权码，不是登录密码
set /p password=授权码: 

if "%password%"=="" (
    echo 授权码不能为空
    pause
    goto exit
)

echo.
echo 正在创建配置文件...

:: 创建Python脚本来配置邮件
echo import json > temp_config.py
echo config = { >> temp_config.py
echo     "smtp_server": "smtp.163.com", >> temp_config.py
echo     "smtp_port": 587, >> temp_config.py
echo     "sender_email": "a36602476@163.com", >> temp_config.py
echo     "receiver_email": "a36602476@163.com", >> temp_config.py
echo     "password": "%password%" >> temp_config.py
echo } >> temp_config.py
echo with open('ib_async/email_config.json', 'w', encoding='utf-8') as f: >> temp_config.py
echo     json.dump(config, f, indent=4, ensure_ascii=False) >> temp_config.py
echo print("邮件配置已保存") >> temp_config.py

python temp_config.py
if errorlevel 1 (
    echo 配置失败，请检查Python环境
) else (
    echo.
    echo ✅ 邮件配置成功！
    echo 配置文件已保存到: ib_async/email_config.json
    echo.
    echo 测试邮件功能:
    echo 1. 运行策略时会自动发送交易通知
    echo 2. 每天21:28会发送每日总结
    echo 3. 异常时会发送错误通知
)

del temp_config.py >nul 2>&1

:exit
echo.
echo 按任意键退出...
pause >nul 