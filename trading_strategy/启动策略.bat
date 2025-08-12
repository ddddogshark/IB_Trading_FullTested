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

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 启动策略
python tqqq_final_trading.py

echo.
echo 策略已退出
pause 