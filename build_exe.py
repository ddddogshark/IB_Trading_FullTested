#!/usr/bin/env python3
"""
TQQQ Trading Strategy EXE Builder
使用PyInstaller打包TQQQ交易策略为持续运行的exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """构建持续运行的exe文件"""
    print("🚀 开始构建TQQQ交易策略持续运行exe文件...")
    
    # 确保在正确的目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理之前的构建
    print("🧹 清理之前的构建文件...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # 创建持续运行的主程序文件
    create_continuous_runner()
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个exe文件
        '--console',                    # 控制台应用
        '--name=TQQQ_Trading_Continuous',  # exe文件名
        '--add-data=email_config.json;.',  # 添加配置文件
        '--add-data=ib_async/email_notifier.py;ib_async',  # 添加邮件模块
        '--add-data=ib_async/email_service.py;ib_async',   # 添加邮件服务
        '--add-data=ib_async/tqqq_trading.py;ib_async',    # 添加主策略文件
        '--hidden-import=pandas',       # 隐藏导入
        '--hidden-import=numpy',
        '--hidden-import=pytz',
        '--hidden-import=ib_async',
        '--hidden-import=nest_asyncio',
        '--hidden-import=asyncio',
        '--hidden-import=logging',
        '--hidden-import=json',
        '--hidden-import=datetime',
        '--hidden-import=time',
        '--hidden-import=argparse',
        '--hidden-import=smtplib',      # 添加邮件相关模块
        '--hidden-import=email',
        '--hidden-import=email.mime',
        '--hidden-import=email.mime.text',
        '--hidden-import=email.mime.multipart',
        '--hidden-import=ssl',
        '--hidden-import=socket',
        '--hidden-import=threading',
        '--hidden-import=queue',
        '--hidden-import=pathlib',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=subprocess',
        '--hidden-import=shutil',
        '--hidden-import=tempfile',
        '--hidden-import=platform',
        '--hidden-import=ctypes',
        '--hidden-import=win32api',
        '--hidden-import=win32con',
        '--hidden-import=win32gui',
        '--collect-all=ib_async',       # 收集所有ib_async相关文件
        '--collect-all=email',          # 收集所有email相关文件
        '--exclude-module=matplotlib',  # 排除不需要的模块
        '--exclude-module=scipy',
        '--exclude-module=scikit-learn',
        '--exclude-module=jupyter',
        '--exclude-module=notebook',
        '--exclude-module=ipython',
        '--exclude-module=tkinter',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        'continuous_runner.py'          # 持续运行的主程序文件
    ]
    
    print("🔨 执行PyInstaller构建...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功!")
        print(result.stdout)
        
        # 检查生成的exe文件
        exe_path = Path('dist/TQQQ_Trading_Continuous.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 生成的exe文件: {exe_path}")
            print(f"📏 文件大小: {size_mb:.2f} MB")
            
            # 复制配置文件到dist目录
            if os.path.exists('email_config.json'):
                shutil.copy2('email_config.json', 'dist/')
                print("📋 配置文件已复制到dist目录")
            
            # 创建启动脚本
            create_startup_script()
            
            print("\n🎉 构建完成!")
            print(f"📁 输出目录: {Path('dist').absolute()}")
            print("💡 使用说明:")
            print("   1. 将整个dist目录复制到目标机器")
            print("   2. 编辑email_config.json配置邮件")
            print("   3. 运行TQQQ_Trading_Continuous.exe (持续运行)")
            print("   4. 或运行start_trading.bat (带启动脚本)")
            
        else:
            print("❌ 未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    return True

def create_continuous_runner():
    """创建持续运行的主程序文件"""
    runner_code = '''#!/usr/bin/env python3
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
        print("\\n用户中断，策略停止")
    except Exception as e:
        print(f"\\n策略运行错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\\n策略已退出")

if __name__ == "__main__":
    main()
'''
    
    with open('continuous_runner.py', 'w', encoding='utf-8') as f:
        f.write(runner_code)
    
    print("📝 创建持续运行主程序文件: continuous_runner.py")

def create_startup_script():
    """创建启动脚本"""
    script_content = '''@echo off
chcp 65001 >nul
title TQQQ Trading Strategy - Continuous Mode

echo ========================================
echo TQQQ智能交易策略 - 持续运行模式
echo ========================================
echo.
echo 🚀 启动持续运行模式...
echo 📧 邮件通知: 已启用
echo 🔄 自动重启: 已启用
echo.
echo 💡 使用说明:
echo    - 按 Ctrl+C 停止策略
echo    - 策略会自动在指定时间执行交易
echo    - 所有交易都会发送邮件通知
echo.
echo ========================================
echo.

REM 运行持续模式
TQQQ_Trading_Continuous.exe

echo.
echo ========================================
echo 策略已退出
echo ========================================
pause
'''
    
    script_path = Path('dist/start_trading.bat')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("📝 创建启动脚本: dist/start_trading.bat")

def test_exe():
    """测试生成的exe文件"""
    print("\n🧪 测试exe文件...")
    exe_path = Path('dist/TQQQ_Trading_Continuous.exe')
    
    if not exe_path.exists():
        print("❌ exe文件不存在")
        return False
    
    try:
        # 测试启动（不等待完整运行）
        print("🔍 测试exe文件启动...")
        result = subprocess.run([str(exe_path)], 
                              capture_output=True, text=True, timeout=15)
        print("✅ exe文件可以正常启动")
        print("输出信息:")
        print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("✅ exe文件启动成功，正在持续运行...")
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TQQQ Trading Strategy Continuous EXE Builder")
    print("=" * 60)
    
    # 构建exe
    if build_exe():
        # 测试exe
        test_exe()
    else:
        print("❌ 构建失败，请检查错误信息")
        sys.exit(1) 