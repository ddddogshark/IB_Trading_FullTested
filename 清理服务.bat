@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"

echo ========================================
echo TQQQ策略服务清理工具
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo ❌ 需要管理员权限才能清理Windows服务
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ✅ 管理员权限检查通过
echo.

:: 检查服务是否存在
echo [1/4] 检查服务状态...
sc query "TQQQStrategy" >nul 2>&1
if errorlevel 1 (
    echo ✅ 服务不存在，无需清理
    pause
    exit /b 0
)

echo ⚠️ 发现TQQQStrategy服务
echo.

:: 停止服务
echo [2/4] 停止服务...
net stop "TQQQStrategy" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 服务可能已经停止或无法停止
) else (
    echo ✅ 服务已停止
)
timeout /t 2 /nobreak >nul

:: 使用NSSM删除
echo [3/4] 使用NSSM删除服务...
if exist "nssm.exe" (
    nssm.exe remove "TQQQStrategy" confirm >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ NSSM删除失败
    ) else (
        echo ✅ NSSM删除成功
    )
) else (
    echo ⚠️ NSSM工具不存在
)

:: 使用sc删除
echo [4/4] 使用sc删除服务...
sc delete "TQQQStrategy" >nul 2>&1
if errorlevel 1 (
    echo ❌ sc删除失败
) else (
    echo ✅ sc删除成功
)

echo.
echo ⏳ 等待服务完全清理...
timeout /t 3 /nobreak >nul

:: 最终检查
echo.
echo [最终检查] 验证服务是否已删除...
sc query "TQQQStrategy" >nul 2>&1
if errorlevel 1 (
    echo ✅ 服务已成功删除
) else (
    echo ❌ 服务仍然存在，可能需要重启后重试
)

echo.
echo 按任意键退出...
pause >nul 