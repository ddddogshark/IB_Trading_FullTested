@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"

echo ========================================
echo Python环境自动修复工具
echo ========================================
echo.

echo 🔧 正在尝试修复Python环境...
echo.

:: 检查并尝试修复Python路径
set FIXED=0

:: 方法1: 尝试使用py命令
echo [方法1] 尝试使用py命令...
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ py命令可用，正在设置环境变量...
    set PYTHON_CMD=py
    set FIXED=1
    goto :success
)

:: 方法2: 尝试使用python命令
echo [方法2] 尝试使用python命令...
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ python命令可用，正在设置环境变量...
    set PYTHON_CMD=python
    set FIXED=1
    goto :success
)

:: 方法3: 尝试常见Python路径
echo [方法3] 尝试常见Python路径...
for %%p in (
    "C:\Python39\python.exe"
    "C:\Python310\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
) do (
    if exist %%p (
        echo ✅ 找到Python: %%p
        set PYTHON_CMD=%%p
        set FIXED=1
        goto :success
    )
)

:: 如果都失败了
echo ❌ 无法找到Python安装
echo.
echo 📋 请尝试以下解决方案:
echo 1. 安装Python 3.8+ (推荐)
echo 2. 确保安装时勾选"Add Python to PATH"
echo 3. 使用"简单启动.bat"直接运行策略
echo.
pause
exit /b 1

:success
echo.
echo ✅ Python环境修复成功!
echo 使用命令: %PYTHON_CMD%
echo.

:: 测试Python功能
echo 🧪 测试Python功能...
%PYTHON_CMD% --version
if errorlevel 1 (
    echo ❌ Python测试失败
    pause
    exit /b 1
)

echo.
echo 🎉 修复完成! 现在可以运行策略了
echo.
echo 📋 下一步:
echo 1. 双击 "启动策略.bat" 启动策略
echo 2. 或双击 "简单启动.bat" 快速启动
echo.
pause 