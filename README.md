# IB_Trading_FullTested

一个基于Interactive Brokers API的TQQQ智能交易策略系统，支持自动化交易、邮件通知和完整的错误处理。

## 🚀 功能特性

- **智能交易策略**: 基于EMA20移动平均线的TQQQ自动化交易
- **实时连接**: 支持IB Gateway连接，实时获取市场数据
- **账户管理**: 自动获取账户信息，智能计算仓位大小
- **邮件通知**: 完整的交易通知和错误报告系统
- **日志记录**: 详细的交易日志和系统状态记录
- **持续运行**: 支持24/7持续运行模式
- **错误处理**: 完善的异常处理和恢复机制

## 📋 系统要求

- Python 3.8+
- Interactive Brokers Gateway
- 有效的IB账户
- 网络连接

## 🛠️ 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/ddddogshark/IB_Trading_FullTested.git
cd IB_Trading_FullTested
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
```

### 3. 激活虚拟环境
**Windows:**
```bash
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

## ⚙️ 配置

### 1. 邮件配置
编辑 `email_config.json` 文件：
```json
{
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "recipient@example.com"
}
```

### 2. IB Gateway配置
- 启动IB Gateway
- 确保端口4001开放
- 配置API连接

## 🎯 使用方法

### 运行交易策略

#### 单次运行
```bash
cd ib_async
python tqqq_trading.py
```

#### 持续运行模式
```bash
cd ib_async
python tqqq_trading.py --continuous
```

### 策略参数配置

在 `tqqq_trading.py` 中可以调整以下参数：

```python
self.ema_period = 20              # EMA周期
self.position_percentage = 0.1    # 仓位百分比（10%）
self.check_time = '10:10'         # 交易检查时间
self.daily_summary_time = '10:11' # 每日总结时间
```

## 📊 策略说明

### 交易逻辑
1. **技术分析**: 计算TQQQ的20日指数移动平均线(EMA20)
2. **买入条件**: 当收盘价 > EMA20时触发买入信号
3. **仓位管理**: 使用账户总价值的10%进行交易
4. **风险控制**: 自动计算合适的股数，避免过度杠杆

### 执行流程
1. 连接到IB Gateway
2. 获取TQQQ历史数据（30天）
3. 计算EMA20指标
4. 分析交易条件
5. 获取账户信息
6. 计算仓位大小
7. 执行买入订单
8. 发送邮件通知

## 📧 邮件通知

系统会发送以下类型的邮件：

- **交易执行通知**: 订单成功执行时
- **每日状态报告**: 每日策略执行状态
- **错误通知**: 系统异常或连接问题时
- **策略中断通知**: 用户中断或系统异常时

## 📝 日志系统

### 日志文件
- `tqqq_trading.log`: 主要交易日志
- 包含详细的连接、交易、错误信息

### 日志级别
- INFO: 正常操作信息
- WARNING: 警告信息
- ERROR: 错误信息

## 🔧 故障排除

### 常见问题

1. **连接失败**
   - 检查IB Gateway是否启动
   - 确认端口4001开放
   - 验证账户权限

2. **历史数据获取失败**
   - 检查网络连接
   - 确认市场数据订阅
   - 验证合约信息

3. **邮件发送失败**
   - 检查SMTP配置
   - 确认邮箱密码正确
   - 验证网络连接

### 调试模式
启用详细日志输出：
```python
logging.getLogger().setLevel(logging.DEBUG)
```

## 📈 性能监控

### 关键指标
- 连接成功率
- 订单执行时间
- 策略命中率
- 账户收益率

### 监控建议
- 定期检查日志文件
- 监控邮件通知
- 跟踪账户余额变化
- 分析交易历史

## 🔒 安全注意事项

1. **账户安全**
   - 不要在代码中硬编码账户信息
   - 定期更换API密钥
   - 监控异常交易活动

2. **网络安全**
   - 使用安全的网络连接
   - 定期更新系统
   - 监控网络流量

3. **数据安全**
   - 定期备份配置和日志
   - 保护敏感信息
   - 使用加密传输

## 📄 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

### 贡献指南
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看[Issues](https://github.com/ddddogshark/IB_Trading_FullTested/issues)
2. 创建新的Issue
3. 联系维护者

## ⚠️ 免责声明

本软件仅供学习和研究使用。使用本软件进行实际交易的风险由用户自行承担。作者不对任何投资损失负责。

**重要提醒**: 
- 在实盘交易前，请充分测试策略
- 了解相关风险
- 遵守当地法律法规
- 咨询专业投资顾问

## 📚 相关资源

- [Interactive Brokers API文档](https://interactivebrokers.github.io/tws-api/)
- [ib_async库文档](https://github.com/ib-api-reloaded/ib_async)
- [TQQQ ETF信息](https://www.invesco.com/us/financial-products/etfs/product-detail?ticker=TQQQ)

---

**版本**: 1.0.0  
**最后更新**: 2025-08-15  
**维护者**: ddddogshark
