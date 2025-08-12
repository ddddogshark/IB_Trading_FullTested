@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 设置控制台编码
powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
set PYTHONIOENCODING=utf-8

echo ========================================
echo TQQQ智能交易策略 - Windows部署脚本
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

:: 检查Git
call :log_step "检查Git..."
git --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Git未安装，请先安装Git"
    call :log_info "下载地址: https://git-scm.com/downloads"
    pause
    exit /b 1
)
call :log_info "Git已安装"

:: 克隆项目
call :log_step "克隆项目..."
if exist "IB_Trading" (
    call :log_info "项目目录已存在，正在更新..."
    cd IB_Trading
    git pull
) else (
    call :log_info "正在克隆项目..."
    git clone https://github.com/ddddogshark/IB_Trading.git
    cd IB_Trading
)

:: 创建虚拟环境
call :log_step "创建Python虚拟环境..."
if not exist "venv" (
    %PYTHON_CMD% -m venv venv
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
pip install -r requirements.txt
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

:: 创建启动脚本
call :log_step "创建Windows启动脚本..."
(
echo @echo off
echo chcp 65001 ^>nul
echo setlocal enabledelayedexpansion
echo powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
echo set PYTHONIOENCODING=utf-8
echo echo 启动TQQQ智能交易策略...
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python -u ib_async\tqqq_final_trading.py
echo pause
) > start-trading.bat

:: 创建测试脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo setlocal enabledelayedexpansion
echo powershell -Command "& {[Console]::OutputEncoding = [System.Text.Encoding]::UTF8}"
echo set PYTHONIOENCODING=utf-8
echo echo 测试TQQQ智能交易策略...
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python -u ib_async\test_strategy.py
echo pause
) > test-trading.bat

call :log_info "Windows启动脚本创建成功"

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
echo 1. 双击 start-trading.bat 启动策略
echo 2. 双击 test-trading.bat 测试策略
echo 3. 手动运行: venv\Scripts\activate ^&^& python ib_async\tqqq_final_trading.py
echo.
echo 注意事项:
echo - 确保IB Gateway已启动并监听端口4001
echo - 确保账户有足够资金进行交易
echo - 这是实盘交易，将实际扣款
echo.
echo ========================================
pause 