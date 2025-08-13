@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"

echo ========================================
echo TQQQ策略Windows服务安装器
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo ❌ 需要管理员权限才能安装Windows服务
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ✅ 管理员权限检查通过
echo.

:: 检查Python环境
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo ✅ Python环境正常

:: 检查NSSM工具
echo [2/6] 检查NSSM工具...
if not exist "nssm.exe" (
    echo ⚠️ NSSM工具不存在，正在下载...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'}"
    if errorlevel 1 (
        echo ❌ 下载NSSM失败
        pause
        exit /b 1
    )
    
    echo 解压NSSM...
    powershell -Command "& {Expand-Archive -Path 'nssm.zip' -DestinationPath '.' -Force}"
    copy "nssm-2.24\win64\nssm.exe" "nssm.exe" >nul 2>&1
    rmdir /s /q "nssm-2.24" >nul 2>&1
    del "nssm.zip" >nul 2>&1
    echo ✅ NSSM工具准备完成
) else (
    echo ✅ NSSM工具已存在
)

:: 获取项目路径
echo [3/6] 获取项目路径...
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%
echo 项目路径: %PROJECT_PATH%
echo ✅ 路径获取完成

:: 检查服务是否已存在
echo [4/6] 检查现有服务...
sc query "TQQQStrategy" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️ 服务已存在，正在删除...
    nssm.exe remove "TQQQStrategy" confirm
    if errorlevel 1 (
        echo ❌ 删除现有服务失败
        pause
        exit /b 1
    )
    echo ✅ 现有服务已删除
)

:: 安装服务
echo [5/6] 安装Windows服务...
nssm.exe install "TQQQStrategy" "%PROJECT_PATH%\ib_async\venv\Scripts\python.exe" "%PROJECT_PATH%\ib_async\tqqq_trading.py --continuous"
if errorlevel 1 (
    echo ❌ 服务安装失败
    pause
    exit /b 1
)

:: 配置服务参数
echo [6/6] 配置服务参数...
nssm.exe set "TQQQStrategy" AppDirectory "%PROJECT_PATH%\ib_async"
nssm.exe set "TQQQStrategy" DisplayName "TQQQ智能交易策略"
nssm.exe set "TQQQStrategy" Description "TQQQ智能交易策略 - 基于EMA20的自动化交易系统"
nssm.exe set "TQQQStrategy" Start SERVICE_AUTO_START
nssm.exe set "TQQQStrategy" AppStdout "%PROJECT_PATH%\ib_async\service.log"
nssm.exe set "TQQQStrategy" AppStderr "%PROJECT_PATH%\ib_async\service_error.log"

echo.
echo ========================================
echo ✅ Windows服务安装完成！
echo ========================================
echo.
echo 服务名称: TQQQStrategy
echo 显示名称: TQQQ智能交易策略
echo 启动类型: 自动启动
echo 日志文件: %PROJECT_PATH%\ib_async\service.log
echo 错误日志: %PROJECT_PATH%\ib_async\service_error.log
echo.
echo 服务管理命令:
echo   启动服务: net start TQQQStrategy
echo   停止服务: net stop TQQQStrategy
echo   查看状态: sc query TQQQStrategy
echo   删除服务: nssm.exe remove TQQQStrategy confirm
echo.
echo 是否现在启动服务? (Y/N)
set /p start_service=请选择: 

if /i "%start_service%"=="Y" (
    echo.
    echo 🚀 启动TQQQ策略服务...
    net start TQQQStrategy
    if errorlevel 1 (
        echo ❌ 服务启动失败
        echo 请检查日志文件: %PROJECT_PATH%\ib_async\service_error.log
    ) else (
        echo ✅ 服务启动成功！
        echo 策略现在将在后台持续运行
        echo 每天21:20自动执行交易策略
    )
)

echo.
echo 按任意键退出...
pause >nul 