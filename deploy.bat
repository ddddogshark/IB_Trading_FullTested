@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ Trading Strategy Continuous EXE Builder
echo ========================================
echo.

echo 🚀 开始构建持续运行exe文件...
echo.

REM 激活Poetry环境并运行构建脚本
poetry run python build_exe.py

echo.
echo ========================================
echo 构建完成！
echo ========================================
echo.
echo 📁 输出文件位置: dist\TQQQ_Trading_Continuous.exe
echo 📋 配置文件: dist\email_config.json
echo 🚀 启动脚本: dist\start_trading.bat
echo.
echo 💡 部署说明:
echo    1. 将dist目录复制到目标机器
echo    2. 编辑email_config.json配置邮件
echo    3. 运行TQQQ_Trading_Continuous.exe (持续运行)
echo    4. 或运行start_trading.bat (推荐)
echo.
echo 🔄 持续运行特性:
echo    - 自动在指定时间执行交易
echo    - 24/7持续监控市场
echo    - 完整的邮件通知系统
echo    - 自动错误恢复
echo.
pause 