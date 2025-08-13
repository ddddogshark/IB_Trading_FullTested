@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"

echo ========================================
echo TQQQ策略环境检测工具
echo ========================================
echo.

echo 🔍 正在检测Python环境...
echo.

:: 方法1: 检查python命令
echo [方法1] 检查python命令...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ python命令不可用
) else (
    echo ✅ python命令可用
    python --version
)

:: 方法2: 检查py命令
echo.
echo [方法2] 检查py命令...
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ py命令不可用
) else (
    echo ✅ py命令可用
    py --version
)

:: 方法3: 检查Python安装路径
echo.
echo [方法3] 检查Python安装路径...
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ 在PATH中找不到python
) else (
    echo ✅ 在PATH中找到python
    where python
)

where py >nul 2>&1
if errorlevel 1 (
    echo ❌ 在PATH中找不到py
) else (
    echo ✅ 在PATH中找到py
    where py
)

:: 检查项目环境
echo.
echo [方法4] 检查项目环境...
if exist "ib_async\venv\Scripts\activate.bat" (
    echo ✅ 项目虚拟环境存在
) else (
    echo ❌ 项目虚拟环境不存在
)

if exist "ib_async\tqqq_trading.py" (
    echo ✅ 主策略文件存在
) else (
    echo ❌ 主策略文件不存在
)

if exist "requirements.txt" (
    echo ✅ 依赖文件存在
) else (
    echo ❌ 依赖文件不存在
)

echo.
echo ========================================
echo 检测完成
echo ========================================
echo.
echo 📋 建议:
echo 1. 如果所有方法都失败，请安装Python 3.8+
echo 2. 安装时勾选"Add Python to PATH"选项
echo 3. 或者手动将Python路径添加到系统PATH环境变量
echo 4. 运行"启动TQQQ策略.bat"可以自动创建虚拟环境
echo.
pause 