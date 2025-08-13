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
        self.ib = IB()
        self.tqqq_contract = None
        self.ema_period = 20
        self.position_percentage = 0.1  # 10%仓位
        self.check_time = '21:20'  # 北京时间21:20
        
        logging.info(f"策略初始化完成 - 主机: {host}, 端口: {port}, 客户端ID: {client_id}")
    
    async def connect_to_ib(self):
        """连接到IB Gateway"""
        try:
            await self.ib.connect(self.host, self.port, clientId=self.client_id)
            logging.info("成功连接到IB Gateway")
            return True
        except Exception as e:
            logging.error(f"连接IB Gateway失败: {e}")
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
            bars = await self.ib.reqHistoricalData(
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
                logging.info(f"获取到 {len(df)} 条历史数据")
                return df
            else:
                logging.error("未获取到历史数据")
                return None
                
        except Exception as e:
            logging.error(f"获取历史数据失败: {e}")
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
            accounts = await self.ib.reqAccountSummary()
            total_value = 0
            
            for account in accounts:
                if account.tag == 'NetLiquidation':
                    total_value = float(account.value)
                    break
            
            logging.info(f"账户总价值: ${total_value:,.2f}")
            return total_value
            
        except Exception as e:
            logging.error(f"获取账户信息失败: {e}")
            return None
    
    async def get_current_price(self, contract):
        """获取当前价格"""
        try:
            ticker = await self.ib.reqMktData(contract)
            await asyncio.sleep(2)  # 等待数据
            
            if ticker.marketPrice():
                price = ticker.marketPrice()
                logging.info(f"TQQQ当前价格: ${price:.2f}")
                return price
            else:
                logging.error("无法获取当前价格")
                return None
                
        except Exception as e:
            logging.error(f"获取当前价格失败: {e}")
            return None
    
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
                return False
            
            # 计算EMA20
            ema20 = self.calculate_ema(historical_data['close'], self.ema_period)
            if ema20 is None:
                return False
            
            # 获取最新数据
            latest_close = historical_data.iloc[-1]['close']
            latest_ema20 = ema20.iloc[-1]
            
            logging.info(f"最新收盘价: ${latest_close:.2f}")
            logging.info(f"最新EMA20: ${latest_ema20:.2f}")
            
            # 判断买入条件
            if latest_close > latest_ema20:
                logging.info("📈 满足买入条件: 收盘价 > EMA20")
                return True
            else:
                logging.info("📉 不满足买入条件: 收盘价 < EMA20")
                return False
                
        except Exception as e:
            logging.error(f"分析交易条件失败: {e}")
            return False
    
    async def execute_trading_strategy(self):
        """执行交易策略"""
        try:
            logging.info("🚀 开始执行TQQQ智能交易策略")
            
            # 1. 连接到IB Gateway
            if not await self.connect_to_ib():
                return False
            
            # 2. 创建合约
            if not self.create_contracts():
                return False
            
            # 3. 分析交易条件
            if not await self.analyze_trading_conditions():
                logging.info("不满足交易条件，策略结束")
                return True
            
            # 4. 获取账户信息
            account_value = await self.get_account_info()
            if account_value is None:
                return False
            
            # 5. 获取当前价格
            current_price = await self.get_current_price(self.tqqq_contract)
            if current_price is None:
                return False
            
            # 6. 计算仓位
            shares = self.calculate_position_size(account_value, current_price)
            if shares == 0:
                logging.error("仓位计算为0，无法交易")
                return False
            
            # 7. 执行买入订单
            if await self.place_market_order(self.tqqq_contract, shares, 'BUY'):
                logging.info("🎉 交易策略执行成功!")
                return True
            else:
                logging.error("❌ 交易策略执行失败")
                return False
                
        except Exception as e:
            logging.error(f"执行交易策略失败: {e}")
            return False
        finally:
            # 断开连接
            if self.ib.isConnected():
                await self.ib.disconnect()
                logging.info("已断开IB连接")
    
    async def run_strategy(self, continuous_mode=False):
        """运行策略"""
        try:
            logging.info("=" * 60)
            logging.info("TQQQ智能交易策略启动")
            if continuous_mode:
                logging.info("🔄 持续运行模式已启用")
            logging.info("=" * 60)
            
            while True:
                # 检查交易时间
                if not self.check_trading_time():
                    if continuous_mode:
                        logging.info("⏰ 等待下次检查时间...")
                        # 等待5分钟后再次检查
                        await asyncio.sleep(300)  # 5分钟
                        continue
                    else:
                        logging.info("不在交易时间，策略结束")
                        return
                
                # 执行策略
                success = await self.execute_trading_strategy()
                
                if success:
                    logging.info("✅ 策略执行完成")
                else:
                    logging.error("❌ 策略执行失败")
                
                if continuous_mode:
                    logging.info("🔄 等待下次执行...")
                    # 执行完成后等待24小时
                    await asyncio.sleep(86400)  # 24小时
                else:
                    break
                    
        except KeyboardInterrupt:
            logging.info("🛑 用户中断策略运行")
        except Exception as e:
            logging.error(f"策略运行异常: {e}")

async def main():
    """主函数"""
    import sys
    
    # 检查是否启用持续运行模式
    continuous_mode = '--continuous' in sys.argv or '-c' in sys.argv
    
    strategy = TQQQSmartTradingStrategy()
    await strategy.run_strategy(continuous_mode=continuous_mode)

if __name__ == "__main__":
    asyncio.run(main()) 