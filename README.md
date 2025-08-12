# IB Trading Strategy - TQQQ智能交易策略

这是一个基于Interactive Brokers API的TQQQ自动化交易策略项目，使用Python和ib_async库实现。

## 项目概述

本项目包含一个智能化的TQQQ交易策略，基于以下条件进行自动化交易：
- TQQQ价格 > EMA20移动平均线
- 定时检查（北京时间21:25）

## 主要功能

### 🚀 核心特性
- **自动化交易**: 基于EMA20技术指标的智能交易决策
- **持续运行**: 支持24/7持续运行模式
- **定时检查**: 每天固定时间自动检查交易条件
- **实时监控**: 实时获取市场数据和账户信息
- **安全退出**: 支持Ctrl+C安全退出机制

### 📊 交易策略
- **买入条件**: TQQQ > EMA20
- **仓位管理**: 每次买入账户资金的10%
- **风险控制**: 自动计算股数，最小1股保护
- **订单类型**: 市价单执行

## 项目结构

```
IB_Trading/
├── ib_async/                    # ib_async库源码
│   ├── tqqq_final_trading.py   # 主要交易策略
│   └── ...
├── .gitignore                  # Git忽略文件
├── README.md                   # 项目说明（本文件）
└── requirements.txt            # 依赖包列表
```

## 安装和使用

### 环境要求
- Python 3.10+
- Interactive Brokers Gateway
- 有效的IB账户

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/IB_Trading.git
cd IB_Trading
```

2. **创建虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置IB Gateway**
- 下载并安装IB Gateway
- 启用API连接（端口4001）
- 配置账户权限

5. **运行策略**
```bash
cd ib_async
python tqqq_final_trading.py
```

## 配置说明

### IB连接配置
```python
strategy = TQQQSmartTradingStrategy(
    host='127.0.0.1',    # IB Gateway地址
    port=4001,           # IB Gateway端口
    client_id=444        # 客户端ID
)
```

### 策略参数
- **EMA周期**: 20
- **检查时间**: 北京时间21:25
- **仓位比例**: 账户资金的10%

## 安全提醒

⚠️ **重要警告**:
- 这是实盘交易策略，将实际扣款
- 请在充分测试后再使用
- 建议先使用模拟账户测试
- 请确保IB Gateway已正确配置

## 日志和监控

程序运行时会生成详细日志：
- 控制台实时输出
- `tqqq_trading.log` 文件记录
- 包含所有交易决策和结果

## 故障排除

### 常见问题
1. **连接失败**: 检查IB Gateway是否运行
2. **数据获取失败**: 检查网络连接和账户权限
3. **时区问题**: 程序自动处理夏令时

## 技术栈

- **Python**: 主要编程语言
- **ib_async**: IB API异步客户端
- **pandas**: 数据处理
- **numpy**: 数值计算
- **pytz**: 时区处理

## 许可证

本项目基于BSD许可证开源。

## 免责声明

本项目仅供学习和研究使用。交易有风险，投资需谨慎。作者不对任何投资损失承担责任。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 更新日志

### v2.0
- ✅ 实现持续运行模式
- ✅ 添加定时检查功能
- ✅ 改进日志记录
- ✅ 添加安全退出机制
- ✅ 基于EMA20的智能交易策略

---

**注意**: 使用前请仔细阅读策略说明文档 