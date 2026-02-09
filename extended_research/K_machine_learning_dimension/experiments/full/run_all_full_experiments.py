#!/usr/bin/env python3
"""
完整实验套件 (E1-E6)
使用Matplotlib生成高质量图表
"""
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 80)
    print("K方向完整实验验证套件 (E1-E6)")
    print("=" * 80)
    print(f"开始时间: {datetime.now().isoformat()}")
    print()
    
    all_results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'version': 'full-experiment-v1.0',
            'environment': 'NumPy/SciPy/Matplotlib'
        },
        'experiments': {}
    }
    
    experiments = [
        ('E4', 'e4_real_dataset_simulation.py', '真实数据集验证'),
        ('E5', 'e5_scaling_laws.py', '标度律验证'),
        ('E6', 'e6_cross_direction.py', '跨方向连接验证'),
    ]
    
    for exp_id, script, desc in experiments:
        try:
            print(f"\n{'='*80}")
            print(f"运行 {exp_id}: {desc}")
            print(f"{'='*80}")
            
            # 动态导入并运行
            module_name = script.replace('.py', '')
            module = __import__(module_name)
            results = module.run_experiment()
            all_results['experiments'][exp_id] = results
            print(f"\n✓ {exp_id} 完成")
        except Exception as e:
            print(f"\n✗ {exp_id} 失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 保存汇总结果
    print("\n" + "=" * 80)
    print("保存实验汇总...")
    with open('all_experiments_full_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "=" * 80)
    print("实验完成!")
    print("=" * 80)
    print("生成的文件:")
    for f in ['results_e4_full.json', 'results_e5_full.json', 
              'results_e6_full.json', 'all_experiments_full_results.json',
              'e4_real_dataset_results.png', 'e5_scaling_laws.png', 
              'e6_cross_direction.png']:
        if os.path.exists(f):
            size = os.path.getsize(f)
            print(f"  - {f} ({size} bytes)")
    
    return all_results


if __name__ == '__main__':
    main()
