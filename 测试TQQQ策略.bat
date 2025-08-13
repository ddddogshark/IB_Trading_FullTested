@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略测试器
echo ========================================
echo.

:: 检查Python是否安装
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 尝试使用py命令...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python未安装或未添加到PATH
        echo 请先安装Python 3.8+
        pause
        exit /b 1
    ) else (
        echo ✅ 使用py命令找到Python
        set PYTHON_CMD=py
    )
) else (
    echo ✅ Python环境检查通过
    set PYTHON_CMD=python
)

:: 进入项目目录
echo.
echo [2/4] 进入项目目录...
cd /d "%~dp0ib_async"
if errorlevel 1 (
    echo ❌ 无法进入项目目录
    pause
    exit /b 1
)
echo ✅ 已进入项目目录: %CD%

:: 激活虚拟环境
echo.
echo [3/4] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境激活成功

:: 运行测试
echo.
echo [4/4] 运行策略测试...
echo ========================================
echo 🧪 TQQQ策略功能测试
echo ========================================
echo    - 连接IB Gateway测试
echo    - TQQQ合约创建测试
echo    - 历史数据获取测试
echo    - EMA计算测试
echo    - 账户信息测试
echo ========================================
echo.
echo ⚠️  注意: 如果IB Gateway未运行，连接测试会失败
echo ========================================
echo.
echo 🚀 正在运行测试...
echo.

:: 运行测试脚本
%PYTHON_CMD% -u test_strategy.py

:: 如果程序异常退出
if errorlevel 1 (
    echo.
    echo ❌ 测试运行异常退出
    echo 请检查:
    echo   1. Python环境是否正确
    echo   2. 依赖包是否安装完整
    echo   3. IB Gateway是否正常运行
    echo.
    pause
) else (
    echo.
    echo ✅ 测试完成
    pause
) 