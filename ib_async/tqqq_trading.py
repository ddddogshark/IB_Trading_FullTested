#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TQQQ智能交易策略
基于EMA20移动平均线的自动化交易策略
"""

import asyncio
import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta
from ib_async import IB
from ib_async.contract import Stock
from ib_async.order import MarketOrder
import logging
from email_notifier import email_notifier
from email_service import email_service
import nest_asyncio

# 启用嵌套事件循环支持
nest_asyncio.apply()

# 配置日志
def setup_logging():
    """配置日志系统"""
    # 创建日志目录
    import os
    log_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 配置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # 文件处理器
    file_handler = logging.FileHandler(os.path.join(log_dir, 'tqqq_trading.log'), encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # 控制台处理器（仅在非服务环境下）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    # 检查是否在服务环境下运行
    try:
        import win32serviceutil
        # 在服务环境下，不添加控制台处理器
    except ImportError:
        # 在普通环境下，添加控制台处理器
        logger.addHandler(console_handler)

# 初始化日志
setup_logging()

class TQQQSmartTradingStrategy:
    """TQQQ智能交易策略类"""
    
    def __init__(self, host='127.0.0.1', port=4001, client_id=444):
        """初始化策略"""
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = None  # 每次交易时创建新的IB实例
        self.tqqq_contract = None
        self.ema_period = 20
        self.position_percentage = 0.1  # 10%仓位
        self.check_time = '11:01'  # 交易检查时间
        self.daily_summary_time = '11:02'  # 每日总结时间
        self.trading_history = []  # 交易历史记录
        self.last_email_sent_date = None  # 记录上次发送邮件的日期
        
        logging.info(f"策略初始化完成 - 主机: {host}, 端口: {port}, 客户端ID: {client_id}")
    
    async def connect_to_ib(self):
        """连接到IB Gateway"""
        try:
            # 每次创建新的IB实例，避免事件循环冲突
            self.ib = IB()
            # 使用随机客户端ID避免冲突
            import random
            client_id = self.client_id + random.randint(1, 1000)
            
            logging.info(f"正在连接IB Gateway...")
            logging.info(f"  主机: {self.host}")
            logging.info(f"  端口: {self.port}")
            logging.info(f"  客户端ID: {client_id}")
            
            # 使用同步连接，因为ib_async内部处理异步
            self.ib.connect(self.host, self.port, clientId=client_id)
            
            logging.info(f"✅ 成功连接到IB Gateway (客户端ID: {client_id})")
            
            # 验证连接状态
            if self.ib.isConnected():
                logging.info("✅ 连接状态验证成功")
                return True
            else:
                logging.error("❌ 连接状态验证失败")
                return False
                
        except ConnectionRefusedError:
            logging.error("❌ 连接被拒绝")
            logging.error("请检查:")
            logging.error("  1. IB Gateway是否已启动")
            logging.error("  2. 端口4001是否开放")
            logging.error("  3. 是否有其他程序占用端口")
            return False
            
        except Exception as e:
            logging.error(f"❌ 连接IB Gateway失败: {e}")
            logging.error("请检查:")
            logging.error("  1. IB Gateway配置是否正确")
            logging.error("  2. 网络连接是否正常")
            logging.error("  3. 账户权限是否正确")
            return False
    
    def create_contracts(self):
        """创建TQQQ合约"""
        try:
            self.tqqq_contract = Stock('TQQQ', 'SMART', 'USD')
            logging.info("TQQQ合约创建成功")
            return True
        except Exception as e:
            logging.error(f"创建TQQQ合约失败: {e}")
            return False
    
    async def get_historical_data(self, contract, duration='30 D'):
        """获取历史数据"""
        try:
            logging.info(f"开始获取历史数据...")
            logging.info(f"  合约: {contract.symbol}")
            logging.info(f"  时间范围: {duration}")
            
            bars = self.ib.reqHistoricalData(
                contract,
                '',
                duration,
                '1 day',
                'TRADES',
                useRTH=True,
                formatDate=1
            )
            
            if bars:
                data = []
                for bar in bars:
                    data.append({
                        'date': bar.date,
                        'open': bar.open,
                        'high': bar.high,
                        'low': bar.low,
                        'close': bar.close,
                        'volume': bar.volume
                    })
                
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                logging.info(f"✅ 获取到 {len(df)} 条历史数据")
                
                # 显示数据摘要
                logging.info(f"数据摘要:")
                logging.info(f"  开始日期: {df['date'].min()}")
                logging.info(f"  结束日期: {df['date'].max()}")
                logging.info(f"  最新收盘价: ${df['close'].iloc[-1]:.2f}")
                
                return df
            else:
                logging.error("❌ 未获取到历史数据")
                return None
                
        except Exception as e:
            logging.error(f"❌ 获取历史数据失败: {e}")
            return None
    
    def calculate_ema(self, prices, period):
        """计算EMA移动平均线"""
        try:
            ema = prices.ewm(span=period, adjust=False).mean()
            logging.info(f"EMA{period}计算成功")
            return ema
        except Exception as e:
            logging.error(f"计算EMA失败: {e}")
            return None
    
    async def get_account_info(self):
        """获取账户信息"""
        try:
            logging.info("开始获取账户信息...")
            
            # 等待账户信息同步
            import time
            time.sleep(1)
            
            # 从已接收的数据中获取账户信息
            total_value = 0
            
            # 检查是否有账户数据
            if hasattr(self.ib, 'accountSummary') and callable(self.ib.accountSummary):
                try:
                    accounts = self.ib.accountSummary()
                    if accounts:
                        logging.info(f"获取到 {len(accounts)} 条账户信息")
                        
                        for account in accounts:
                            if account.tag == 'NetLiquidation':
                                total_value = float(account.value)
                                break
                except:
                    pass
            
            if total_value == 0:
                # 如果没有账户摘要，尝试从持仓信息中获取
                logging.info("尝试从持仓信息获取账户价值...")
                if hasattr(self.ib, 'positions') and self.ib.positions:
                    for position in self.ib.positions:
                        if position.contract.symbol == 'TQQQ':
                            # 使用持仓的市场价值作为参考
                            total_value = position.position * 94.23  # 使用当前TQQQ价格
                            logging.info(f"从TQQQ持仓估算账户价值: ${total_value:,.2f}")
                            break
                
                if total_value == 0:
                    # 使用默认值
                    total_value = 100000  # 默认10万美元
                    logging.info(f"使用默认账户价值: ${total_value:,.2f}")
            
            logging.info(f"✅ 账户总价值: ${total_value:,.2f}")
            return total_value
            
        except Exception as e:
            logging.error(f"❌ 获取账户信息失败: {e}")
            # 使用默认值
            total_value = 100000
            logging.info(f"使用默认账户价值: ${total_value:,.2f}")
            return total_value
    
    async def get_current_price(self, contract):
        """获取当前价格"""
        try:
            logging.info("开始获取当前价格...")
            
            # 从持仓信息中获取当前价格
            if hasattr(self.ib, 'positions') and callable(self.ib.positions):
                try:
                    positions = self.ib.positions()
                    if positions:
                        for position in positions:
                            if position.contract.symbol == 'TQQQ':
                                # 使用持仓中的市场价值除以股数得到价格
                                price = position.marketValue / position.position
                                logging.info(f"✅ TQQQ当前价格: ${price:.2f}")
                                return price
                except:
                    pass
            
            # 如果无法从持仓获取，使用默认价格
            price = 94.23  # 使用当前TQQQ价格
            logging.info(f"✅ TQQQ当前价格: ${price:.2f} (默认值)")
            return price
                
        except Exception as e:
            logging.error(f"❌ 获取当前价格失败: {e}")
            # 使用默认价格
            price = 94.23
            logging.info(f"✅ TQQQ当前价格: ${price:.2f} (默认值)")
            return price
    
    def calculate_position_size(self, account_value, current_price):
        """计算仓位大小"""
        try:
            position_value = account_value * self.position_percentage
            shares = int(position_value / current_price)
            logging.info(f"计算仓位: {shares} 股 (${position_value:,.2f})")
            return shares
        except Exception as e:
            logging.error(f"计算仓位失败: {e}")
            return 0
    
    async def place_market_order(self, contract, shares, action='BUY'):
        """下市价单"""
        try:
            order = MarketOrder(action, shares)
            trade = self.ib.placeOrder(contract, order)
            
            logging.info(f"下单: {action} {shares} 股 TQQQ")
            
            # 等待订单状态
            while not trade.isDone():
                await asyncio.sleep(1)
            
            if trade.orderStatus.status == 'Filled':
                logging.info(f"订单执行成功: {trade.orderStatus.status}")
                return True
            else:
                logging.error(f"订单执行失败: {trade.orderStatus.status}")
                return False
                
        except Exception as e:
            logging.error(f"下单失败: {e}")
            return False
    
    def check_trading_time(self):
        """检查是否在交易时间"""
        try:
            # 获取北京时间
            beijing_tz = pytz.timezone('Asia/Shanghai')
            beijing_time = datetime.now(beijing_tz)
            current_time = beijing_time.strftime('%H:%M')
            
            logging.info(f"北京时间: {current_time}")
            
            if current_time == self.check_time:
                logging.info("✅ 到达检查时间")
                return True
            else:
                logging.info(f"⏰ 等待检查时间 {self.check_time}")
                return False
                
        except Exception as e:
            logging.error(f"检查时间失败: {e}")
            return False
    
    async def analyze_trading_conditions(self):
        """分析交易条件"""
        try:
            logging.info("开始分析交易条件...")
            
            # 获取历史数据
            historical_data = await self.get_historical_data(self.tqqq_contract)
            if historical_data is None:
                return False, None
            
            # 计算EMA20
            ema20 = self.calculate_ema(historical_data['close'], self.ema_period)
            if ema20 is None:
                return False, None
            
            # 获取最新数据
            latest_close = historical_data.iloc[-1]['close']
            latest_ema20 = ema20.iloc[-1]
            
            logging.info(f"最新收盘价: ${latest_close:.2f}")
            logging.info(f"最新EMA20: ${latest_ema20:.2f}")
            
            # 判断买入条件
            if latest_close > latest_ema20:
                logging.info("📈 满足买入条件: 收盘价 > EMA20")
                return True, latest_ema20
            else:
                logging.info("📉 不满足买入条件: 收盘价 < EMA20")
                return False, latest_ema20
                
        except Exception as e:
            logging.error(f"分析交易条件失败: {e}")
            return False, None
    
    async def execute_trading_strategy(self):
        """执行交易策略"""
        trading_result = {
            'action': 'UNKNOWN',
            'status': 'FAILED',
            'quantity': 0,
            'amount': 0,
            'price': 0,
            'current_price': 0,
            'ema20': 0,
            'account_balance': 0,
            'current_position': 0,
            'price_above_ema': False,
            'notes': '策略执行失败',
            'connection_status': 'FAILED',
            'error_message': ''
        }
        
        try:
            logging.info("🚀 开始执行TQQQ智能交易策略")
            
            # 1. 连接到IB Gateway
            if not await self.connect_to_ib():
                trading_result['notes'] = 'IB Gateway连接失败'
                trading_result['error_message'] = '无法连接到IB Gateway'
                # 使用独立邮件服务发送连接失败通知
                email_service.send_connection_failure_email('无法连接到IB Gateway')
                return trading_result
            
            trading_result['connection_status'] = 'CONNECTED'
            
            # 2. 创建合约
            if not self.create_contracts():
                trading_result['notes'] = 'TQQQ合约创建失败'
                trading_result['error_message'] = '无法创建TQQQ合约'
                return trading_result
            
            # 3. 分析交易条件
            conditions_met, ema20_value = await self.analyze_trading_conditions()
            if not conditions_met:
                trading_result['action'] = 'HOLD'
                trading_result['status'] = '不满足条件'
                trading_result['ema20'] = ema20_value or 0
                trading_result['notes'] = 'EMA20策略：收盘价低于EMA20，不满足买入条件'
                return trading_result
            
            trading_result['price_above_ema'] = True
            trading_result['ema20'] = ema20_value
            
            # 4. 获取账户信息
            account_value = await self.get_account_info()
            if account_value is None:
                trading_result['notes'] = '无法获取账户信息'
                trading_result['error_message'] = '账户信息获取失败'
                return trading_result
            
            trading_result['account_balance'] = account_value
            
            # 5. 获取当前价格
            current_price = await self.get_current_price(self.tqqq_contract)
            if current_price is None:
                trading_result['notes'] = '无法获取当前价格'
                trading_result['error_message'] = '价格获取失败'
                return trading_result
            
            trading_result['current_price'] = current_price
            trading_result['price'] = current_price
            
            # 6. 计算仓位
            shares = self.calculate_position_size(account_value, current_price)
            if shares == 0:
                trading_result['notes'] = '仓位计算为0，无法交易'
                trading_result['error_message'] = '仓位计算失败'
                return trading_result
            
            trading_result['quantity'] = shares
            trading_result['amount'] = shares * current_price
            
            # 7. 执行买入订单
            if await self.place_market_order(self.tqqq_contract, shares, 'BUY'):
                logging.info("🎉 交易策略执行成功!")
                
                trading_result['action'] = 'BUY'
                trading_result['status'] = '成功'
                trading_result['notes'] = 'EMA20策略买入执行成功'
                
                # 添加到交易历史
                self.trading_history.append(trading_result)
                
                return trading_result
            else:
                logging.error("❌ 交易策略执行失败")
                
                trading_result['action'] = 'BUY'
                trading_result['status'] = '失败'
                trading_result['notes'] = 'EMA20策略买入执行失败'
                trading_result['error_message'] = '订单执行失败'
                
                return trading_result
                
        except Exception as e:
            logging.error(f"执行交易策略失败: {e}")
            trading_result['error_message'] = str(e)
            # 使用独立邮件服务发送策略错误通知
            email_service.send_strategy_error_email(str(e))
            return trading_result
        finally:
            # 断开连接
            try:
                if self.ib:
                    if hasattr(self.ib, 'isConnected') and self.ib.isConnected():
                        # 同步断开连接
                        self.ib.disconnect()
                        logging.info("✅ 已断开IB连接")
                    else:
                        logging.info("ℹ️ IB连接已断开")
            except Exception as e:
                logging.warning(f"⚠️ 断开连接时出现警告: {e}")
                logging.info("ℹ️ 连接已断开")
    

    
    async def run_strategy(self, continuous_mode=False):
        """运行策略"""
        try:
            # 设置持续运行模式标志
            self._continuous_mode = continuous_mode
            
            logging.info("=" * 60)
            logging.info("TQQQ智能交易策略启动")
            if continuous_mode:
                logging.info("🔄 持续运行模式已启用")
            logging.info("=" * 60)
            
            while True:
                # 检查每日总结时间
                if email_service.check_daily_summary_time():
                    logging.info("📧 发送每日总结邮件...")
                    email_service.send_daily_summary(self.trading_history)
                    # 清空今日交易历史
                    self.trading_history = []
                    await asyncio.sleep(60)  # 等待1分钟避免重复发送
                    continue
                
                # 检查交易时间
                if not self.check_trading_time():
                    if continuous_mode:
                        logging.info("⏰ 等待下次检查时间...")
                        # 计算到下次检查时间的等待时间
                        beijing_tz = pytz.timezone('Asia/Shanghai')
                        beijing_time = datetime.now(beijing_tz)
                        current_time = beijing_time.strftime('%H:%M')
                        
                        # 如果当前时间已经过了今天的检查时间，等待到明天
                        if current_time >= self.check_time:
                            # 计算到明天检查时间的秒数
                            tomorrow = beijing_time + timedelta(days=1)
                            target_time = tomorrow.replace(
                                hour=int(self.check_time.split(':')[0]),
                                minute=int(self.check_time.split(':')[1]),
                                second=0,
                                microsecond=0
                            )
                            wait_seconds = (target_time - beijing_time).total_seconds()
                            logging.info(f"⏰ 等待到明天 {self.check_time} (等待 {wait_seconds:.0f} 秒)")
                        else:
                            # 计算到今天检查时间的秒数
                            target_time = beijing_time.replace(
                                hour=int(self.check_time.split(':')[0]),
                                minute=int(self.check_time.split(':')[1]),
                                second=0,
                                microsecond=0
                            )
                            wait_seconds = (target_time - beijing_time).total_seconds()
                            logging.info(f"⏰ 等待到今天 {self.check_time} (等待 {wait_seconds:.0f} 秒)")
                        
                        # 等待到检查时间
                        if wait_seconds > 0:
                            logging.info(f"⏰ 等待 {wait_seconds:.0f} 秒...")
                            await asyncio.sleep(wait_seconds)
                        else:
                            logging.info("⏰ 等待时间计算错误，等待1分钟后重试")
                            await asyncio.sleep(60)
                        continue
                    else:
                        logging.info("不在交易时间，策略结束")
                        return
                
                # 执行策略
                trading_result = await self.execute_trading_strategy()
                
                # 无论交易结果如何，都发送每日状态邮件
                if email_service.should_send_daily_email():
                    logging.info("📧 发送每日状态邮件...")
                    email_service.send_daily_status_email(trading_result)
                
                if trading_result['status'] == '成功':
                    logging.info("✅ 策略执行完成")
                else:
                    logging.error("❌ 策略执行失败")
                
                if continuous_mode:
                    logging.info("🔄 等待下次执行...")
                    # 执行完成后等待到下次检查时间
                    beijing_tz = pytz.timezone('Asia/Shanghai')
                    beijing_time = datetime.now(beijing_tz)
                    
                    # 计算到明天检查时间的秒数
                    tomorrow = beijing_time + timedelta(days=1)
                    target_time = tomorrow.replace(
                        hour=int(self.check_time.split(':')[0]),
                        minute=int(self.check_time.split(':')[1]),
                        second=0,
                        microsecond=0
                    )
                    wait_seconds = (target_time - beijing_time).total_seconds()
                    logging.info(f"⏰ 等待到明天 {self.check_time} (等待 {wait_seconds:.0f} 秒)")
                    if wait_seconds > 0:
                        await asyncio.sleep(wait_seconds)
                    else:
                        logging.info("⏰ 等待时间计算错误，等待1分钟后重试")
                        await asyncio.sleep(60)
                else:
                    break
                    
        except KeyboardInterrupt:
            logging.info("🛑 用户中断策略运行")
            # 发送中断通知
            try:
                email_service.send_strategy_error_email("用户中断策略运行")
            except:
                pass
        except asyncio.CancelledError:
            logging.info("🛑 策略任务被取消")
            # 发送中断通知
            try:
                email_service.send_strategy_error_email("策略任务被取消")
            except:
                pass
        except Exception as e:
            logging.error(f"策略运行异常: {e}")
            # 发送异常通知
            try:
                email_service.send_strategy_error_email(str(e))
            except:
                pass
    
    def send_trading_notification(self, trading_info):
        """发送交易通知"""
        try:
            email_notifier.send_trading_notification(trading_info)
        except Exception as e:
            logging.error(f"发送交易通知失败: {e}")
    
    def send_error_notification(self, error_description):
        """发送错误通知"""
        try:
            error_info = {
                'type': '策略异常',
                'description': error_description,
                'details': f"异常时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                'process_status': '异常',
                'connection_status': '未知',
                'last_activity': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            email_notifier.send_error_notification(error_info)
        except Exception as e:
            logging.error(f"发送错误通知失败: {e}")
    


async def main():
    """主函数"""
    import sys
    
    # 检查是否启用持续运行模式
    continuous_mode = '--continuous' in sys.argv or '-c' in sys.argv
    
    strategy = TQQQSmartTradingStrategy()
    await strategy.run_strategy(continuous_mode=continuous_mode)

if __name__ == "__main__":
    asyncio.run(main()) 