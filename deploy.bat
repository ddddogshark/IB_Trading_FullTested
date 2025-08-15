@echo off
chcp 65001 >nul
echo ========================================
echo TQQQ Trading Strategy EXE Builder
echo ========================================
echo.

echo 🚀 开始构建exe文件...
echo.

REM 激活Poetry环境并运行构建脚本
poetry run python build_exe.py

echo.
echo ========================================
echo 构建完成！
echo ========================================
echo.
echo 📁 输出文件位置: dist\TQQQ_Trading.exe
echo 📋 配置文件: dist\email_config.json
echo.
echo 💡 部署说明:
echo    1. 将dist目录复制到目标机器
echo    2. 编辑email_config.json配置邮件
echo    3. 运行TQQQ_Trading.exe
echo.
pause 