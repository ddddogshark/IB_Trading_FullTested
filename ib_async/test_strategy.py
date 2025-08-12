#!/usr/bin/env python3
"""
TQQQ智能交易策略测试脚本
用于测试策略的各个组件功能
"""

import sys
import time
from datetime import datetime
import pytz
from tqqq_final_trading import TQQQSmartTradingStrategy

def test_strategy_components():
    """测试策略的各个组件"""
    print("🧪 TQQQ智能交易策略组件测试")
    print("=" * 60)
    
    # 创建策略实例
    strategy = TQQQSmartTradingStrategy(
        host='127.0.0.1',
        port=4001,
        client_id=444
    )
    
    print("✅ 策略实例创建成功")
    
    # 测试1: 连接测试
    print("\n[测试1] 连接IB Gateway测试")
    print("-" * 40)
    try:
        connected = strategy.connect_to_ib()
        if connected:
            print("✅ 连接IB Gateway成功")
        else:
            print("❌ 连接IB Gateway失败")
            print("   请确保IB Gateway已启动并监听端口4001")
            return False
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False
    
    # 测试2: 合约创建测试
    print("\n[测试2] 合约创建测试")
    print("-" * 40)
    try:
        contracts_created = strategy.create_contracts()
        if contracts_created:
            print("✅ TQQQ合约创建成功")
            print(f"   合约信息: {strategy.tqqq_contract}")
        else:
            print("❌ 合约创建失败")
            return False
    except Exception as e:
        print(f"❌ 合约创建测试异常: {e}")
        return False
    
    # 测试3: 历史数据获取测试
    print("\n[测试3] 历史数据获取测试")
    print("-" * 40)
    try:
        historical_data = strategy.get_historical_data(
            strategy.tqqq_contract, 
            duration='5 D'
        )
        if historical_data is not None and len(historical_data) > 0:
            print("✅ 历史数据获取成功")
            print(f"   数据条数: {len(historical_data)}")
            print(f"   最新价格: ${historical_data.iloc[-1]['close']:.2f}")
            print(f"   数据日期范围: {historical_data.iloc[0]['date']} 到 {historical_data.iloc[-1]['date']}")
        else:
            print("❌ 历史数据获取失败")
            return False
    except Exception as e:
        print(f"❌ 历史数据获取测试异常: {e}")
        return False
    
    # 测试4: EMA计算测试
    print("\n[测试4] EMA计算测试")
    print("-" * 40)
    try:
        if historical_data is not None:
            ema20 = strategy.calculate_ema(historical_data['close'], 20)
            if ema20 is not None:
                print("✅ EMA20计算成功")
                print(f"   最新EMA20: ${ema20.iloc[-1]:.2f}")
                print(f"   最新收盘价: ${historical_data.iloc[-1]['close']:.2f}")
                
                # 判断信号
                if historical_data.iloc[-1]['close'] > ema20.iloc[-1]:
                    print("📈 当前信号: 买入信号 (收盘价 > EMA20)")
                else:
                    print("📉 当前信号: 卖出信号 (收盘价 < EMA20)")
            else:
                print("❌ EMA计算失败")
                return False
    except Exception as e:
        print(f"❌ EMA计算测试异常: {e}")
        return False
    
    # 测试5: 账户信息测试
    print("\n[测试5] 账户信息测试")
    print("-" * 40)
    try:
        account_value = strategy.get_account_value()
        if account_value > 0:
            print("✅ 账户信息获取成功")
            print(f"   账户总价值: ${account_value:,.2f}")
        else:
            print("⚠️ 账户信息获取失败或账户价值为0")
    except Exception as e:
        print(f"❌ 账户信息测试异常: {e}")
    
    # 测试6: 当前价格获取测试
    print("\n[测试6] 当前价格获取测试")
    print("-" * 40)
    try:
        current_price = strategy.get_current_tqqq_price()
        if current_price > 0:
            print("✅ 当前价格获取成功")
            print(f"   当前TQQQ价格: ${current_price:.2f}")
        else:
            print("❌ 当前价格获取失败")
            return False
    except Exception as e:
        print(f"❌ 当前价格获取测试异常: {e}")
        return False
    
    # 测试7: 仓位计算测试
    print("\n[测试7] 仓位计算测试")
    print("-" * 40)
    try:
        position_size = strategy.calculate_position_size(percentage=0.1)
        if position_size > 0:
            print("✅ 仓位计算成功")
            print(f"   计算股数: {position_size}股")
            print(f"   使用资金比例: 10%")
            estimated_cost = position_size * current_price
            print(f"   预估成本: ${estimated_cost:,.2f}")
        else:
            print("❌ 仓位计算失败")
            return False
    except Exception as e:
        print(f"❌ 仓位计算测试异常: {e}")
        return False
    
    # 测试8: 时间检查测试
    print("\n[测试8] 时间检查测试")
    print("-" * 40)
    try:
        beijing_time = datetime.now(strategy.beijing_tz)
        print(f"   当前北京时间: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        should_check = strategy.should_check_today()
        if should_check:
            print("✅ 当前时间满足检查条件")
        else:
            print("⏰ 当前时间不满足检查条件 (需要北京时间21:20±5分钟)")
    except Exception as e:
        print(f"❌ 时间检查测试异常: {e}")
    
    # 测试9: 交易条件分析测试
    print("\n[测试9] 交易条件分析测试")
    print("-" * 40)
    try:
        should_trade, price = strategy.analyze_trading_conditions()
        if should_trade:
            print("✅ 满足交易条件")
            print(f"   当前价格: ${price:.2f}")
            print("   建议: 可以执行买入")
        else:
            print("❌ 不满足交易条件")
            print(f"   当前价格: ${price:.2f}")
            print("   建议: 不执行交易")
    except Exception as e:
        print(f"❌ 交易条件分析测试异常: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 所有组件测试完成!")
    print("✅ 策略可以正常运行")
    print("=" * 60)
    
    return True

def test_manual_trade():
    """测试手动交易功能"""
    print("\n🧪 手动交易测试")
    print("=" * 60)
    print("⚠️  警告: 这将执行真实的买入交易!")
    print("   请确保您了解风险并确认要执行交易")
    print("=" * 60)
    
    confirm = input("确认要执行测试交易吗? (输入 'YES' 确认): ")
    if confirm != 'YES':
        print("❌ 测试交易已取消")
        return False
    
    strategy = TQQQSmartTradingStrategy(
        host='127.0.0.1',
        port=4001,
        client_id=444
    )
    
    try:
        # 连接和创建合约
        if not strategy.connect_to_ib():
            print("❌ 连接失败")
            return False
        
        if not strategy.create_contracts():
            print("❌ 合约创建失败")
            return False
        
        # 执行买入测试
        print("🚀 开始执行测试买入...")
        success = strategy.place_buy_order(percentage=0.01)  # 使用1%资金进行测试
        
        if success:
            print("🎉 测试买入成功!")
            return True
        else:
            print("❌ 测试买入失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试交易异常: {e}")
        return False

def main():
    """主函数"""
    print("TQQQ智能交易策略测试工具")
    print("=" * 60)
    print("请选择测试模式:")
    print("1. 组件功能测试 (推荐)")
    print("2. 手动交易测试 (实盘交易)")
    print("3. 退出")
    print("=" * 60)
    
    while True:
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == '1':
            success = test_strategy_components()
            if success:
                print("\n✅ 组件测试全部通过，策略可以正常运行!")
            else:
                print("\n❌ 组件测试失败，请检查配置")
            break
            
        elif choice == '2':
            success = test_manual_trade()
            if success:
                print("\n✅ 手动交易测试成功!")
            else:
                print("\n❌ 手动交易测试失败")
            break
            
        elif choice == '3':
            print("👋 退出测试工具")
            break
            
        else:
            print("❌ 无效选择，请输入1-3")

if __name__ == "__main__":
    main() 