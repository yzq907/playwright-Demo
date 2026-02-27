import os
import subprocess
import sys
import argparse
from pathlib import Path


def clean_old_data():
    """清理旧的测试数据"""
    print("\n[1/3] 清理旧的测试数据...")
    allure_results = Path("allure-results")
    
    if allure_results.exists():
        import shutil
        shutil.rmtree(allure_results)
        print("✓ 已清理 allure-results")


def run_tests(test_path=None, headed=False):
    """运行测试"""
    print("\n[2/3] 运行测试...")
    
    cmd = "pytest --alluredir=allure-results"
    
    if test_path:
        cmd += f" {test_path}"
    
    if headed:
        cmd += " --headed"
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print("✗ 测试运行失败")
        return False
    
    print("✓ 测试运行完成")
    return True


def serve_report():
    """启动 Allure 报告服务器"""
    print("\n[3/3] 启动 Allure 报告服务器...")
    print("提示: 按 Ctrl+C 停止服务器")
    print()
    
    cmd = "allure serve allure-results"
    subprocess.run(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser(description='Playwright 自动化测试启动器')
    parser.add_argument('--headed', action='store_true', help='使用有头模式运行测试（显示浏览器）')
    parser.add_argument('--path', type=str, help='指定测试文件或目录路径')
    parser.add_argument('--no-clean', action='store_true', help='不清理旧的测试数据')
    
    args = parser.parse_args()
    
    print("=" * 40)
    print("    Playwright 自动化测试启动器")
    print("=" * 40)
    
    try:
        if not args.no_clean:
            clean_old_data()
        
        if not run_tests(test_path=args.path, headed=args.headed):
            print("\n测试失败，请检查错误信息")
            sys.exit(1)
        
        serve_report()
        
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
