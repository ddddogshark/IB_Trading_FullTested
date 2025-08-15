# TQQQ Trading Strategy 部署指南

## 📦 部署包说明

本项目已打包成独立的持续运行exe文件，可在任何Windows 10/11环境下运行，无需安装Python或任何依赖。

### 📁 部署包内容

```
TQQQ_Trading_Deployment/
├── TQQQ_Trading_Continuous.exe  # 持续运行主程序 (33.63 MB)
├── start_trading.bat            # 启动脚本 (推荐使用)
├── email_config.json            # 邮件配置文件
└── README.md                    # 使用说明
```

## 🚀 快速部署

### 1. 下载部署包
从GitHub下载最新的部署包：
```bash
git clone https://github.com/ddddogshark/IB_Trading_FullTested.git
cd IB_Trading_FullTested/dist
```

### 2. 配置邮件服务
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

### 3. 启动IB Gateway
- 启动Interactive Brokers Gateway
- 确保端口4001开放
- 登录您的IB账户

### 4. 运行程序

#### 方式一：使用启动脚本（推荐）
```bash
start_trading.bat
```

#### 方式二：直接运行exe
```bash
TQQQ_Trading_Continuous.exe
```

## 🔄 持续运行特性

### 核心功能
- **24/7持续监控**: 全天候监控市场状态
- **自动交易执行**: 在指定时间自动执行交易策略
- **邮件通知**: 实时发送交易通知和状态报告
- **错误恢复**: 自动处理连接中断和异常情况
- **日志记录**: 详细的运行日志和交易记录

### 运行模式
- **持续运行**: 程序启动后持续运行，直到手动停止
- **定时检查**: 每天在指定时间检查交易条件
- **自动重启**: 遇到错误时自动重试连接
- **优雅退出**: 支持Ctrl+C优雅停止

## ⚙️ 系统要求

### 最低要求
- **操作系统**: Windows 10/11 (64位)
- **内存**: 4GB RAM
- **存储**: 100MB 可用空间
- **网络**: 稳定的互联网连接

### 必需软件
- **Interactive Brokers Gateway**: 用于连接IB API
- **有效的IB账户**: 用于实际交易

## 🔧 配置说明

### 邮件配置 (email_config.json)

| 字段 | 说明 | 示例 |
|------|------|------|
| smtp_server | SMTP服务器地址 | smtp.gmail.com |
| smtp_port | SMTP端口 | 587 |
| sender_email | 发件人邮箱 | your-email@gmail.com |
| sender_password | 邮箱授权码 | your-app-password |
| recipient_email | 收件人邮箱 | recipient@example.com |

### 支持的邮箱服务

1. **Gmail**
   ```json
   {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587
   }
   ```

2. **QQ邮箱**
   ```json
   {
       "smtp_server": "smtp.qq.com",
       "smtp_port": 587
   }
   ```

3. **163邮箱**
   ```json
   {
       "smtp_server": "smtp.163.com",
       "smtp_port": 587
   }
   ```

4. **Outlook**
   ```json
   {
       "smtp_server": "smtp-mail.outlook.com",
       "smtp_port": 587
   }
   ```

## 📊 策略参数

### 默认配置
- **交易标的**: TQQQ (3倍杠杆纳斯达克ETF)
- **技术指标**: EMA20 (20日指数移动平均线)
- **买入条件**: 收盘价 > EMA20
- **仓位管理**: 账户总价值的10%
- **检查时间**: 10:25 (北京时间)
- **总结时间**: 10:26 (北京时间)

### 自定义配置
如需修改策略参数，请编辑源代码并重新打包：
```python
self.ema_period = 20              # EMA周期
self.position_percentage = 0.1    # 仓位百分比
self.check_time = '10:25'         # 交易检查时间
self.daily_summary_time = '10:26' # 每日总结时间
```

## 🔍 故障排除

### 常见问题

1. **程序无法启动**
   - 检查Windows Defender是否阻止了程序
   - 右键点击exe文件 → 属性 → 解除锁定
   - 以管理员身份运行

2. **连接IB Gateway失败**
   - 确保IB Gateway已启动
   - 检查端口4001开放
   - 验证账户权限

3. **邮件发送失败**
   - 检查网络连接
   - 验证邮箱配置
   - 确认授权码正确

4. **策略不执行**
   - 检查当前时间是否在交易窗口
   - 查看日志输出
   - 确认持续运行模式

### 日志文件
程序运行时会生成详细的日志信息，包括：
- 连接状态
- 交易执行
- 错误信息
- 系统状态

## 📧 邮件通知

### 通知类型
1. **交易执行通知**: 订单成功执行时
2. **每日状态报告**: 每日策略执行状态
3. **错误通知**: 系统异常或连接问题时
4. **策略中断通知**: 用户中断或系统异常时

### 邮件内容
- 交易动作（买入/卖出/持有）
- TQQQ交易数量和金额
- 当前价格和EMA20值
- 账户余额和持仓信息
- 策略执行状态

## 🔒 安全注意事项

### 账户安全
- 不要在代码中硬编码账户信息
- 定期更换API密钥
- 监控异常交易活动

### 网络安全
- 使用安全的网络连接
- 定期更新系统
- 监控网络流量

### 数据安全
- 定期备份配置和日志
- 保护敏感信息
- 使用加密传输

## 📞 技术支持

### 获取帮助
1. 查看[GitHub Issues](https://github.com/ddddogshark/IB_Trading_FullTested/issues)
2. 创建新的Issue
3. 联系维护者

### 更新日志
- **v1.0.0**: 初始版本，支持持续运行功能
- 完整的邮件通知系统
- 完善的错误处理
- 独立exe部署包
- 24/7持续监控

## ⚠️ 免责声明

本软件仅供学习和研究使用。使用本软件进行实际交易的风险由用户自行承担。作者不对任何投资损失负责。

**重要提醒**: 
- 在实盘交易前，请充分测试策略
- 了解相关风险
- 遵守当地法律法规
- 咨询专业投资顾问

---

**版本**: 1.0.0  
**最后更新**: 2025-08-15  
**维护者**: ddddogshark 