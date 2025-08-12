# IB Trading Strategy - TQQQ智能交易策略

这是一个基于Interactive Brokers API的TQQQ自动化交易策略项目，使用Python和ib_async库实现。

## 项目结构

```
IB_Trading/
├── ib_async/                    # 原始ib_async库（第三方依赖）
│   ├── ib_async/               # ib_async核心库文件
│   ├── docs/                   # 库文档
│   ├── examples/               # 示例代码
│   ├── tests/                  # 测试文件
│   └── ...
├── trading_strategy/           # 🎯 您的交易策略（主要开发部分）
│   ├── tqqq_final_trading.py  # 核心交易策略
│   ├── 启动策略.bat           # Windows启动脚本
│   └── README.md              # 策略详细说明
├── .gitignore                 # Git忽略文件
├── README.md                  # 项目说明（本文件）
└── requirements.txt           # 依赖包列表
```

## 🎯 您的开发部分

### 交易策略 (`trading_strategy/`)
这是您自己开发的TQQQ智能交易策略，包含：

- **核心策略**: `tqqq_final_trading.py` - 基于EMA20的自动化交易策略
- **启动脚本**: `启动策略.bat` - Windows一键启动脚本
- **详细文档**: `README.md` - 策略使用说明

### 策略特点
- **自动化交易**: 基于EMA20技术指标的智能交易决策
- **持续运行**: 支持24/7持续运行模式
- **定时检查**: 每天北京时间21:20自动检查交易条件
- **实时监控**: 实时获取市场数据和账户信息
- **安全退出**: 支持Ctrl+C安全退出机制

## 📚 原始库部分

### ib_async库 (`ib_async/`)
这是第三方开源库，提供IB API的Python接口：

- **核心功能**: IB API的Python封装
- **文档**: 完整的API文档和示例
- **示例代码**: 各种使用示例
- **测试**: 单元测试和集成测试

## 快速开始

### 1. 查看您的策略
```bash
# 进入策略目录
cd trading_strategy

# 查看策略说明
cat README.md

# 运行策略
python tqqq_final_trading.py
```

### 2. 查看原始库
```bash
# 查看ib_async库文档
cd ib_async/docs
# 或查看示例
cd ib_async/examples
```

## 环境要求
- Python 3.10+
- Interactive Brokers Gateway
- 有效的IB账户

## 安装依赖
```bash
pip install -r requirements.txt
```

## 安全提醒

⚠️ **重要警告**:
- 这是实盘交易策略，将实际扣款
- 请在充分测试后再使用
- 建议先使用模拟账户测试
- 请确保IB Gateway已正确配置

## 技术栈

- **Python**: 主要编程语言
- **ib_async**: IB API异步客户端（第三方库）
- **pandas**: 数据处理
- **numpy**: 数值计算
- **pytz**: 时区处理

## 许可证

- **您的策略**: 基于BSD许可证开源
- **ib_async库**: 基于BSD许可证开源

## 免责声明

本项目仅供学习和研究使用。交易有风险，投资需谨慎。作者不对任何投资损失承担责任。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

---

**注意**: 
- 您的交易策略在 `trading_strategy/` 目录中
- 原始ib_async库在 `ib_async/` 目录中
- 详细使用说明请查看 `trading_strategy/README.md` 