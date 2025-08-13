@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo TQQQ策略邮件测试工具
echo ========================================
echo.

echo 此工具将测试邮件发送功能
echo.

:: 检查配置文件
if not exist "ib_async\email_config.json" (
    echo ❌ 邮件配置文件不存在
    echo 请先运行 配置邮件.bat 进行配置
    pause
    goto exit
)

echo ✅ 邮件配置文件存在
echo.

:: 创建测试脚本
echo import sys > test_email.py
echo import os >> test_email.py
echo sys.path.append('ib_async') >> test_email.py
echo from email_notifier import email_notifier >> test_email.py
echo. >> test_email.py
echo print("正在发送测试邮件...") >> test_email.py
echo. >> test_email.py
echo # 发送测试邮件 >> test_email.py
echo test_info = { >> test_email.py
echo     'action': '测试', >> test_email.py
echo     'status': '成功', >> test_email.py
echo     'quantity': 100, >> test_email.py
echo     'amount': 5000.00, >> test_email.py
echo     'price': 50.00, >> test_email.py
echo     'current_price': 50.00, >> test_email.py
echo     'ema20': 48.50, >> test_email.py
echo     'account_balance': 100000.00, >> test_email.py
echo     'current_position': 0, >> test_email.py
echo     'price_above_ema': True, >> test_email.py
echo     'notes': '这是一封测试邮件，用于验证邮件通知功能是否正常工作' >> test_email.py
echo } >> test_email.py
echo. >> test_email.py
echo success = email_notifier.send_trading_notification(test_info) >> test_email.py
echo. >> test_email.py
echo if success: >> test_email.py
echo     print("✅ 测试邮件发送成功！") >> test_email.py
echo     print("请检查您的邮箱 a36602476@163.com") >> test_email.py
echo else: >> test_email.py
echo     print("❌ 测试邮件发送失败") >> test_email.py
echo     print("请检查邮件配置和网络连接") >> test_email.py

:: 运行测试
echo 正在测试邮件发送功能...
python test_email.py

if errorlevel 1 (
    echo.
    echo ❌ 邮件测试失败
    echo 可能的原因:
    echo 1. 邮件配置错误
    echo 2. 网络连接问题
    echo 3. 163邮箱SMTP服务未开启
    echo 4. 授权码错误
) else (
    echo.
    echo ✅ 邮件测试完成
    echo 请检查您的邮箱是否收到测试邮件
)

:: 清理临时文件
del test_email.py >nul 2>&1

:exit
echo.
echo 按任意键退出...
pause >nul 