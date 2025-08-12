@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ智能交易策略启动器
echo ========================================
echo.
echo 正在启动策略...
echo 请确保IB Gateway已运行
echo 按Ctrl+C可以安全退出
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import pandas, numpy, pytz" 2>nul
if errorlevel 1 (
    echo 错误: 缺少必要的依赖包
    echo 请运行: pip install pandas numpy pytz ib_async
    pause
    exit /b 1
)

REM 启动策略
python "%~dp0tqqq_final_trading.py"

echo.
echo 策略已退出
pause 