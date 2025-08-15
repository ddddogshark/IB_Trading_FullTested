# TQQQ交易策略配置文件指南

## 📁 配置文件说明

### 1. `trading_config.json` - 交易时间配置
```json
{
  "check_time": "11:19",
  "daily_summary_time": "11:20",
  "description": "TQQQ交易策略时间配置",
  "instructions": "修改check_time和daily_summary_time来调整交易检查时间和每日总结时间"
}
```

**配置项说明：**
- `check_time`: 每日交易检查时间（格式：HH:MM）
- `daily_summary_time`: 每日总结邮件发送时间（格式：HH:MM）

**使用示例：**
- 设置为 `"09:30"` 和 `"09:31"` - 开盘后立即检查
- 设置为 `"15:45"` 和 `"15:46"` - 收盘前检查
- 设置为 `"11:19"` 和 `"11:20"` - 中午时段检查

### 2. `email_config.json` - 邮件通知配置
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password",
  "receiver_email": "receiver@example.com"
}
```

## 🔧 如何修改配置

### 方法1：直接编辑配置文件（推荐）
1. 找到 `dist` 目录下的配置文件
2. 用文本编辑器打开 `trading_config.json`
3. 修改 `check_time` 和 `daily_summary_time` 的值
4. 保存文件
5. 重启程序（修改立即生效）

### 方法2：程序自动创建
1. 删除现有的 `trading_config.json` 文件
2. 重新运行程序
3. 程序会自动创建默认配置文件

### 方法3：使用启动脚本
1. 运行 `start_trading.bat`
2. 选择运行模式（后台/控制台）
3. 程序会自动读取外部配置文件

## ⚠️ 注意事项

1. **时间格式**：必须使用 `HH:MM` 格式（24小时制）
2. **有效时间**：建议设置在交易时间内（09:30-16:00）
3. **重启生效**：修改配置文件后需要重启程序
4. **备份配置**：建议备份重要的配置文件
5. **外部配置**：程序优先使用与exe同目录的外部配置文件
6. **后台运行**：双击exe文件可直接后台运行，关闭窗口不会停止程序

## 🚀 快速配置示例

### 开盘交易配置
```json
{
  "check_time": "09:35",
  "daily_summary_time": "09:36"
}
```

### 午盘交易配置
```json
{
  "check_time": "11:19",
  "daily_summary_time": "11:20"
}
```

### 收盘前配置
```json
{
  "check_time": "15:45",
  "daily_summary_time": "15:46"
}
```

## 🖥️ 运行模式说明

### 后台运行模式（推荐）
- **文件**: `TQQQ_Trading_Continuous.exe`
- **特点**: 无控制台窗口，双击直接后台运行
- **适用**: 长期运行，不需要查看日志
- **停止**: 使用任务管理器或运行启动脚本选择"停止进程"

### 控制台运行模式
- **文件**: `TQQQ_Trading_Continuous_Console.exe`
- **特点**: 显示控制台窗口，实时查看日志
- **适用**: 调试、监控、查看详细运行信息
- **停止**: 按 Ctrl+C 或关闭窗口

### 启动脚本模式
- **文件**: `start_trading.bat`
- **特点**: 提供选择菜单，支持多种运行模式
- **功能**: 
  - 后台运行
  - 控制台运行
  - 停止所有进程

## 📞 技术支持

如果遇到配置问题，请检查：
1. JSON格式是否正确
2. 时间格式是否为 HH:MM
3. 文件编码是否为 UTF-8
4. 程序是否有读取权限
5. 配置文件是否在exe同目录下 