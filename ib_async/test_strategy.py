#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复后策略的测试脚本
"""

import asyncio
import sys
from tqqq_trading import TQQQSmartTradingStrategy

async def test_strategy():
    """测试策略功能"""
    print("🧪 测试修复后的TQQQ策略")
    print("=" * 50)
    
    # 创建策略实例
    strategy = TQQQSmartTradingStrategy()
    print("✅ 策略实例创建成功")
    
    # 测试连接
    print("\n[测试1] 连接IB Gateway...")
    try:
        connected = await strategy.connect_to_ib()
        if connected:
            print("✅ 连接成功")
        else:
            print("⚠️ 连接失败 (IB Gateway可能未运行)")
    except Exception as e:
        print(f"❌ 连接异常: {e}")
    
    # 测试合约创建
    print("\n[测试2] 创建TQQQ合约...")
    try:
        if strategy.create_contracts():
            print("✅ 合约创建成功")
            print(f"   合约信息: {strategy.tqqq_contract}")
        else:
            print("❌ 合约创建失败")
    except Exception as e:
        print(f"❌ 合约创建异常: {e}")
    
    # 如果连接成功，测试其他功能
    if strategy.ib.isConnected():
        print("\n[测试3] 获取历史数据...")
        try:
            data = await strategy.get_historical_data(strategy.tqqq_contract, '5 D')
            if data is not None and len(data) > 0:
                print("✅ 历史数据获取成功")
                print(f"   数据条数: {len(data)}")
                print(f"   最新价格: ${data.iloc[-1]['close']:.2f}")
            else:
                print("❌ 历史数据获取失败")
        except Exception as e:
            print(f"❌ 历史数据获取异常: {e}")
        
        print("\n[测试4] 计算EMA...")
        try:
            if data is not None:
                ema = strategy.calculate_ema(data['close'], 20)
                if ema is not None:
                    print("✅ EMA计算成功")
                    print(f"   最新EMA20: ${ema.iloc[-1]:.2f}")
                else:
                    print("❌ EMA计算失败")
        except Exception as e:
            print(f"❌ EMA计算异常: {e}")
        
        print("\n[测试5] 获取账户信息...")
        try:
            account_value = await strategy.get_account_info()
            if account_value is not None:
                print("✅ 账户信息获取成功")
                print(f"   账户总价值: ${account_value:,.2f}")
            else:
                print("❌ 账户信息获取失败")
        except Exception as e:
            print(f"❌ 账户信息获取异常: {e}")
        
        # 断开连接
        await strategy.ib.disconnect()
        print("\n✅ 已断开IB连接")
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")

if __name__ == "__main__":
    asyncio.run(test_strategy()) 