#!/usr/bin/env python3
"""
E2: 网络架构比较实验 (轻量级NumPy版本)
分析不同架构对有效维度的影响
"""
import numpy as np
import sys
import os
import json
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numpy_mlp import NumPyMLP, generate_synthetic_data
from e1_effective_dimension import EffectiveDimensionEstimator


def run_e2_experiment():
    """运行E2实验"""
    print("=" * 60)
    print("E2: 网络架构比较实验")
    print("=" * 60)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'experiments': []
    }
    
    # 实验1: 深度变化 (固定参数量)
    print("\n📊 实验1: 深度 vs 有效维度")
    depth_configs = []
    total_params_target = 5000
    
    for depth in [2, 3, 4, 5, 6]:
        # 计算每层的宽度以保持总参数大致相同
        # 输入10, 输出5, depth层 => depth-1个权重矩阵
        # 使用近似公式
        if depth == 2:
            width = 100
        elif depth == 3:
            width = 65
        elif depth == 4:
            width = 50
        elif depth == 5:
            width = 40
        else:
            width = 35
        
        layers = [10] + [width] * (depth - 1) + [5]
        depth_configs.append({
            'name': f'Depth-{depth}',
            'layers': layers,
            'depth': depth
        })
    
    depth_results = []
    for cfg in depth_configs:
        model = NumPyMLP(cfg['layers'], activation='relu')
        estimator = EffectiveDimensionEstimator('fisher')
        
        X, y = generate_synthetic_data(200, 10, 5)
        n_params = model.count_parameters()
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * n_params
        
        depth_results.append({
            'name': cfg['name'],
            'depth': cfg['depth'],
            'total_params': n_params,
            'd_eff': float(d_eff),
            'd_eff_ratio': float(d_eff / n_params)
        })
        
        print(f"   {cfg['name']}: params={n_params}, d_eff={d_eff:.1f} "
              f"({100*d_eff/n_params:.1f}%)")
    
    results['experiments'].append({
        'name': 'Depth Variation',
        'configs': depth_results
    })
    
    # 实验2: 宽度变化
    print("\n📊 实验2: 宽度 vs 有效维度")
    width_configs = []
    for width in [20, 40, 60, 80, 100]:
        layers = [10, width, width, 5]
        width_configs.append({
            'name': f'Width-{width}',
            'layers': layers,
            'width': width
        })
    
    width_results = []
    for cfg in width_configs:
        model = NumPyMLP(cfg['layers'], activation='relu')
        estimator = EffectiveDimensionEstimator('fisher')
        
        X, y = generate_synthetic_data(200, 10, 5)
        n_params = model.count_parameters()
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * n_params
        
        width_results.append({
            'name': cfg['name'],
            'width': cfg['width'],
            'total_params': n_params,
            'd_eff': float(d_eff),
            'd_eff_ratio': float(d_eff / n_params)
        })
        
        print(f"   {cfg['name']}: params={n_params}, d_eff={d_eff:.1f} "
              f"({100*d_eff/n_params:.1f}%)")
    
    results['experiments'].append({
        'name': 'Width Variation',
        'configs': width_results
    })
    
    # 实验3: 激活函数比较
    print("\n📊 实验3: 激活函数影响")
    activations = ['relu', 'tanh', 'sigmoid']
    base_layers = [10, 50, 50, 5]
    
    activation_results = []
    for act in activations:
        model = NumPyMLP(base_layers, activation=act)
        estimator = EffectiveDimensionEstimator('fisher')
        
        X, y = generate_synthetic_data(200, 10, 5)
        n_params = model.count_parameters()
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * n_params
        
        activation_results.append({
            'activation': act,
            'total_params': n_params,
            'd_eff': float(d_eff),
            'd_eff_ratio': float(d_eff / n_params)
        })
        
        print(f"   {act}: d_eff={d_eff:.1f} ({100*d_eff/n_params:.1f}%)")
    
    results['experiments'].append({
        'name': 'Activation Function',
        'configs': activation_results
    })
    
    # 关键发现
    print("\n📈 关键发现:")
    
    # 深度趋势
    d_ratios = [r['d_eff_ratio'] for r in depth_results]
    print(f"   深度增加时 d_eff/N 趋势: {d_ratios[0]:.3f} -> {d_ratios[-1]:.3f}")
    
    # 宽度趋势
    w_ratios = [r['d_eff_ratio'] for r in width_results]
    print(f"   宽度增加时 d_eff/N 趋势: {w_ratios[0]:.3f} -> {w_ratios[-1]:.3f}")
    
    # 保存结果
    output_file = 'results_e2_lightweight.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ 结果已保存到: {output_file}")
    
    return results


if __name__ == '__main__':
    run_e2_experiment()
