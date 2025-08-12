@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ智能交易策略 - 快速测试
echo ========================================
echo.

:: 进入项目目录
cd /d "%~dp0ib_async"

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 设置环境变量
set PYTHONIOENCODING=utf-8

:: 运行快速测试
echo 🧪 运行快速测试...
python -u debug_test.py

echo.
echo 测试完成!
pause 