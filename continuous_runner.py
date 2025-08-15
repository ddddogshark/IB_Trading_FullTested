#!/usr/bin/env python3
"""
TQQQ Trading Strategy Continuous Runner
持续运行TQQQ交易策略的主程序
"""

import sys
import os
import asyncio
import nest_asyncio

# 添加ib_async目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
ib_async_dir = os.path.join(current_dir, 'ib_async')
if os.path.exists(ib_async_dir):
    sys.path.insert(0, ib_async_dir)

# 应用nest_asyncio以支持嵌套事件循环
nest_asyncio.apply()

def main():
    """主函数 - 持续运行TQQQ交易策略"""
    try:
        # 导入主策略模块
        from tqqq_trading import TQQQSmartTradingStrategy
        
        print("启动TQQQ智能交易策略 (持续运行模式)")
        print("=" * 60)
        
        # 创建策略实例并运行
        strategy = TQQQSmartTradingStrategy()
        
        # 直接运行持续模式
        asyncio.run(strategy.run_strategy(continuous_mode=True))
        
    except KeyboardInterrupt:
        print("\n用户中断，策略停止")
    except Exception as e:
        print(f"\n策略运行错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n策略已退出")

if __name__ == "__main__":
    main()
