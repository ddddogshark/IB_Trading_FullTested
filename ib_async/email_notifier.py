#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件通知模块
支持163邮箱发送交易策略通知
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self, config_file='email_config.json'):
        """初始化邮件通知器"""
        # 获取当前文件所在目录
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(current_dir, config_file)
        self.config = self.load_config()
        self.sender_email = 'a36602476@163.com'
        self.receiver_email = 'a36602476@163.com'
        
    def load_config(self):
        """加载邮件配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 创建默认配置文件
                default_config = {
                    "smtp_server": "smtp.163.com",
                    "smtp_port": 587,
                    "sender_email": "a36602476@163.com",
                    "receiver_email": "a36602476@163.com",
                    "password": "lzw.36602476"
                }
                self.save_config(default_config)
                logging.warning(f"已创建默认配置文件: {self.config_file}")
                logging.warning("请在配置文件中设置正确的邮箱密码")
                return default_config
        except Exception as e:
            logging.error(f"加载邮件配置失败: {e}")
            return {}
    
    def save_config(self, config):
        """保存邮件配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"保存邮件配置失败: {e}")
    
    def send_email(self, subject, content):
        """发送邮件"""
        try:
            if not self.config.get('password') or self.config['password'] == "请在此处配置您的邮箱密码":
                logging.error("邮箱密码未配置，无法发送邮件")
                return False
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            msg['Subject'] = subject
            
            # 添加邮件内容
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # 连接SMTP服务器
            try:
                # 尝试SSL连接
                server = smtplib.SMTP_SSL(self.config['smtp_server'], 465)
            except:
                # 如果SSL失败，尝试普通连接
                server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
                server.starttls()
            
            # 登录
            server.login(self.sender_email, self.config['password'])
            
            # 发送邮件
            text = msg.as_string()
            server.sendmail(self.sender_email, self.receiver_email, text)
            server.quit()
            
            logging.info(f"邮件发送成功: {subject}")
            return True
            
        except Exception as e:
            logging.error(f"邮件发送失败: {e}")
            return False
    
    def send_trading_notification(self, trading_info):
        """发送交易通知"""
        subject = f"TQQQ策略交易通知 - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = f"""
TQQQ智能交易策略 - 每日交易报告
========================================
报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

交易详情:
----------------------------------------
策略动作: {trading_info.get('action', '未知')}
交易状态: {trading_info.get('status', '未知')}

交易信息:
- TQQQ交易数量: {trading_info.get('quantity', 0)} 股
- 交易金额: ${trading_info.get('amount', 0):.2f}
- 交易价格: ${trading_info.get('price', 0):.2f}

市场信息:
- 当前价格: ${trading_info.get('current_price', 0):.2f}
- EMA20: ${trading_info.get('ema20', 0):.2f}
- 账户余额: ${trading_info.get('account_balance', 0):.2f}

策略逻辑:
- 收盘价 > EMA20: {'是' if trading_info.get('price_above_ema', False) else '否'}
- 当前持仓: {trading_info.get('current_position', 0)} 股

备注:
{trading_info.get('notes', '无')}
========================================
        """
        
        return self.send_email(subject, content)
    
    def send_error_notification(self, error_info):
        """发送错误通知"""
        subject = f"TQQQ策略异常通知 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        content = f"""
TQQQ智能交易策略 - 异常报告
========================================
异常时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

异常类型: {error_info.get('type', '未知')}
异常描述: {error_info.get('description', '无描述')}

详细信息:
{error_info.get('details', '无详细信息')}

系统状态:
- 进程状态: {error_info.get('process_status', '未知')}
- 连接状态: {error_info.get('connection_status', '未知')}
- 最后活动: {error_info.get('last_activity', '未知')}

建议操作:
1. 检查IB Gateway是否正常运行
2. 检查网络连接
3. 查看详细日志文件
4. 重启策略服务

========================================
        """
        
        return self.send_email(subject, content)
    
    def send_daily_summary(self, summary_info):
        """发送每日总结"""
        subject = f"TQQQ策略每日总结 - {datetime.now().strftime('%Y-%m-%d')}"
        
        content = f"""
TQQQ智能交易策略 - 每日总结报告
========================================
报告日期: {datetime.now().strftime('%Y-%m-%d')}
生成时间: {datetime.now().strftime('%H:%M:%S')}

今日交易汇总:
----------------------------------------
总交易次数: {summary_info.get('total_trades', 0)}
买入次数: {summary_info.get('buy_count', 0)}
卖出次数: {summary_info.get('sell_count', 0)}
持有次数: {summary_info.get('hold_count', 0)}

交易详情:
- 总交易金额: ${summary_info.get('total_amount', 0):.2f}
- 总交易数量: {summary_info.get('total_quantity', 0)} 股
- 平均交易价格: ${summary_info.get('avg_price', 0):.2f}

账户状态:
- 当前余额: ${summary_info.get('current_balance', 0):.2f}
- 当前持仓: {summary_info.get('current_position', 0)} 股
- 持仓市值: ${summary_info.get('position_value', 0):.2f}

策略表现:
- 策略执行成功率: {summary_info.get('success_rate', 0):.1f}%
- 今日盈亏: ${summary_info.get('daily_pnl', 0):.2f}
- 策略状态: {summary_info.get('strategy_status', '正常')}

市场分析:
- 今日最高价: ${summary_info.get('high_price', 0):.2f}
- 今日最低价: ${summary_info.get('low_price', 0):.2f}
- EMA20趋势: {summary_info.get('ema_trend', '未知')}

========================================
        """
        
        return self.send_email(subject, content)

# 全局邮件通知器实例
email_notifier = EmailNotifier() 