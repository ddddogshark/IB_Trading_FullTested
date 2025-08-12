@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略 - 一键部署工具
echo ========================================
echo.

:: 颜色定义
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "NC=[0m"

:: 日志函数
:log_info
echo %GREEN%[INFO]%NC% %~1
goto :eof

:log_warn
echo %YELLOW%[WARN]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:log_step
echo %BLUE%[STEP]%NC% %~1
goto :eof

:: 检查Python
call :log_step "检查Python环境..."
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        call :log_error "Python未安装，请先安装Python 3.8+"
        call :log_info "下载地址: https://www.python.org/downloads/"
        call :log_info "安装时请勾选'Add Python to PATH'选项"
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
        call :log_info "使用py命令"
    )
) else (
    set PYTHON_CMD=python
    call :log_info "使用python命令"
)

:: 进入项目目录
call :log_step "进入项目目录..."
cd /d "%~dp0ib_async"
if errorlevel 1 (
    call :log_error "无法进入项目目录"
    pause
    exit /b 1
)
call :log_info "项目目录: %CD%"

:: 创建虚拟环境
call :log_step "创建Python虚拟环境..."
if not exist "venv" (
    call :log_info "正在创建虚拟环境..."
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        call :log_error "虚拟环境创建失败"
        pause
        exit /b 1
    )
    call :log_info "虚拟环境创建成功"
) else (
    call :log_info "虚拟环境已存在"
)

:: 激活虚拟环境
call :log_step "激活虚拟环境..."
call venv\Scripts\activate.bat
if errorlevel 1 (
    call :log_error "虚拟环境激活失败"
    pause
    exit /b 1
)
call :log_info "虚拟环境激活成功"

:: 安装依赖
call :log_step "安装Python依赖..."
pip install -r ..\requirements.txt
if errorlevel 1 (
    call :log_error "依赖安装失败"
    pause
    exit /b 1
)
call :log_info "依赖安装成功"

:: 创建配置目录
call :log_step "创建配置目录..."
if not exist "logs" mkdir logs
if not exist "config" mkdir config
call :log_info "配置目录创建成功"

:: 显示部署结果
echo.
echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 项目目录: %CD%
echo 虚拟环境: %CD%\venv
echo 日志目录: %CD%\logs
echo.
echo 启动方式:
echo 1. 双击 "智能启动.bat" 智能启动策略
echo 2. 双击 "简单启动.bat" 快速启动策略
echo 3. 双击 "测试策略.bat" 测试策略
echo 4. 双击 "快速测试.bat" 快速测试
echo.
echo 注意事项:
echo - 确保IB Gateway已启动并监听端口4001
echo - 确保账户有足够资金进行交易
echo - 这是实盘交易，将实际扣款
echo.
echo ========================================
pause 