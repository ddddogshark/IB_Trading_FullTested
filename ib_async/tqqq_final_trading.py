#!/usr/bin/env python3
"""
TQQQ智能交易策略
基于EMA20信号的自动化交易策略
支持持续运行和定时检查
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ib_async import *
import logging
import time
import pytz
import threading
import signal
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tqqq_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TQQQSmartTradingStrategy:
    """TQQQ智能交易策略类"""
    
    def __init__(self, host='127.0.0.1', port=4001, client_id=444):
        """初始化交易策略"""
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = None
        self.tqqq_contract = None
        self.running = True
        self.last_trade_date = None
        
        # 设置时区
        self.beijing_tz = pytz.timezone('Asia/Shanghai')
        
        # 信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """处理退出信号"""
        logger.info("收到退出信号，正在关闭...")
        self.running = False
        if self.ib and self.ib.isConnected():
            self.ib.disconnect()
        sys.exit(0)
        
    def connect_to_ib(self):
        """连接到IB Gateway"""
        try:
            if self.ib and self.ib.isConnected():
                return True
                
            self.ib = IB()
            logger.info(f"正在连接到 {self.host}:{self.port}")
            self.ib.connect(self.host, self.port, clientId=self.client_id, timeout=20)
            logger.info("✅ 连接成功!")
            return True
        except Exception as e:
            logger.error(f"❌ 连接失败: {e}")
            return False
    
    def create_contracts(self):
        """创建TQQQ合约"""
        try:
            # 创建TQQQ股票合约
            self.tqqq_contract = Stock('TQQQ', 'SMART', 'USD')
            
            # 验证合约
            tqqq_contracts = self.ib.qualifyContracts(self.tqqq_contract)
            
            if tqqq_contracts:
                self.tqqq_contract = tqqq_contracts[0]
                logger.info(f"✅ TQQQ合约创建成功: {self.tqqq_contract}")
                return True
            else:
                logger.error("❌ 无法验证合约")
                return False
        except Exception as e:
            logger.error(f"❌ 创建合约失败: {e}")
            return False
    
    def get_historical_data(self, contract, duration='1 D', bar_size='1 day'):
        """获取历史数据"""
        try:
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow='TRADES',
                useRTH=True,
                formatDate=1
            )
            
            if bars:
                df = util.df(bars)
                return df
            else:
                logger.error(f"❌ 无法获取 {contract.symbol} 历史数据")
                return None
                
        except Exception as e:
            logger.error(f"❌ 获取历史数据失败: {e}")
            return None
    
    def calculate_ema(self, prices, period=20):
        """计算EMA"""
        try:
            return prices.ewm(span=period).mean()
        except Exception as e:
            logger.error(f"❌ 计算EMA失败: {e}")
            return None
    

    
    def analyze_trading_conditions(self):
        """分析交易条件"""
        try:
            logger.info("🔍 开始分析交易条件...")
            
            # 1. 获取TQQQ历史数据
            tqqq_data = self.get_historical_data(self.tqqq_contract, duration='30 D')
            if tqqq_data is None or len(tqqq_data) < 20:
                logger.error("❌ 无法获取足够的TQQQ数据")
                return False, None
            
            # 2. 计算EMA20
            tqqq_data['ema20'] = self.calculate_ema(tqqq_data['close'], 20)
            
            # 3. 获取昨日数据
            yesterday_close = tqqq_data.iloc[-2]['close']  # 昨日收盘价
            yesterday_ema20 = tqqq_data.iloc[-2]['ema20']  # 昨日EMA20
            current_price = tqqq_data.iloc[-1]['close']    # 当前价格
            
            logger.info("📊 TQQQ数据分析:")
            logger.info(f"   昨日收盘价: ${yesterday_close:.2f}")
            logger.info(f"   昨日EMA20: ${yesterday_ema20:.2f}")
            logger.info(f"   当前价格: ${current_price:.2f}")
            
            # 4. 检查EMA20信号
            if yesterday_close > yesterday_ema20:
                logger.info("✅ 昨日收盘价在EMA20以上，满足买入条件")
                return True, current_price
            else:
                logger.info("❌ 昨日收盘价在EMA20以下，不满足买入条件")
                return False, current_price
                
        except Exception as e:
            logger.error(f"❌ 分析交易条件失败: {e}")
            return False, None
    
    def get_account_value(self):
        """获取账户总价值"""
        try:
            # 获取账户信息
            account_values = self.ib.accountSummary()
            
            # 查找总账户价值
            total_value = 0
            for value in account_values:
                if value.tag == 'NetLiquidation' and value.currency == 'USD':
                    total_value = float(value.value)
                    break
            
            logger.info(f"💰 账户总价值: ${total_value:,.2f}")
            return total_value
            
        except Exception as e:
            logger.error(f"❌ 获取账户价值失败: {e}")
            return 0
    
    def calculate_position_size(self, percentage=0.1):
        """计算基于账户资金百分比的仓位大小"""
        try:
            # 获取账户总价值
            account_value = self.get_account_value()
            
            if account_value <= 0:
                logger.error("❌ 无法获取有效的账户价值")
                return 0
            
            # 获取当前TQQQ价格
            current_price = self.get_current_tqqq_price()
            
            if current_price <= 0:
                logger.error("❌ 无法获取有效的TQQQ价格")
                return 0
            
            # 计算可用资金
            available_funds = account_value * percentage
            
            # 计算可买入股数（向下取整）
            quantity = int(available_funds / current_price)
            
            # 确保至少买入1股
            if quantity < 1:
                quantity = 1
                logger.warning(f"⚠️ 计算股数小于1，调整为1股")
            
            # 计算实际使用资金
            actual_funds = quantity * current_price
            
            logger.info(f"📊 仓位计算:")
            logger.info(f"   账户总价值: ${account_value:,.2f}")
            logger.info(f"   使用比例: {percentage*100}%")
            logger.info(f"   可用资金: ${available_funds:,.2f}")
            logger.info(f"   当前TQQQ价格: ${current_price:.2f}")
            logger.info(f"   计算股数: {quantity}股")
            logger.info(f"   实际使用资金: ${actual_funds:,.2f}")
            
            return quantity
            
        except Exception as e:
            logger.error(f"❌ 计算仓位大小失败: {e}")
            return 1  # 出错时返回1股作为默认值
    
    def get_current_tqqq_price(self):
        """获取当前TQQQ价格"""
        try:
            # 获取TQQQ实时价格
            ticker = self.ib.reqMktData(self.tqqq_contract)
            
            # 等待价格数据
            max_wait = 10
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                time.sleep(0.5)
                if ticker.marketPrice() > 0:
                    price = ticker.marketPrice()
                    logger.info(f"📈 当前TQQQ价格: ${price:.2f}")
                    return price
                elif ticker.last > 0:
                    price = ticker.last
                    logger.info(f"📈 当前TQQQ价格(最后成交): ${price:.2f}")
                    return price
            
            # 如果无法获取实时价格，使用历史数据的最新价格
            logger.warning("⚠️ 无法获取实时价格，使用历史数据")
            tqqq_data = self.get_historical_data(self.tqqq_contract, duration='1 D')
            if tqqq_data is not None and len(tqqq_data) > 0:
                price = tqqq_data.iloc[-1]['close']
                logger.info(f"📈 使用历史价格: ${price:.2f}")
                return price
            
            logger.error("❌ 无法获取TQQQ价格")
            return 0
            
        except Exception as e:
            logger.error(f"❌ 获取TQQQ价格失败: {e}")
            return 0
    
    def place_buy_order(self, percentage=0.1):
        """基于账户资金百分比下买单"""
        try:
            # 计算仓位大小
            quantity = self.calculate_position_size(percentage)
            
            if quantity <= 0:
                logger.error("❌ 计算仓位失败，取消交易")
                return False
            
            # 创建市价单
            order = MarketOrder('BUY', quantity)
            
            # 设置常规交易时间以外
            order.outsideRth = True
            
            # 获取当前价格用于显示
            current_price = self.get_current_tqqq_price()
            estimated_cost = quantity * current_price if current_price > 0 else 0
            
            logger.info(f"💰 正在下买单: {quantity}股TQQQ")
            logger.info(f"   使用账户资金: {percentage*100}%")
            logger.info(f"   预估成本: ${estimated_cost:,.2f}")
            logger.info(f"   订单类型: 市价单")
            logger.info(f"   交易时间: 常规交易时间以外")
            logger.warning("⚠️ 这是实盘交易，将实际扣款!")
            
            # 下单
            trade = self.ib.placeOrder(self.tqqq_contract, order)
            
            # 等待订单状态
            max_wait = 60
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                time.sleep(1)
                status = trade.orderStatus.status
                logger.info(f"订单状态: {status}")
                
                if status == 'Filled':
                    actual_cost = quantity * trade.orderStatus.avgFillPrice
                    logger.info(f"🎉 买单成功执行: {quantity}股TQQQ")
                    logger.info(f"成交价格: ${trade.orderStatus.avgFillPrice:.2f}")
                    logger.info(f"实际成本: ${actual_cost:,.2f}")
                    return True
                elif status in ['Cancelled', 'Inactive']:
                    logger.error(f"❌ 订单被取消或失效: {status}")
                    return False
                elif status in ['PendingSubmit', 'Submitted', 'PreSubmitted', 'ApiPending']:
                    logger.info("订单处理中...")
                elif status == 'ApiCancelled':
                    logger.error("API取消...")
                    return False
            
            logger.warning(f"⚠️ 订单超时，状态: {trade.orderStatus.status}")
            return False
                
        except Exception as e:
            logger.error(f"❌ 下买单失败: {e}")
            return False
    
    def should_check_today(self):
        """检查今天是否应该执行策略"""
        try:
            # 获取北京时间
            beijing_time = datetime.now(self.beijing_tz)
            today = beijing_time.date()
            
            # 如果今天已经交易过，跳过
            if self.last_trade_date == today:
                logger.info(f"📅 今天 ({today}) 已经检查过，跳过")
                return False
            
            # 检查是否是北京时间21:20
            current_time = beijing_time.time()
            target_time = datetime.strptime('21:20', '%H:%M').time()
            
            # 允许5分钟的误差
            time_diff = abs((current_time.hour * 60 + current_time.minute) - 
                          (target_time.hour * 60 + target_time.minute))
            
            if time_diff <= 5:
                logger.info(f"⏰ 当前北京时间: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"🎯 接近检查时间 (21:20)，开始检查策略条件")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"❌ 检查时间条件失败: {e}")
            return False
    
    def execute_daily_strategy(self):
        """执行每日策略"""
        try:
            logger.info("🚀 开始执行每日策略检查...")
            logger.info("=" * 60)
            
            # 1. 连接到IB
            if not self.connect_to_ib():
                logger.error("❌ 无法连接到IB，跳过今日检查")
                return False
            
            # 2. 创建合约
            if not self.create_contracts():
                logger.error("❌ 无法创建合约，跳过今日检查")
                return False
            
            # 3. 分析交易条件
            should_trade, current_price = self.analyze_trading_conditions()
            
            if not should_trade:
                logger.info("❌ 不满足交易条件，今日不执行交易")
                # 更新最后检查日期
                beijing_time = datetime.now(self.beijing_tz)
                self.last_trade_date = beijing_time.date()
                return False
            
            # 4. 执行买入
            logger.info("🎯 满足所有交易条件，开始执行买入...")
            logger.info(f"📊 交易条件总结:")
            logger.info(f"   - TQQQ价格: ${current_price:.2f}")
            logger.info(f"   - EMA20信号: 满足 ✅")
            
            success = self.place_buy_order(percentage=0.1)  # 使用账户资金的10%
            
            if success:
                logger.info("🎉 今日策略执行成功!")
                # 更新最后交易日期
                beijing_time = datetime.now(self.beijing_tz)
                self.last_trade_date = beijing_time.date()
                return True
            else:
                logger.error("❌ 今日买入执行失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 执行每日策略失败: {e}")
            return False
    
    def run_continuous_strategy(self):
        """持续运行策略"""
        logger.info("🔄 启动持续运行模式...")
        logger.info("📅 每天北京时间21:20检查策略条件")
        logger.info("📊 策略条件:")
        logger.info("   1. 昨日TQQQ收盘价 > EMA20")
        logger.info("   2. 满足条件时买入账户资金的10%")
        logger.info("🌙 支持常规交易时间以外的交易")
        logger.info("💰 实盘模式 - 将实际下单并扣款!")
        logger.info("=" * 60)
        
        while self.running:
            try:
                # 检查是否应该执行策略
                if self.should_check_today():
                    # 执行策略
                    self.execute_daily_strategy()
                
                # 等待1分钟后再次检查
                time.sleep(60)
                
            except KeyboardInterrupt:
                logger.info("收到中断信号，正在退出...")
                break
            except Exception as e:
                logger.error(f"❌ 持续运行过程中出错: {e}")
                time.sleep(60)  # 出错后等待1分钟再继续
        
        # 断开连接
        if self.ib and self.ib.isConnected():
            self.ib.disconnect()
            logger.info("✅ 已断开连接")

def main():
    """主函数"""
    print("TQQQ智能交易策略 - 持续运行模式")
    print("=" * 60)
    print("⚠️  警告: 这是实盘交易策略!")
    print("🔄 持续运行模式 - 程序将一直运行直到手动关闭")
    print("⏰ 每天北京时间21:20自动检查策略条件")
    print("📊 策略条件:")
    print("   1. 昨日TQQQ收盘价 > EMA20")
    print("   2. 满足条件时买入账户资金的10%")
    print("🌙 支持常规交易时间以外的交易")
    print("💰 将实际扣款并执行交易")
    print("=" * 60)
    print("按 Ctrl+C 可以安全退出程序")
    print("=" * 60)
    
    # 创建策略实例
    strategy = TQQQSmartTradingStrategy(
        host='127.0.0.1',
        port=4001,
        client_id=444
    )
    
    # 运行持续策略
    strategy.run_continuous_strategy()

if __name__ == "__main__":
    main() 