@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ智能交易策略测试工具
echo ========================================
echo.

:: 进入项目目录
cd /d "%~dp0ib_async"

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 运行测试脚本
python -u test_strategy.py

pause 