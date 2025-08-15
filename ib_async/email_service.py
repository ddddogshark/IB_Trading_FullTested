#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立邮件服务模块
确保邮件发送不受交易策略影响，独立运行
"""

import asyncio
import logging
from datetime import datetime, timedelta
import pytz
from email_notifier import email_notifier

class EmailService:
    """独立邮件服务类"""
    
    def __init__(self):
        """初始化邮件服务"""
        self.last_email_sent_date = None
        self.daily_check_time = '21:24'  # 每日检查时间
        self.daily_summary_time = '21:25'  # 每日总结时间
        
    def should_send_daily_email(self):
        """检查是否应该发送每日邮件"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        beijing_time = datetime.now(beijing_tz)
        current_date = beijing_time.strftime('%Y-%m-%d')
        
        # 如果今天还没有发送过邮件，或者不是同一天
        if self.last_email_sent_date != current_date:
            return True
        return False
    
    def send_daily_status_email(self, trading_result=None):
        """发送每日状态邮件（独立于交易结果）"""
        try:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            beijing_time = datetime.now(beijing_tz)
            current_date = beijing_time.strftime('%Y-%m-%d')
            
            # 更新发送日期
            self.last_email_sent_date = current_date
            
            # 如果没有交易结果，创建一个默认的状态报告
            if trading_result is None:
                trading_result = {
                    'action': 'STATUS_CHECK',
                    'status': '无交易',
                    'quantity': 0,
                    'amount': 0,
                    'price': 0,
                    'current_price': 0,
                    'ema20': 0,
                    'account_balance': 0,
                    'current_position': 0,
                    'price_above_ema': False,
                    'notes': '策略正常运行，但未执行交易',
                    'connection_status': 'UNKNOWN',
                    'error_message': ''
                }
            
            # 记录交易结果信息用于调试
            logging.info(f"发送每日状态邮件，交易结果: {trading_result}")
            
            # 发送邮件通知
            email_notifier.send_trading_notification(trading_result)
            logging.info("✅ 每日状态邮件发送成功")
            
        except Exception as e:
            logging.error(f"发送每日状态邮件失败: {e}")
    
    def send_connection_failure_email(self, error_details):
        """发送连接失败邮件"""
        try:
            trading_result = {
                'action': 'CONNECTION_FAILED',
                'status': '连接失败',
                'quantity': 0,
                'amount': 0,
                'price': 0,
                'current_price': 0,
                'ema20': 0,
                'account_balance': 0,
                'current_position': 0,
                'price_above_ema': False,
                'notes': 'IB Gateway连接失败，无法执行交易策略',
                'connection_status': 'FAILED',
                'error_message': error_details
            }
            
            email_notifier.send_trading_notification(trading_result)
            logging.info("✅ 连接失败邮件发送成功")
            
        except Exception as e:
            logging.error(f"发送连接失败邮件失败: {e}")
    
    def send_strategy_error_email(self, error_details):
        """发送策略错误邮件"""
        try:
            trading_result = {
                'action': 'STRATEGY_ERROR',
                'status': '策略错误',
                'quantity': 0,
                'amount': 0,
                'price': 0,
                'current_price': 0,
                'ema20': 0,
                'account_balance': 0,
                'current_position': 0,
                'price_above_ema': False,
                'notes': '交易策略执行过程中发生错误',
                'connection_status': 'ERROR',
                'error_message': error_details
            }
            
            email_notifier.send_trading_notification(trading_result)
            logging.info("✅ 策略错误邮件发送成功")
            
        except Exception as e:
            logging.error(f"发送策略错误邮件失败: {e}")
    
    def check_daily_summary_time(self):
        """检查是否到达每日总结时间"""
        beijing_tz = pytz.timezone('Asia/Shanghai')
        beijing_time = datetime.now(beijing_tz)
        current_time = beijing_time.strftime('%H:%M')
        return current_time == self.daily_summary_time
    
    def send_daily_summary(self, trading_history=None):
        """发送每日总结"""
        try:
            if not trading_history:
                logging.info("今日无交易记录，发送空总结")
                summary_info = {
                    'total_trades': 0,
                    'buy_count': 0,
                    'sell_count': 0,
                    'hold_count': 0,
                    'total_amount': 0,
                    'total_quantity': 0,
                    'avg_price': 0,
                    'current_balance': 0,
                    'current_position': 0,
                    'position_value': 0,
                    'success_rate': 0,
                    'daily_pnl': 0,
                    'strategy_status': '正常',
                    'high_price': 0,
                    'low_price': 0,
                    'ema_trend': '未知'
                }
            else:
                # 统计交易信息
                total_trades = len(trading_history)
                buy_count = sum(1 for trade in trading_history if trade.get('action') == 'BUY')
                sell_count = sum(1 for trade in trading_history if trade.get('action') == 'SELL')
                hold_count = sum(1 for trade in trading_history if trade.get('action') == 'HOLD')
                
                total_amount = sum(trade.get('amount', 0) for trade in trading_history)
                total_quantity = sum(trade.get('quantity', 0) for trade in trading_history)
                
                summary_info = {
                    'total_trades': total_trades,
                    'buy_count': buy_count,
                    'sell_count': sell_count,
                    'hold_count': hold_count,
                    'total_amount': total_amount,
                    'total_quantity': total_quantity,
                    'avg_price': total_amount / total_quantity if total_quantity > 0 else 0,
                    'current_balance': 0,  # 需要从账户获取
                    'current_position': 0,  # 需要从账户获取
                    'position_value': 0,  # 需要从账户获取
                    'success_rate': 100.0,  # 假设成功
                    'daily_pnl': 0,  # 需要计算
                    'strategy_status': '正常',
                    'high_price': max((trade.get('price', 0) for trade in trading_history), default=0),
                    'low_price': min((trade.get('price', 0) for trade in trading_history), default=0),
                    'ema_trend': '未知'
                }
            
            email_notifier.send_daily_summary(summary_info)
            logging.info("每日总结邮件发送成功")
            
        except Exception as e:
            logging.error(f"发送每日总结失败: {e}")

# 全局邮件服务实例
email_service = EmailService() 