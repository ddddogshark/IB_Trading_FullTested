@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略测试工具
echo ========================================
echo.

:: 进入项目目录
cd /d "%~dp0ib_async"

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 运行测试脚本
python -u test_strategy.py

if errorlevel 1 (
    echo.
    echo ❌ 测试运行异常退出
    echo 请检查:
    echo   1. IB Gateway是否正常运行
    echo   2. 网络连接是否正常
    echo   3. 账户权限是否正确
    echo.
)

pause 