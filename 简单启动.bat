@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ智能交易策略 - 简单启动
echo ========================================
echo.

:: 进入项目目录
cd /d "%~dp0ib_async"

:: 检查虚拟环境是否存在
if not exist "venv\Scripts\python.exe" (
    echo ❌ 虚拟环境不存在
    echo 请先运行 "启动策略.bat" 来创建虚拟环境
    pause
    exit /b 1
)

:: 直接使用虚拟环境中的Python
echo 🚀 启动策略...
echo.

:: 设置环境变量
set PYTHONIOENCODING=utf-8

:: 运行策略
venv\Scripts\python.exe -u tqqq_final_trading.py

echo.
echo 策略已退出
pause 