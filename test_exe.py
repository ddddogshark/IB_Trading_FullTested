#!/usr/bin/env python3
"""
TQQQ Trading Strategy EXE Test
测试exe文件的基本功能
"""

import subprocess
import time
import os
from pathlib import Path

def test_exe_basic():
    """测试exe文件基本功能"""
    print("🧪 测试TQQQ_Trading_Continuous.exe基本功能...")
    
    exe_path = Path('dist/TQQQ_Trading_Continuous.exe')
    if not exe_path.exists():
        print("❌ exe文件不存在")
        return False
    
    try:
        # 启动exe文件
        print("🚀 启动exe文件...")
        process = subprocess.Popen(
            [str(exe_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 等待几秒钟看输出
        print("⏳ 等待程序启动...")
        time.sleep(10)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            print("✅ exe文件正在运行")
            
            # 读取输出
            try:
                stdout, stderr = process.communicate(timeout=5)
                print("📤 程序输出:")
                print(stdout[:1000] + "..." if len(stdout) > 1000 else stdout)
                if stderr:
                    print("❌ 错误输出:")
                    print(stderr)
            except subprocess.TimeoutExpired:
                print("⏰ 程序仍在运行，输出超时")
            
            # 终止进程
            print("🛑 终止测试进程...")
            process.terminate()
            process.wait(timeout=5)
            print("✅ 测试完成")
            return True
        else:
            print("❌ exe文件已退出")
            stdout, stderr = process.communicate()
            print("输出:", stdout)
            print("错误:", stderr)
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_startup_script():
    """测试启动脚本"""
    print("\n🧪 测试启动脚本...")
    
    script_path = Path('dist/start_trading.bat')
    if not script_path.exists():
        print("❌ 启动脚本不存在")
        return False
    
    print("✅ 启动脚本存在")
    print("📝 脚本内容:")
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    
    return True

def check_files():
    """检查生成的文件"""
    print("\n📁 检查生成的文件...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist目录不存在")
        return False
    
    files = list(dist_dir.glob('*'))
    print(f"📦 dist目录包含 {len(files)} 个文件:")
    
    for file in files:
        if file.is_file():
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"   {file.name} ({size_mb:.2f} MB)")
        else:
            print(f"   {file.name}/ (目录)")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("TQQQ Trading Strategy EXE Test")
    print("=" * 60)
    
    # 检查文件
    check_files()
    
    # 测试启动脚本
    test_startup_script()
    
    # 测试exe文件
    test_exe_basic()
    
    print("\n🎉 测试完成!") 