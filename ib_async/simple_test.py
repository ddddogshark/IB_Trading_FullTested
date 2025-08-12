#!/usr/bin/env python3
"""
简化的TQQQ策略测试
"""

import sys
import time
from datetime import datetime
import pytz

def test_imports():
    """测试导入功能"""
    print("🧪 测试导入功能...")
    
    try:
        import pandas as pd
        print("✅ pandas导入成功")
    except ImportError as e:
        print(f"❌ pandas导入失败: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy导入成功")
    except ImportError as e:
        print(f"❌ numpy导入失败: {e}")
        return False
    
    try:
        import pytz
        print("✅ pytz导入成功")
    except ImportError as e:
        print(f"❌ pytz导入失败: {e}")
        return False
    
    try:
        import ib_async
        print("✅ ib_async导入成功")
    except ImportError as e:
        print(f"❌ ib_async导入失败: {e}")
        return False
    
    return True

def test_strategy_class():
    """测试策略类"""
    print("\n🧪 测试策略类...")
    
    try:
        from tqqq_final_trading import TQQQSmartTradingStrategy
        print("✅ 策略类导入成功")
        
        # 创建策略实例
        strategy = TQQQSmartTradingStrategy()
        print("✅ 策略实例创建成功")
        
        # 测试时区设置
        beijing_time = datetime.now(strategy.beijing_tz)
        print(f"✅ 时区设置正确: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 策略类测试失败: {e}")
        return False

def test_connection():
    """测试连接功能"""
    print("\n🧪 测试连接功能...")
    
    try:
        from tqqq_final_trading import TQQQSmartTradingStrategy
        
        strategy = TQQQSmartTradingStrategy()
        
        # 尝试连接（可能会失败，因为IB Gateway可能没有运行）
        print("⚠️ 尝试连接IB Gateway...")
        print("   注意: 如果IB Gateway未运行，连接会失败")
        
        connected = strategy.connect_to_ib()
        
        if connected:
            print("✅ 连接IB Gateway成功")
            return True
        else:
            print("⚠️ 连接IB Gateway失败")
            print("   这可能是正常的，如果IB Gateway未运行")
            return True  # 不认为是错误
            
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False

def main():
    """主函数"""
    print("TQQQ智能交易策略 - 简化测试")
    print("=" * 50)
    
    # 测试1: 导入功能
    if not test_imports():
        print("\n❌ 导入测试失败")
        return
    
    # 测试2: 策略类
    if not test_strategy_class():
        print("\n❌ 策略类测试失败")
        return
    
    # 测试3: 连接功能
    if not test_connection():
        print("\n❌ 连接测试失败")
        return
    
    print("\n" + "=" * 50)
    print("🎉 简化测试完成!")
    print("✅ 策略基本功能正常")
    print("=" * 50)
    print("\n📋 下一步:")
    print("1. 确保IB Gateway已启动")
    print("2. 运行完整测试: python test_strategy.py")
    print("3. 启动策略: python tqqq_final_trading.py")

if __name__ == "__main__":
    main() 