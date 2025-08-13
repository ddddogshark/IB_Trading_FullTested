@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo TQQQ策略Windows服务管理器
echo ========================================
echo.

:menu
echo 请选择操作:
echo.
echo [1] 查看服务状态
echo [2] 启动服务
echo [3] 停止服务
echo [4] 重启服务
echo [5] 查看服务日志
echo [6] 查看错误日志
echo [7] 安装服务
echo [8] 删除服务
echo [0] 退出
echo.
set /p choice=请输入选项 (0-8): 

if "%choice%"=="1" goto status
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto error_logs
if "%choice%"=="7" goto install
if "%choice%"=="8" goto remove
if "%choice%"=="0" goto exit
echo 无效选项，请重新选择
goto menu

:status
echo.
echo ========================================
echo 查看服务状态
echo ========================================
echo.
sc query "TQQQStrategy"
echo.
pause
goto menu

:start
echo.
echo ========================================
echo 启动服务
echo ========================================
echo.
echo 正在启动TQQQ策略服务...
net start TQQQStrategy
if errorlevel 1 (
    echo 服务启动失败
    echo 请检查:
    echo 1. 服务是否已安装
    echo 2. 是否有管理员权限
    echo 3. 查看错误日志
) else (
    echo 服务启动成功！
    echo 策略现在将在后台持续运行
)
echo.
pause
goto menu

:stop
echo.
echo ========================================
echo 停止服务
echo ========================================
echo.
echo 正在停止TQQQ策略服务...
net stop TQQQStrategy
if errorlevel 1 (
    echo 服务停止失败
    echo 请检查服务状态
) else (
    echo 服务停止成功！
)
echo.
pause
goto menu

:restart
echo.
echo ========================================
echo 重启服务
echo ========================================
echo.
echo 正在重启TQQQ策略服务...
net stop TQQQStrategy >nul 2>&1
timeout /t 3 /nobreak >nul
net start TQQQStrategy
if errorlevel 1 (
    echo 服务重启失败
) else (
    echo 服务重启成功！
)
echo.
pause
goto menu

:logs
echo.
echo ========================================
echo 查看服务日志
echo ========================================
echo.
if exist "ib_async\service.log" (
    echo 最近50行服务日志:
    echo.
    powershell -Command "& {Get-Content 'ib_async\service.log' -Tail 50}"
) else (
    echo 服务日志文件不存在
    echo 可能原因:
    echo 1. 服务未启动
    echo 2. 服务未正确安装
    echo 3. 日志文件路径错误
)
echo.
pause
goto menu

:error_logs
echo.
echo ========================================
echo 查看错误日志
echo ========================================
echo.
if exist "ib_async\service_error.log" (
    echo 最近50行错误日志:
    echo.
    powershell -Command "& {Get-Content 'ib_async\service_error.log' -Tail 50}"
) else (
    echo 没有错误日志文件
    echo 这通常表示服务运行正常
)
echo.
pause
goto menu

:install
echo.
echo ========================================
echo 安装服务
echo ========================================
echo.
echo 需要管理员权限才能安装服务
echo 请以管理员身份运行 install_service.bat
echo.
echo 是否现在打开安装脚本? (Y/N)
set /p open_install=请选择: 
if /i "%open_install%"=="Y" (
    start "" "install_service.bat"
)
echo.
pause
goto menu

:remove
echo.
echo ========================================
echo 删除服务
echo ========================================
echo.
echo 警告: 删除服务将停止策略运行
echo.
set /p confirm=确认要删除服务吗? (y/N): 
if /i not "%confirm%"=="y" goto menu

echo.
echo 正在删除TQQQ策略服务...
if exist "nssm.exe" (
    nssm.exe remove "TQQQStrategy" confirm
    if errorlevel 1 (
        echo 服务删除失败
    ) else (
        echo 服务删除成功！
    )
) else (
    echo NSSM工具不存在
    echo 请先运行 install_service.bat 安装NSSM工具
)
echo.
pause
goto menu

:exit
echo.
echo 感谢使用TQQQ策略Windows服务管理器！
echo.
exit /b 0 