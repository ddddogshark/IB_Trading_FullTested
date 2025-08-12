#!/bin/bash

# TQQQ智能交易策略自动化部署脚本
# 支持Docker和传统部署两种方式

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查系统
check_system() {
    log_step "检查系统环境..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log_info "检测到Linux系统"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log_info "检测到macOS系统"
    else
        log_error "不支持的操作系统: $OSTYPE"
        exit 1
    fi
    
    # 检查是否为root用户
    if [[ $EUID -eq 0 ]]; then
        log_warn "检测到root用户，建议使用普通用户运行"
    fi
}

# 安装Docker
install_docker() {
    log_step "安装Docker..."
    
    if command -v docker &> /dev/null; then
        log_info "Docker已安装"
        return 0
    fi
    
    if [[ "$OS" == "linux" ]]; then
        log_info "正在安装Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        log_info "Docker安装完成，请重新登录以应用用户组权限"
    else
        log_error "请手动安装Docker Desktop"
        exit 1
    fi
}

# 安装Docker Compose
install_docker_compose() {
    log_step "安装Docker Compose..."
    
    if command -v docker-compose &> /dev/null; then
        log_info "Docker Compose已安装"
        return 0
    fi
    
    if [[ "$OS" == "linux" ]]; then
        log_info "正在安装Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        log_info "Docker Compose安装完成"
    else
        log_error "请手动安装Docker Compose"
        exit 1
    fi
}

# 安装Python
install_python() {
    log_step "检查Python环境..."
    
    if command -v python3.12 &> /dev/null; then
        log_info "Python 3.12已安装"
        return 0
    fi
    
    if [[ "$OS" == "linux" ]]; then
        log_info "正在安装Python 3.12..."
        if command -v apt-get &> /dev/null; then
            # Ubuntu/Debian
            sudo apt update
            sudo apt install -y python3.12 python3.12-venv python3-pip
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            sudo yum install -y python3.12 python3.12-pip
        else
            log_error "不支持的包管理器"
            exit 1
        fi
        log_info "Python 3.12安装完成"
    else
        log_error "请手动安装Python 3.12"
        exit 1
    fi
}

# 克隆项目
clone_project() {
    log_step "克隆项目..."
    
    if [ -d "IB_Trading" ]; then
        log_info "项目目录已存在，正在更新..."
        cd IB_Trading
        git pull
    else
        log_info "正在克隆项目..."
        git clone https://github.com/ddddogshark/IB_Trading.git
        cd IB_Trading
    fi
}

# Docker部署
deploy_docker() {
    log_step "开始Docker部署..."
    
    # 创建必要目录
    mkdir -p logs config ib-config
    
    # 创建IB Gateway配置
    cat > ib-config/ibgateway.yaml << EOF
ibgateway:
  port: 4001
  host: 0.0.0.0
  log_level: INFO
  paper_trading: false
EOF
    
    # 启动服务
    log_info "启动Docker服务..."
    docker-compose up -d
    
    # 等待服务启动
    sleep 10
    
    # 检查服务状态
    if docker-compose ps | grep -q "Up"; then
        log_info "Docker服务启动成功！"
        log_info "查看日志: docker-compose logs -f tqqq-trading"
        log_info "停止服务: docker-compose down"
    else
        log_error "Docker服务启动失败"
        docker-compose logs
        exit 1
    fi
}

# 传统部署
deploy_traditional() {
    log_step "开始传统部署..."
    
    # 创建虚拟环境
    log_info "创建Python虚拟环境..."
    python3.12 -m venv venv
    source venv/bin/activate
    
    # 安装依赖
    log_info "安装Python依赖..."
    pip install -r requirements.txt
    
    # 创建配置目录
    mkdir -p logs config
    
    # 创建systemd服务文件
    if [[ "$OS" == "linux" ]]; then
        log_info "创建systemd服务..."
        sudo tee /etc/systemd/system/tqqq-trading.service > /dev/null << EOF
[Unit]
Description=TQQQ Trading Strategy
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python ib_async/tqqq_final_trading.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        # 启用服务
        sudo systemctl daemon-reload
        sudo systemctl enable tqqq-trading
        sudo systemctl start tqqq-trading
        
        log_info "传统部署完成！"
        log_info "查看状态: sudo systemctl status tqqq-trading"
        log_info "查看日志: sudo journalctl -u tqqq-trading -f"
    else
        log_info "传统部署完成！"
        log_info "启动策略: source venv/bin/activate && python ib_async/tqqq_final_trading.py"
    fi
}

# 创建监控脚本
create_monitor() {
    log_step "创建监控脚本..."
    
    cat > monitor.sh << 'EOF'
#!/bin/bash

# TQQQ交易策略监控脚本

LOG_FILE="logs/tqqq_trading.log"
SERVICE_NAME="tqqq-trading"

# 检查策略进程
check_process() {
    if ! pgrep -f "tqqq_final_trading.py" > /dev/null; then
        echo "$(date): 策略进程未运行，正在重启..."
        if command -v systemctl &> /dev/null; then
            sudo systemctl restart $SERVICE_NAME
        else
            # 手动重启
            cd "$(dirname "$0")"
            source venv/bin/activate
            nohup python ib_async/tqqq_final_trading.py > trading.log 2>&1 &
        fi
    fi
}

# 检查IB Gateway连接
check_connection() {
    if ! nc -z 127.0.0.1 4001 2>/dev/null; then
        echo "$(date): IB Gateway连接失败"
    fi
}

# 检查日志文件大小
check_log_size() {
    if [ -f "$LOG_FILE" ]; then
        log_size=$(du -m "$LOG_FILE" 2>/dev/null | cut -f1)
        if [ "$log_size" -gt 100 ] 2>/dev/null; then
            echo "$(date): 日志文件过大，正在轮转..."
            mv "$LOG_FILE" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S)"
        fi
    fi
}

# 主函数
main() {
    check_process
    check_connection
    check_log_size
}

main
EOF
    
    chmod +x monitor.sh
    
    # 添加到crontab
    if command -v crontab &> /dev/null; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * $(pwd)/monitor.sh") | crontab -
        log_info "监控脚本已添加到crontab"
    fi
}

# 显示帮助信息
show_help() {
    echo "TQQQ智能交易策略部署脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -d, --docker     使用Docker部署（推荐）"
    echo "  -t, --traditional 使用传统方式部署"
    echo "  -h, --help       显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -d            # Docker部署"
    echo "  $0 -t            # 传统部署"
}

# 主函数
main() {
    local deploy_type=""
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--docker)
                deploy_type="docker"
                shift
                ;;
            -t|--traditional)
                deploy_type="traditional"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 如果没有指定部署类型，询问用户
    if [[ -z "$deploy_type" ]]; then
        echo "请选择部署方式:"
        echo "1) Docker部署（推荐）"
        echo "2) 传统部署"
        read -p "请输入选择 (1/2): " choice
        
        case $choice in
            1)
                deploy_type="docker"
                ;;
            2)
                deploy_type="traditional"
                ;;
            *)
                log_error "无效选择"
                exit 1
                ;;
        esac
    fi
    
    # 开始部署
    log_info "开始TQQQ智能交易策略部署..."
    log_info "部署方式: $deploy_type"
    
    check_system
    
    if [[ "$deploy_type" == "docker" ]]; then
        install_docker
        install_docker_compose
    else
        install_python
    fi
    
    clone_project
    create_monitor
    
    if [[ "$deploy_type" == "docker" ]]; then
        deploy_docker
    else
        deploy_traditional
    fi
    
    log_info "部署完成！"
    log_info "项目目录: $(pwd)"
    log_info "日志目录: $(pwd)/logs"
}

# 运行主函数
main "$@" 