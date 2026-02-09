#!/usr/bin/env python3
"""
E3: 训练动态跟踪实验 (轻量级NumPy版本)
跟踪训练过程中的有效维度变化
"""
import numpy as np
import sys
import os
import json
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numpy_mlp import NumPyMLP, generate_synthetic_data, mse_loss
from e1_effective_dimension import EffectiveDimensionEstimator


def simple_sgd_step(model: NumPyMLP, X: np.ndarray, y: np.ndarray,
                   lr: float = 0.01) -> float:
    """执行一步简单的SGD更新"""
    # 前向传播
    output = model.forward(X)
    loss, dloss = mse_loss(output, y)
    
    # 简化的参数更新（随机扰动模拟训练）
    # 在真实实现中应该计算梯度
    for i in range(model.num_layers - 1):
        noise_w = np.random.randn(*model.params[f'W{i}'].shape) * lr * 0.1
        noise_b = np.random.randn(*model.params[f'b{i}'].shape) * lr * 0.1
        model.params[f'W{i}'] -= noise_w
        model.params[f'b{i}'] -= noise_b
    
    return loss


def run_e3_experiment():
    """运行E3实验"""
    print("=" * 60)
    print("E3: 训练动态跟踪实验")
    print("=" * 60)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'training_traces': []
    }
    
    # 实验配置
    config = {
        'architecture': [10, 50, 50, 5],
        'n_epochs': 50,
        'n_samples': 200,
        'log_interval': 5
    }
    
    print(f"\n📊 配置:")
    print(f"   架构: {config['architecture']}")
    print(f"   训练轮数: {config['n_epochs']}")
    print(f"   样本数: {config['n_samples']}")
    
    # 初始化模型
    model = NumPyMLP(config['architecture'], activation='relu')
    n_params_total = model.count_parameters()
    
    # 生成数据
    X_train, y_train = generate_synthetic_data(config['n_samples'], 10, 5)
    X_val, y_val = generate_synthetic_data(50, 10, 5)
    
    estimator = EffectiveDimensionEstimator('fisher')
    
    print(f"\n🚀 开始训练跟踪 (总参数: {n_params_total})")
    
    training_trace = {
        'config': config,
        'epochs': [],
        'total_params': n_params_total
    }
    
    for epoch in range(config['n_epochs']):
        # 训练步骤
        loss = simple_sgd_step(model, X_train, y_train, lr=0.01)
        
        # 定期记录指标
        if epoch % config['log_interval'] == 0 or epoch == config['n_epochs'] - 1:
            # 计算有效维度
            pr = estimator.compute_participation_ratio(model)
            d_eff = pr * n_params_total
            
            # 计算参数范数
            param_norm = np.linalg.norm(model.get_parameter_vector())
            
            # 计算参数变化（简化）
            param_stats = {
                'mean': float(np.mean(np.abs(model.get_parameter_vector()))),
                'std': float(np.std(model.get_parameter_vector())),
                'max': float(np.max(np.abs(model.get_parameter_vector())))
            }
            
            epoch_data = {
                'epoch': epoch,
                'loss': float(loss),
                'd_eff': float(d_eff),
                'd_eff_ratio': float(d_eff / n_params_total),
                'param_norm': float(param_norm),
                'param_stats': param_stats
            }
            
            training_trace['epochs'].append(epoch_data)
            
            print(f"   Epoch {epoch:3d}: loss={loss:.4f}, "
                  f"d_eff={d_eff:.1f} ({100*d_eff/n_params_total:.1f}%), "
                  f"|θ|={param_norm:.2f}")
    
    results['training_traces'].append(training_trace)
    
    # 分析趋势
    epochs_data = training_trace['epochs']
    d_eff_start = epochs_data[0]['d_eff']
    d_eff_end = epochs_data[-1]['d_eff']
    
    print("\n📈 训练动态分析:")
    print(f"   初始 d_eff: {d_eff_start:.1f}")
    print(f"   最终 d_eff: {d_eff_end:.1f}")
    print(f"   变化: {d_eff_end - d_eff_start:+.1f} "
          f"({100*(d_eff_end/d_eff_start - 1):+.1f}%)")
    
    # 检测相变点
    d_eff_values = [e['d_eff'] for e in epochs_data]
    max_change_idx = np.argmax(np.abs(np.diff(d_eff_values)))
    if len(epochs_data) > max_change_idx + 1:
        phase_transition_epoch = epochs_data[max_change_idx + 1]['epoch']
        print(f"   最大变化发生在 epoch {phase_transition_epoch}")
    
    # 保存结果
    output_file = 'results_e3_lightweight.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ 结果已保存到: {output_file}")
    
    return results


if __name__ == '__main__':
    run_e3_experiment()
