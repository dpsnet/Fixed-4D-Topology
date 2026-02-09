#!/usr/bin/env python3
"""
运行所有轻量级实验
生成论文所需数据
"""
import sys
import os
import json
from datetime import datetime

# 确保导入路径正确
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("K方向实验验证套件 (轻量级NumPy版本)")
    print("=" * 70)
    print(f"开始时间: {datetime.now().isoformat()}")
    print()
    
    all_results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'version': 'lightweight-numpy-v1.0',
            'description': 'PyTorch-free implementation for resource-constrained environments'
        },
        'experiments': {}
    }
    
    # E1: 有效维度估计器验证
    try:
        print("\n" + "=" * 70)
        from e1_effective_dimension import run_e1_experiment
        results_e1 = run_e1_experiment()
        all_results['experiments']['E1'] = results_e1
        print("\n✓ E1 完成")
    except Exception as e:
        print(f"\n✗ E1 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # E2: 网络架构比较
    try:
        print("\n" + "=" * 70)
        from e2_architecture_comparison import run_e2_experiment
        results_e2 = run_e2_experiment()
        all_results['experiments']['E2'] = results_e2
        print("\n✓ E2 完成")
    except Exception as e:
        print(f"\n✗ E2 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # E3: 训练动态
    try:
        print("\n" + "=" * 70)
        from e3_training_dynamics import run_e3_experiment
        results_e3 = run_e3_experiment()
        all_results['experiments']['E3'] = results_e3
        print("\n✓ E3 完成")
    except Exception as e:
        print(f"\n✗ E3 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 保存汇总结果
    print("\n" + "=" * 70)
    print("保存实验汇总...")
    with open('all_experiments_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "=" * 70)
    print("实验完成!")
    print("=" * 70)
    print(f"结果文件:")
    for f in ['results_e1_lightweight.json', 'results_e2_lightweight.json', 
              'results_e3_lightweight.json', 'all_experiments_results.json']:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  - {f} ({size} bytes)")
    
    return all_results


if __name__ == '__main__':
    main()
