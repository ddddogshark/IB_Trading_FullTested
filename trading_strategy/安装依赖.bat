@echo off
chcp 65001 >nul
echo ========================================
echo 安装TQQQ交易策略依赖
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

echo 正在安装依赖包...
echo.

REM 安装依赖
pip install pandas numpy pytz ib_async

if errorlevel 1 (
    echo.
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 依赖安装完成！
echo 现在可以运行启动策略.bat了
pause 