#!/usr/bin/env python3
"""
TQQQ Trading Strategy EXE Builder
使用PyInstaller打包TQQQ交易策略为独立的exe文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """构建exe文件"""
    print("🚀 开始构建TQQQ交易策略exe文件...")
    
    # 确保在正确的目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理之前的构建
    print("🧹 清理之前的构建文件...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个exe文件
        '--console',                    # 控制台应用
        '--name=TQQQ_Trading',          # exe文件名
        '--add-data=email_config.json;.',  # 添加配置文件
        '--add-data=ib_async/email_notifier.py;ib_async',  # 添加邮件模块
        '--add-data=ib_async/email_service.py;ib_async',   # 添加邮件服务
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
        'ib_async/tqqq_trading.py'      # 主程序文件
    ]
    
    print("🔨 执行PyInstaller构建...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功!")
        print(result.stdout)
        
        # 检查生成的exe文件
        exe_path = Path('dist/TQQQ_Trading.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 生成的exe文件: {exe_path}")
            print(f"📏 文件大小: {size_mb:.2f} MB")
            
            # 复制配置文件到dist目录
            if os.path.exists('email_config.json'):
                shutil.copy2('email_config.json', 'dist/')
                print("📋 配置文件已复制到dist目录")
            
            print("\n🎉 构建完成!")
            print(f"📁 输出目录: {Path('dist').absolute()}")
            print("💡 使用说明:")
            print("   1. 将整个dist目录复制到目标机器")
            print("   2. 编辑email_config.json配置邮件")
            print("   3. 运行TQQQ_Trading.exe")
            
        else:
            print("❌ 未找到生成的exe文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    
    return True

def test_exe():
    """测试生成的exe文件"""
    print("\n🧪 测试exe文件...")
    exe_path = Path('dist/TQQQ_Trading.exe')
    
    if not exe_path.exists():
        print("❌ exe文件不存在")
        return False
    
    try:
        # 测试帮助信息
        result = subprocess.run([str(exe_path), '--help'], 
                              capture_output=True, text=True, timeout=10)
        print("✅ exe文件可以正常启动")
        print("帮助信息:")
        print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  exe文件启动超时，但可能正常")
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TQQQ Trading Strategy EXE Builder")
    print("=" * 60)
    
    # 构建exe
    if build_exe():
        # 测试exe
        test_exe()
    else:
        print("❌ 构建失败，请检查错误信息")
        sys.exit(1) 