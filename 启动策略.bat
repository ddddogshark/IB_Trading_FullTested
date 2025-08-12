@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略启动器
echo ========================================
echo.

:: 检查Python是否安装
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 尝试使用py命令...
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python未安装或未添加到PATH
        echo 请先安装Python 3.8+
        echo 或者将Python添加到系统PATH环境变量中
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
echo [2/6] 进入项目目录...
cd /d "%~dp0ib_async"
if errorlevel 1 (
    echo ❌ 无法进入项目目录
    pause
    exit /b 1
)
echo ✅ 已进入项目目录: %CD%

:: 检查虚拟环境
echo.
echo [3/6] 检查虚拟环境...
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
echo.
echo [4/6] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虚拟环境激活失败
    pause
    exit /b 1
)
echo ✅ 虚拟环境激活成功

:: 安装依赖
echo.
echo [5/6] 检查并安装依赖...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖检查完成

:: 显示策略信息
echo.
echo [6/6] 启动TQQQ智能交易策略...
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
%PYTHON_CMD% -u tqqq_final_trading.py

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