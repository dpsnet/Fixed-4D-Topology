#!/usr/bin/env python3
"""
E4: 真实数据集验证实验 (NumPy模拟版本)
模拟MNIST/CIFAR-like数据结构的实验
"""
import numpy as np
import sys
import os
import json
from typing import Dict, List, Tuple
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lightweight.numpy_mlp import NumPyMLP, generate_synthetic_data, mse_loss
from lightweight.e1_effective_dimension import EffectiveDimensionEstimator


def generate_mnist_like_data(n_samples: int, n_classes: int = 10, 
                             input_dim: int = 784) -> Tuple[np.ndarray, np.ndarray]:
    """生成MNIST-like结构化数据"""
    np.random.seed(42)
    X = np.random.randn(n_samples, input_dim) * 0.5
    
    # 添加类特定的结构
    y = np.zeros((n_samples, n_classes))
    for i in range(n_samples):
        label = i % n_classes
        # One-hot编码
        y[i, label] = 1.0
        # 在特征中添加类特定模式
        X[i, label*10:(label+1)*10] += np.random.randn(10) * 2
    
    return X, y


def generate_cifar_like_data(n_samples: int, n_classes: int = 10,
                             input_dim: int = 3072) -> Tuple[np.ndarray, np.ndarray]:
    """生成CIFAR-like结构化数据 (RGB图像)"""
    np.random.seed(43)
    X = np.random.randn(n_samples, input_dim) * 0.3
    
    y = np.zeros((n_samples, n_classes))
    for i in range(n_samples):
        label = i % n_classes
        y[i, label] = 1.0
        # RGB通道特定模式
        channel_size = input_dim // 3
        for c in range(3):
            X[i, c*channel_size + label*10:c*channel_size + (label+1)*10] += np.random.randn(10) * 1.5
    
    return X, y


def run_e4_experiment():
    """运行E4实验"""
    print("=" * 70)
    print("E4: 真实数据集验证实验 (结构化数据模拟)")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'datasets': []
    }
    
    # 实验配置
    configs = [
        {
            'name': 'MNIST-like',
            'data_fn': generate_mnist_like_data,
            'input_dim': 784,
            'n_classes': 10,
            'train_samples': 5000,
            'test_samples': 1000,
            'architecture': [784, 256, 128, 10]
        },
        {
            'name': 'CIFAR-like',
            'data_fn': generate_cifar_like_data,
            'input_dim': 3072,
            'n_classes': 10,
            'train_samples': 3000,
            'test_samples': 600,
            'architecture': [3072, 512, 256, 10]
        },
        {
            'name': 'Small-Scale',
            'data_fn': generate_mnist_like_data,
            'input_dim': 256,
            'n_classes': 10,
            'train_samples': 2000,
            'test_samples': 400,
            'architecture': [256, 128, 64, 10]
        }
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for idx, cfg in enumerate(configs):
        print(f"\n📊 数据集: {cfg['name']}")
        print(f"   架构: {cfg['architecture']}")
        print(f"   训练样本: {cfg['train_samples']}")
        
        # 生成数据
        X_train, y_train = cfg['data_fn'](cfg['train_samples'], cfg['n_classes'], cfg['input_dim'])
        X_test, y_test = cfg['data_fn'](cfg['test_samples'], cfg['n_classes'], cfg['input_dim'])
        
        # 创建模型
        model = NumPyMLP(cfg['architecture'], activation='relu')
        n_params = model.count_parameters()
        
        # 计算有效维度
        estimator = EffectiveDimensionEstimator('fisher')
        pr = estimator.compute_participation_ratio(model)
        d_eff = pr * n_params
        
        # 计算泛化误差估计
        output_train = model.forward(X_train)
        train_error = np.mean((output_train - y_train) ** 2)
        
        output_test = model.forward(X_test)
        test_error = np.mean((output_test - y_test) ** 2)
        generalization_gap = test_error - train_error
        
        # 预测泛化界
        predicted_bound = np.sqrt(d_eff / cfg['train_samples'])
        
        dataset_result = {
            'name': cfg['name'],
            'architecture': cfg['architecture'],
            'total_params': n_params,
            'd_eff': float(d_eff),
            'd_eff_ratio': float(d_eff / n_params),
            'train_samples': cfg['train_samples'],
            'train_error': float(train_error),
            'test_error': float(test_error),
            'generalization_gap': float(generalization_gap),
            'predicted_bound': float(predicted_bound)
        }
        
        results['datasets'].append(dataset_result)
        
        print(f"   总参数: {n_params}")
        print(f"   有效维度: {d_eff:.1f} ({100*d_eff/n_params:.1f}%)")
        print(f"   训练误差: {train_error:.4f}")
        print(f"   测试误差: {test_error:.4f}")
        print(f"   泛化差距: {generalization_gap:.4f}")
        print(f"   预测泛化界: {predicted_bound:.4f}")
        
        # 绘图
        ax = axes[idx]
        metrics = ['Train Error', 'Test Error', 'Gen Gap', 'Pred Bound']
        values = [train_error, test_error, generalization_gap, predicted_bound]
        colors = ['green', 'orange', 'red', 'blue']
        ax.bar(metrics, values, color=colors, alpha=0.7)
        ax.set_title(f"{cfg['name']}\nd_eff/N={100*d_eff/n_params:.1f}%")
        ax.set_ylabel('Error / Bound')
        ax.tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    plt.savefig('e4_real_dataset_results.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ 图表已保存: e4_real_dataset_results.png")
    
    # 保存结果
    with open('results_e4_full.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ 结果已保存: results_e4_full.json")
    
    return results


if __name__ == '__main__':
    run_e4_experiment()
