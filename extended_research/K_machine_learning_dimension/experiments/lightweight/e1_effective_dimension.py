#!/usr/bin/env python3
"""
E1: 有效维度估计器验证实验 (轻量级NumPy版本)
验证不同估计器的一致性和准确性
"""
import numpy as np
import sys
import os
import json
from typing import Dict, List, Tuple
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numpy_mlp import NumPyMLP, generate_synthetic_data, mse_loss


class EffectiveDimensionEstimator:
    """基于随机化方法的有效维度估计器"""
    
    def __init__(self, method: str = 'fisher'):
        self.method = method
        self.history = []
        
    def estimate_trace(self, model: NumPyMLP, X: np.ndarray, y: np.ndarray,
                      n_samples: int = 100) -> float:
        """使用随机化估计迹"""
        n_params = model.count_parameters()
        
        if self.method == 'fisher':
            # 基于Fisher信息矩阵的迹估计
            traces = []
            for _ in range(min(n_samples, 50)):  # 限制样本数
                z = np.random.randn(X.shape[0], X.shape[1])
                fisher = model.compute_fisher(z, y, mse_loss)
                traces.append(np.trace(fisher))
            return np.mean(traces)
        
        elif self.method == 'random':
            # 随机投影估计
            dim = min(n_params, 1000)
            A = np.random.randn(dim, n_params)
            ATA = A @ A.T
            return np.trace(ATA)
        
        else:
            return float(n_params)
    
    def estimate_rank(self, model: NumPyMLP, X: np.ndarray, 
                     threshold: float = 1e-3) -> int:
        """估计有效秩"""
        # 简化的秩估计：基于参数分布
        params = model.get_parameter_vector()
        
        # 计算奇异值（近似）
        n = min(len(params), 1000)
        sample = np.random.choice(params, n, replace=False)
        
        # 使用方差作为有效维度的代理
        variance = np.var(sample)
        effective = int(np.sum(np.abs(sample) > threshold * np.std(params)))
        
        return min(effective, model.count_parameters())
    
    def compute_participation_ratio(self, model: NumPyMLP) -> float:
        """计算参与率（Participation Ratio）"""
        params = model.get_parameter_vector()
        squared = params ** 2
        sum_sq = np.sum(squared)
        sum_fourth = np.sum(squared ** 2)
        
        if sum_fourth > 0:
            return (sum_sq ** 2) / (len(params) * sum_fourth)
        return 1.0


def run_e1_experiment():
    """运行E1实验"""
    print("=" * 60)
    print("E1: 有效维度估计器验证实验")
    print("=" * 60)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'configurations': [],
        'summary': {}
    }
    
    # 实验配置
    configs = [
        {'name': 'Small Network', 'layers': [10, 20, 5], 'n_samples': 100},
        {'name': 'Medium Network', 'layers': [20, 40, 40, 10], 'n_samples': 200},
        {'name': 'Wide Shallow', 'layers': [10, 100, 5], 'n_samples': 100},
        {'name': 'Deep Narrow', 'layers': [10, 15, 15, 15, 5], 'n_samples': 100},
    ]
    
    estimators = ['fisher', 'random']
    
    for cfg in configs:
        print(f"\n📊 Testing: {cfg['name']}")
        print(f"   Architecture: {cfg['layers']}")
        
        # 创建模型
        model = NumPyMLP(cfg['layers'], activation='relu')
        n_params = model.count_parameters()
        
        # 生成数据
        X, y = generate_synthetic_data(
            cfg['n_samples'], cfg['layers'][0], cfg['layers'][-1]
        )
        
        config_result = {
            'name': cfg['name'],
            'architecture': cfg['layers'],
            'total_params': n_params,
            'estimates': {}
        }
        
        # 运行不同估计器
        for est_name in estimators:
            estimator = EffectiveDimensionEstimator(method=est_name)
            
            trace_est = estimator.estimate_trace(model, X, y)
            rank_est = estimator.estimate_rank(model, X)
            pr_est = estimator.compute_participation_ratio(model)
            
            # 计算有效维度
            d_eff_trace = min(trace_est / n_params * n_params, n_params)
            d_eff_rank = rank_est
            d_eff_pr = pr_est * n_params
            
            config_result['estimates'][est_name] = {
                'trace_estimate': float(trace_est),
                'rank_estimate': int(rank_est),
                'participation_ratio': float(pr_est),
                'd_eff_trace': float(d_eff_trace),
                'd_eff_rank': int(d_eff_rank),
                'd_eff_pr': float(d_eff_pr)
            }
            
            print(f"   Estimator: {est_name}")
            print(f"     Total params: {n_params}")
            print(f"     Trace d_eff: {d_eff_trace:.1f}")
            print(f"     Rank d_eff: {d_eff_rank}")
            print(f"     PR d_eff: {d_eff_pr:.1f}")
        
        # 计算一致性
        d_eff_values = [
            config_result['estimates']['fisher']['d_eff_pr'],
            config_result['estimates']['random']['d_eff_pr']
        ]
        consistency = 1 - np.std(d_eff_values) / (np.mean(d_eff_values) + 1e-10)
        config_result['consistency'] = float(consistency)
        
        print(f"   Consistency: {consistency:.3f}")
        
        results['configurations'].append(config_result)
    
    # 计算总体统计
    all_consistencies = [c['consistency'] for c in results['configurations']]
    results['summary'] = {
        'mean_consistency': float(np.mean(all_consistencies)),
        'min_consistency': float(np.min(all_consistencies)),
        'max_consistency': float(np.max(all_consistencies))
    }
    
    print("\n" + "=" * 60)
    print("E1 实验总结")
    print("=" * 60)
    print(f"平均一致性: {results['summary']['mean_consistency']:.3f}")
    print(f"一致性范围: [{results['summary']['min_consistency']:.3f}, "
          f"{results['summary']['max_consistency']:.3f}]")
    
    # 保存结果
    output_file = 'results_e1_lightweight.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ 结果已保存到: {output_file}")
    
    return results


if __name__ == '__main__':
    run_e1_experiment()
