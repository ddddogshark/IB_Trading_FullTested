@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略 - 智能启动
echo ========================================
echo.

:: 进入项目目录
cd /d "%~dp0ib_async"

:: 智能检测Python路径
echo 🔍 智能检测Python环境...

:: 方法1: 检查系统PATH中的python
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ 找到系统Python
    set PYTHON_CMD=python
    goto :found_python
)

:: 方法2: 检查py启动器
py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ 找到py启动器
    set PYTHON_CMD=py
    goto :found_python
)

:: 方法3: 检查虚拟环境中的Python
if exist "venv\Scripts\python.exe" (
    echo ✅ 找到虚拟环境Python
    set PYTHON_CMD=venv\Scripts\python.exe
    goto :found_python
)

:: 方法4: 搜索常见Python安装路径
echo 🔍 搜索Python安装路径...
for %%p in (
    "C:\Python39\python.exe"
    "C:\Python310\python.exe"
    "C:\Python311\python.exe"
    "C:\Python312\python.exe"
    "C:\Python313\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files (x86)\Python39\python.exe"
    "C:\Program Files (x86)\Python310\python.exe"
    "C:\Program Files (x86)\Python311\python.exe"
    "C:\Program Files (x86)\Python312\python.exe"
    "C:\Program Files (x86)\Python313\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\py.exe"
) do (
    if exist %%p (
        echo ✅ 找到Python: %%p
        set PYTHON_CMD=%%p
        goto :found_python
    )
)

:: 如果都找不到Python
echo ❌ 无法找到Python安装
echo.
echo 📋 请尝试以下解决方案:
echo 1. 安装Python 3.8+ (推荐)
echo 2. 确保安装时勾选"Add Python to PATH"
echo 3. 或者运行 "启动策略.bat" 来创建虚拟环境
echo.
pause
exit /b 1

:found_python
echo.
echo 🎯 使用Python: %PYTHON_CMD%
echo.

:: 检查虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️ 虚拟环境不存在，正在创建...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ❌ 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
) else (
    echo ✅ 虚拟环境已存在
)

:: 激活虚拟环境
echo 🔄 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境激活成功

:: 安装依赖
echo 📦 检查依赖...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖检查完成

:: 显示策略信息
echo.
echo ========================================
echo 📊 策略信息:
echo    - 策略名称: TQQQ智能交易策略
echo    - 交易标的: TQQQ (3倍杠杆纳斯达克ETF)
echo    - 信号指标: EMA20移动平均线
echo    - 交易条件: 昨日收盘价 > EMA20时买入
echo    - 仓位大小: 账户资金的10%
echo    - 检查时间: 每天北京时间21:20
echo    - 交易模式: 实盘交易 (将实际扣款!)
echo ========================================
echo.
echo ⚠️  重要提醒:
echo    1. 确保IB Gateway已启动并连接到端口4001
echo    2. 确保账户有足够资金进行交易
echo    3. 这是实盘交易，将实际扣款并执行交易
echo    4. 按Ctrl+C可以安全退出程序
echo ========================================
echo.
echo 🚀 正在启动策略...
echo.

:: 运行策略
python -u tqqq_final_trading.py

:: 如果程序异常退出
if errorlevel 1 (
    echo.
    echo ❌ 策略运行异常退出
    echo 请检查:
    echo   1. IB Gateway是否正常运行
    echo   2. 网络连接是否正常
    echo   3. 账户权限是否正确
    echo.
    pause
) else (
    echo.
    echo ✅ 策略正常退出
    pause
) 