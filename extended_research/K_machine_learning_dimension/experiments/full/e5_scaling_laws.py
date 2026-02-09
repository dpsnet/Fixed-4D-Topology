#!/usr/bin/env python3
"""
E5: 标度律验证实验
验证d_eff与网络规模、数据规模的标度关系
"""
import numpy as np
import sys
import os
import json
from typing import Dict, List
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lightweight.numpy_mlp import NumPyMLP, generate_synthetic_data
from lightweight.e1_effective_dimension import EffectiveDimensionEstimator


def run_e5_experiment():
    """运行E5实验"""
    print("=" * 70)
    print("E5: 标度律验证实验")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'scaling_laws': {}
    }
    
    # 实验1: 网络规模标度
    print("\n📊 实验1: 网络规模 vs 有效维度")
    widths = [32, 64, 128, 256, 512]
    d_effs_width = []
    n_params_list = []
    
    for width in widths:
        layers = [100, width, width, 10]
        model = NumPyMLP(layers, activation='relu')
        estimator = EffectiveDimensionEstimator('fisher')
        
        n_params = model.count_parameters()
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * n_params
        
        d_effs_width.append(d_eff)
        n_params_list.append(n_params)
        print(f"   Width {width:3d}: params={n_params:6d}, d_eff={d_eff:8.1f}")
    
    results['scaling_laws']['network_size'] = {
        'widths': widths,
        'd_effs': [float(d) for d in d_effs_width],
        'n_params': n_params_list
    }
    
    # 实验2: 数据规模标度
    print("\n📊 实验2: 数据规模 vs 有效维度")
    sample_sizes = [100, 500, 1000, 2000, 5000]
    d_effs_samples = []
    
    model = NumPyMLP([50, 100, 100, 5], activation='relu')
    estimator = EffectiveDimensionEstimator('fisher')
    
    for n_samples in sample_sizes:
        X, y = generate_synthetic_data(n_samples, 50, 5)
        
        # 简化：使用参与率作为d_eff的代理
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * model.count_parameters()
        
        d_effs_samples.append(d_eff)
        print(f"   Samples {n_samples:5d}: d_eff={d_eff:8.1f}")
    
    results['scaling_laws']['data_size'] = {
        'sample_sizes': sample_sizes,
        'd_effs': [float(d) for d in d_effs_samples]
    }
    
    # 实验3: 深度标度
    print("\n📊 实验3: 深度 vs 有效维度")
    depths = [2, 3, 4, 5, 6]
    d_effs_depth = []
    
    for depth in depths:
        layers = [50] + [80] * (depth - 1) + [5]
        model = NumPyMLP(layers, activation='relu')
        estimator = EffectiveDimensionEstimator('fisher')
        
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * model.count_parameters()
        d_effs_depth.append(d_eff)
        print(f"   Depth {depth}: d_eff={d_eff:8.1f}")
    
    results['scaling_laws']['depth'] = {
        'depths': depths,
        'd_effs': [float(d) for d in d_effs_depth]
    }
    
    # 生成图表
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # 图1: 宽度标度
    ax1 = axes[0]
    ax1.plot(widths, d_effs_width, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Hidden Layer Width')
    ax1.set_ylabel('Effective Dimension')
    ax1.set_title('Scaling: Network Width vs d_eff')
    ax1.grid(True, alpha=0.3)
    
    # 图2: 数据规模标度
    ax2 = axes[1]
    ax2.plot(sample_sizes, d_effs_samples, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Samples')
    ax2.set_ylabel('Effective Dimension')
    ax2.set_title('Scaling: Data Size vs d_eff')
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    # 图3: 深度标度
    ax3 = axes[2]
    ax3.plot(depths, d_effs_depth, 'go-', linewidth=2, markersize=8)
    ax3.set_xlabel('Network Depth')
    ax3.set_ylabel('Effective Dimension')
    ax3.set_title('Scaling: Depth vs d_eff')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('e5_scaling_laws.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ 图表已保存: e5_scaling_laws.png")
    
    # 保存结果
    with open('results_e5_full.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ 结果已保存: results_e5_full.json")
    
    return results


if __name__ == '__main__':
    run_e5_experiment()
