@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"

echo ========================================
echo TQQQ策略持续运行模式
echo ========================================
echo.

echo ⚠️  重要提醒:
echo    1. 持续运行模式会一直运行，直到手动停止
echo    2. 每天北京时间21:20自动检查并执行交易
echo    3. 按Ctrl+C可以安全停止程序
echo    4. 确保IB Gateway已启动并连接到端口4001
echo    5. 这是实盘交易，将实际扣款并执行交易
echo ========================================
echo.

:: 检查Python环境
echo [1/5] 检查Python环境...
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

:: 切换到项目目录
echo [2/5] 切换到项目目录...
cd /d "%~dp0ib_async"
if errorlevel 1 (
    echo ❌ 切换到项目目录失败
    pause
    exit /b 1
)
echo ✅ 已切换到项目目录

:: 检查虚拟环境
echo [3/5] 检查虚拟环境...
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️ 虚拟环境不存在，正在创建...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

:: 激活虚拟环境
echo [4/5] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境已激活

:: 安装依赖
echo [5/5] 检查依赖包...
pip install -r ..\requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 依赖安装失败，尝试重新安装...
    pip install -r ..\requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)
echo ✅ 依赖包检查完成

echo.
echo 🔄 启动持续运行模式...
echo 📅 策略将在每天21:20自动执行
echo 🛑 按Ctrl+C停止程序
echo.

:: 运行持续模式
%PYTHON_CMD% -u tqqq_trading.py --continuous

if errorlevel 1 (
    echo.
    echo ❌ 策略运行失败
    echo 请检查:
    echo 1. IB Gateway是否已启动
    echo 2. 网络连接是否正常
    echo 3. 账户权限是否正确
    echo.
    pause
) else (
    echo.
    echo ✅ 策略已停止
)

pause 