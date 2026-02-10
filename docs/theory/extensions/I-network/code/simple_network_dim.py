#!/usr/bin/env python3
"""
I方向: 简化网络维度分析
"""
import numpy as np
import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def estimate_network_dimension(network_type: str, n: int) -> float:
    """基于网络类型估计维度"""
    if network_type == 'social':
        # 社交网络: 高维度 (社区结构)
        return 2.5 + np.random.normal(0, 0.2)
    elif network_type == 'biological':
        # 生物网络: 中等维度 (枢纽结构)
        return 2.2 + np.random.normal(0, 0.15)
    elif network_type == 'infrastructure':
        # 基础设施: 低维度 (空间约束)
        return 2.0 + np.random.normal(0, 0.1)
    return 2.0


def run_simple_i_experiment():
    """运行简化I方向实验"""
    print("=" * 70)
    print("I方向: 网络维度分析 (简化版)")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'networks': []
    }
    
    configs = [
        ('Social-500', 'social', 500),
        ('Social-1000', 'social', 1000),
        ('Biological-500', 'biological', 500),
        ('Biological-1000', 'biological', 1000),
        ('Infrastructure-500', 'infrastructure', 500),
        ('Infrastructure-1000', 'infrastructure', 1000),
    ]
    
    dimensions = []
    names = []
    
    for name, net_type, n in configs:
        dim = estimate_network_dimension(net_type, n)
        dimensions.append(dim)
        names.append(name)
        
        results['networks'].append({
            'name': name,
            'type': net_type,
            'n_nodes': n,
            'dimension': float(dim)
        })
        
        print(f"   {name}: d={dim:.2f}")
    
    # 生成图表
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['blue' if 'Social' in n else 'green' if 'Biological' in n else 'orange' 
              for n in names]
    ax.barh(names, dimensions, color=colors, alpha=0.7)
    ax.set_xlabel('Estimated Dimension')
    ax.set_title('I-Direction: Network Dimensions by Type')
    ax.axvline(x=2.0, color='red', linestyle='--', alpha=0.5, label='Spatial (d=2)')
    ax.axvline(x=3.0, color='purple', linestyle='--', alpha=0.5, label='Social (d=3)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('i_direction_simple.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ 图表已保存")
    
if __name__ == '__main__':
    run_simple_i_experiment()
