@echo off
chcp 65001 >nul
echo ========================================
echo Python环境检测工具
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

:: 方法4: 检查常见Python安装路径
echo.
echo [方法4] 检查常见Python安装路径...
set PYTHON_PATHS=^
C:\Python*;^
C:\Program Files\Python*;^
C:\Program Files (x86)\Python*;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python*;^
C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\py.exe

for %%p in (%PYTHON_PATHS%) do (
    if exist "%%p" (
        echo ✅ 找到Python: %%p
    )
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
echo.
pause 