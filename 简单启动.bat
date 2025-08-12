@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

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

:: 运行策略
venv\Scripts\python.exe -u tqqq_final_trading.py

if errorlevel 1 (
    echo.
    echo ❌ 策略运行异常退出
    echo 请检查:
    echo   1. IB Gateway是否正常运行
    echo   2. 网络连接是否正常
    echo   3. 账户权限是否正确
    echo.
) else (
    echo.
    echo ✅ 策略正常退出
)

pause 