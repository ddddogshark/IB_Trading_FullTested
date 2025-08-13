# TQQQ智能交易策略

## 📊 项目概述

这是一个基于EMA20移动平均线的TQQQ自动化交易策略，使用Interactive Brokers (IB) API进行实盘交易。

## 🎯 策略特点

- **交易标的**: TQQQ (3倍杠杆纳斯达克ETF)
- **信号指标**: EMA20指数移动平均线
- **买入条件**: 昨日收盘价 > EMA20
- **仓位管理**: 账户资金的10%
- **执行时间**: 每天北京时间21:20自动检查
- **交易模式**: 实盘交易

## 📁 项目结构

```
IB_Trading/
├── ib_async/                    # 主项目目录
│   ├── tqqq_trading.py         # 主策略文件
│   ├── test_strategy.py        # 策略测试脚本
│   ├── venv/                   # Python虚拟环境
│   ├── tqqq_trading.log        # 策略日志文件
│   ├── service.log             # Windows服务日志
│   └── service_error.log       # Windows服务错误日志
├── requirements.txt             # Python依赖包
├── 启动TQQQ策略.bat            # 策略启动脚本
├── 持续运行策略.bat            # 持续运行脚本
├── 测试TQQQ策略.bat            # 策略测试脚本
├── 环境检测.bat                # 环境检测工具
├── install_service.bat         # Windows服务安装脚本
├── 服务管理.bat                # Windows服务管理脚本
└── README.md                   # 项目说明文件
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装：
- **操作系统**: Windows 10/11
- **Python**: 3.8+ (推荐3.11或3.12)
- **内存**: 至少4GB RAM
- **网络**: 稳定的互联网连接
- **Interactive Brokers Gateway**
- **有效的IB账户**

### 2. 启动方式

#### 方式一：使用批处理脚本（推荐）
```bash
# 检测环境
双击 "环境检测.bat"

# 启动策略（单次运行）
双击 "启动TQQQ策略.bat"

# 启动持续运行
双击 "持续运行策略.bat"

# 测试策略
双击 "测试TQQQ策略.bat"
```

#### 方式二：手动运行
```bash
# 进入项目目录
cd ib_async

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r ..\requirements.txt

# 运行策略（单次运行）
python tqqq_trading.py

# 运行持续模式
python tqqq_trading.py --continuous

# 运行测试
python test_strategy.py
```

## 📊 策略执行流程

### 第一步：环境初始化
```python
# 创建策略实例
strategy = TQQQSmartTradingStrategy(
    host='127.0.0.1',    # IB Gateway地址
    port=4001,           # IB Gateway端口
    client_id=444        # 客户端ID
)
```

### 第二步：连接IB Gateway
- 建立与IB Gateway的连接
- 验证连接状态
- 设置超时时间

### 第三步：创建交易合约
- 创建TQQQ股票合约对象
- 验证合约信息
- 确保合约可用

### 第四步：获取历史数据
- 获取30天的日线数据
- 包含开盘价、最高价、最低价、收盘价
- 用于计算技术指标

### 第五步：计算技术指标
```python
# 计算EMA20移动平均线
def calculate_ema(self, prices, period=20):
    return prices.ewm(span=period).mean()
```

### 第六步：分析交易条件
```python
# 分析是否满足交易条件
def analyze_trading_conditions(self):
    # 获取昨日数据
    yesterday_close = tqqq_data.iloc[-2]['close']  # 昨日收盘价
    yesterday_ema20 = tqqq_data.iloc[-2]['ema20']  # 昨日EMA20
    
    # 判断信号
    if yesterday_close > yesterday_ema20:
        return True, current_price  # 满足买入条件
    else:
        return False, current_price  # 不满足条件
```

### 第七步：获取账户信息
- 获取账户净资产
- 用于计算仓位大小

### 第八步：计算仓位大小
```python
# 计算买入股数
def calculate_position_size(self, percentage=0.1):
    account_value = self.get_account_value()
    available_funds = account_value * percentage  # 10%资金
    current_price = self.get_current_tqqq_price()
    quantity = int(available_funds / current_price)  # 向下取整
```

### 第九步：获取当前价格
- 获取TQQQ实时市场价格
- 如果无法获取实时价格，使用历史数据

### 第十步：执行买入订单
```python
# 下买单
def place_buy_order(self, percentage=0.1):
    quantity = self.calculate_position_size(percentage)
    order = MarketOrder('BUY', quantity)  # 市价单
    order.outsideRth = True  # 允许常规交易时间以外交易
    trade = self.ib.placeOrder(self.tqqq_contract, order)
```

### 第十一步：时间检查
```python
# 检查是否应该执行策略
def should_check_today(self):
    beijing_time = datetime.now(self.beijing_tz)
    current_time = beijing_time.time()
    target_time = datetime.strptime('21:20', '%H:%M').time()
    
    # 允许5分钟误差
    time_diff = abs((current_time.hour * 60 + current_time.minute) - 
                  (target_time.hour * 60 + target_time.minute))
    
    return time_diff <= 5
```

## 🚀 运行模式

### 单次运行模式
- **特点**: 执行一次策略后自动退出
- **适用场景**: 测试、手动执行、调试
- **启动方式**: 
  ```bash
  # 使用启动脚本选择模式1
  启动TQQQ策略.bat
  
  # 或直接运行
  python tqqq_trading.py
  ```

### 持续运行模式
- **特点**: 程序持续运行，每天21:20自动执行
- **适用场景**: 长期自动化交易
- **启动方式**:
  ```bash
  # 使用持续运行脚本
  持续运行策略.bat
  
  # 或直接运行
  python tqqq_trading.py --continuous
  ```
- **停止方式**: 按 `Ctrl+C` 安全停止程序

### Windows服务模式（推荐）
- **特点**: 系统级服务，关闭CMD窗口不影响运行
- **适用场景**: 生产环境长期运行
- **安装方式**:
  ```bash
  # 以管理员身份运行
  右键 install_service.bat → 以管理员身份运行
  ```
- **管理方式**:
  ```bash
  # 使用服务管理脚本
  服务管理.bat
  
  # 或使用系统命令
  net start TQQQStrategy    # 启动服务
  net stop TQQQStrategy     # 停止服务
  sc query TQQQStrategy     # 查看状态
  ```

## 📅 策略执行时间表

| 时间 | 操作 | 说明 |
|------|------|------|
| 每天21:20 | 自动检查 | 检查交易条件 |
| 满足条件时 | 立即买入 | 使用10%账户资金 |
| 不满足条件 | 跳过 | 等待下一天 |
| 持续模式 | 每5分钟检查一次 | 直到到达执行时间 |

## ⚠️ 重要提醒

### 风险提示
- **实盘交易**: 这是实盘交易策略，将实际扣款并执行交易
- **杠杆风险**: TQQQ是3倍杠杆ETF，波动较大
- **市场风险**: 股市有风险，投资需谨慎
- **技术风险**: 依赖网络连接和IB Gateway稳定性

### 使用前准备
1. **IB Gateway**: 确保IB Gateway已启动并监听端口4001
2. **账户资金**: 确保账户有足够资金进行交易
3. **网络连接**: 确保网络连接稳定
4. **权限设置**: 确保账户有交易TQQQ的权限

## 🔧 配置说明

### 连接参数
```python
host = '127.0.0.1'    # IB Gateway地址
port = 4001           # IB Gateway端口
client_id = 444       # 客户端ID
```

### 策略参数
```python
ema_period = 20       # EMA周期
position_percentage = 0.1  # 仓位比例 (10%)
check_time = '21:20'  # 检查时间 (北京时间)
```

## 📈 策略监控

- **策略日志**: `ib_async/tqqq_trading.log`
- **服务日志**: `ib_async/service.log`
- **错误日志**: `ib_async/service_error.log`
- **实时输出**: 控制台显示（非服务模式）
- **交易记录**: IB账户历史

## 🧪 测试功能

### 组件测试
- 连接IB Gateway测试
- 合约创建测试
- 历史数据获取测试
- EMA计算测试
- 账户信息测试
- 当前价格获取测试
- 仓位计算测试
- 时间检查测试
- 交易条件分析测试

### 运行测试
```bash
# 运行测试脚本
双击 "测试TQQQ策略.bat"

# 或手动运行
python test_strategy.py
```

## 🔄 策略优化建议

1. **参数调整**: 可以调整EMA周期和资金比例
2. **风险控制**: 可以添加止损和止盈机制
3. **信号优化**: 可以结合其他技术指标
4. **时间优化**: 可以调整检查时间频率

## 🛠️ 环境问题解决

### 常见问题

#### 问题1: Python未找到
```
❌ Python未安装或未添加到PATH
```

**解决方案**:
1. 重新安装Python，确保勾选"Add Python to PATH"
2. 运行 `环境检测.bat` 诊断问题

#### 问题2: 虚拟环境创建失败
```
❌ 虚拟环境创建失败
```

**解决方案**:
1. 确保Python版本为3.8+
2. 检查磁盘空间是否充足
3. 以管理员身份运行脚本

#### 问题3: 依赖安装失败
```
❌ 依赖安装失败
```

**解决方案**:
1. 检查网络连接
2. 尝试使用国内镜像源:
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

#### 问题4: 编码问题
```
'ho' is not recognized as an internal or external command
```

**解决方案**:
1. 使用 `启动TQQQ策略.bat` 启动
2. 确保系统支持UTF-8编码

#### 问题5: IB Gateway连接失败
```
❌ 连接失败
```

**解决方案**:
1. 确保IB Gateway已启动
2. 检查端口4001是否被占用
3. 确认防火墙设置

### 环境检测工具

#### 使用检测脚本
- `环境检测.bat`: 检测Python环境和项目配置

#### 手动检测命令
```bash
# 检测Python版本
python --version

# 检测pip
pip --version

# 检测虚拟环境
venv\Scripts\python.exe --version
```

### 部署验证

#### 1. 环境检查
```bash
# 检查Python
python --version

# 检查虚拟环境
venv\Scripts\activate
python --version

# 检查依赖
pip list
```

#### 2. 功能测试
1. 运行 `测试TQQQ策略.bat`
2. 检查输出是否正常
3. 确认没有错误信息

#### 3. 策略测试
1. 运行 `测试TQQQ策略.bat`
2. 检查各项功能是否正常
3. 确认连接IB Gateway成功
4. 测试持续运行模式：运行 `持续运行策略.bat`

## 📞 技术支持

如果遇到问题，请检查：
1. IB Gateway是否正常运行
2. 网络连接是否正常
3. 账户权限是否正确
4. Python环境和依赖是否正确安装

### 获取帮助
1. 运行 `环境检测.bat` 诊断问题
2. 查看项目日志文件
3. 运行 `测试TQQQ策略.bat` 进行功能测试

### 日志文件位置
- 策略日志: `ib_async/tqqq_trading.log`
- 系统日志: Windows事件查看器

### 联系方式
- GitHub Issues: [项目Issues页面](https://github.com/ddddogshark/IB_Trading/issues)
- 项目文档: 查看项目根目录的README.md

## 技术栈

- **Python**: 主要编程语言
- **ib_async**: IB API异步客户端（第三方库）
- **pandas**: 数据处理
- **numpy**: 数值计算
- **pytz**: 时区处理

## 📄 许可证

- **您的策略**: 基于BSD许可证开源
- **ib_async库**: 基于BSD许可证开源

## 免责声明

本项目仅供学习和研究使用。交易有风险，投资需谨慎。作者不对任何投资损失承担责任。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

---

**注意**: 
- 您的交易策略在 `ib_async/` 目录中
- 这是实盘交易策略，请确保在充分测试后再使用
- 交易有风险，投资需谨慎！
