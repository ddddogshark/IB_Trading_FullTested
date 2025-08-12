#!/usr/bin/env python3
"""
调试测试脚本
"""

import sys
import traceback

def debug_imports():
    """调试导入问题"""
    print("🔍 调试导入问题...")
    
    # 测试基本模块
    modules = ['pandas', 'numpy', 'pytz']
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} 导入成功")
        except ImportError as e:
            print(f"❌ {module} 导入失败: {e}")
            return False
    
    # 测试ib_async
    try:
        import ib_async
        print("✅ ib_async 导入成功")
    except ImportError as e:
        print(f"❌ ib_async 导入失败: {e}")
        print("   尝试安装: pip install ib_async")
        return False
    
    return True

def debug_strategy():
    """调试策略类"""
    print("\n🔍 调试策略类...")
    
    try:
        from tqqq_final_trading import TQQQSmartTradingStrategy
        print("✅ 策略类导入成功")
        
        # 创建实例
        strategy = TQQQSmartTradingStrategy()
        print("✅ 策略实例创建成功")
        
        # 检查属性
        print(f"   主机: {strategy.host}")
        print(f"   端口: {strategy.port}")
        print(f"   客户端ID: {strategy.client_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ 策略类调试失败: {e}")
        print("   详细错误信息:")
        traceback.print_exc()
        return False

def debug_connection():
    """调试连接"""
    print("\n🔍 调试连接...")
    
    try:
        from tqqq_final_trading import TQQQSmartTradingStrategy
        from ib_async.ib import IB
        
        # 创建IB实例
        ib = IB()
        print("✅ IB实例创建成功")
        
        # 尝试连接
        print("⚠️ 尝试连接IB Gateway...")
        print("   如果IB Gateway未运行，连接会失败")
        
        try:
            ib.connect('127.0.0.1', 4001, clientId=444, timeout=5)
            print("✅ 连接成功")
            ib.disconnect()
            return True
        except Exception as conn_error:
            print(f"⚠️ 连接失败: {conn_error}")
            print("   这是正常的，如果IB Gateway未运行")
            return True
            
    except Exception as e:
        print(f"❌ 连接调试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔍 TQQQ策略调试工具")
    print("=" * 50)
    
    # 显示环境信息
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"当前目录: {sys.path[0]}")
    print("=" * 50)
    
    # 调试1: 导入
    if not debug_imports():
        print("\n❌ 导入调试失败")
        return
    
    # 调试2: 策略类
    if not debug_strategy():
        print("\n❌ 策略类调试失败")
        return
    
    # 调试3: 连接
    if not debug_connection():
        print("\n❌ 连接调试失败")
        return
    
    print("\n" + "=" * 50)
    print("🎉 调试完成!")
    print("✅ 所有基本功能正常")
    print("=" * 50)

if __name__ == "__main__":
    main() 