@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ Trading Strategy Launcher
echo ========================================
echo.
echo Starting strategy...
echo Please ensure IB Gateway is running
echo Press Ctrl+C to exit safely
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python and add to PATH
    pause
    exit /b 1
)

REM Check if dependencies are installed
py -c "import pandas, numpy, pytz" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    echo.
    py -m pip install pandas numpy pytz ib_async
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
)

REM Start strategy
py "%~dp0tqqq_final_trading.py"

echo.
echo Strategy exited
pause 