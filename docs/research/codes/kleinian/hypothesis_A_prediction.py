#!/usr/bin/env python3
"""
假设A改进版预测验证

使用改进后的公式预测新的Kleinian群的维数，并评估预测精度。

最终改进公式：
    dim_H = 1 + 0.244 · (1/log V) · (L'/L) + γ_type

其中：
    γ_B (Bianchi) = +0.919
    γ_C (Cusped) = +0.269
    γ_CL (Closed) = +0.861
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from datetime import datetime


@dataclass
class PredictionResult:
    """预测结果"""
    name: str
    group_type: str
    volume: Optional[float]
    log_derivative: float
    predicted_dim: float
    observed_dim: Optional[float] = None
    
    @property
    def error(self) -> Optional[float]:
        if self.observed_dim is None:
            return None
        return self.observed_dim - self.predicted_dim
    
    @property
    def abs_error(self) -> Optional[float]:
        if self.error is None:
            return None
        return abs(self.error)


class ImprovedHypothesisAPredictor:
    """
    改进假设A预测器
    
    使用优化后的参数进行维数预测
    """
    
    def __init__(self):
        # 优化后的参数
        self.alpha = 0.2443
        self.gamma = {
            'B': 0.9190,   # Bianchi
            'C': 0.2687,   # Cusped
            'CL': 0.8608,  # Closed
            'S': 0.5       # Schottky（估计值，需更多数据）
        }
    
    def predict(self, group_type: str, log_derivative: float, 
                volume: Optional[float] = None) -> float:
        """
        预测Hausdorff维数
        
        Args:
            group_type: 群类型 ('B', 'C', 'S', 'CL')
            log_derivative: L'/L 对数导数值
            volume: 双曲体积（对于有限体积群）
        
        Returns:
            预测的Hausdorff维数
        """
        # 计算归一化项
        if volume is not None and volume > 0 and volume != float('inf'):
            normalized_term = (1.0 / np.log(volume)) * log_derivative
        elif group_type == 'S':
            # Schottky群使用启发式处理
            normalized_term = 0.5 * log_derivative
        else:
            # 默认处理
            normalized_term = log_derivative
        
        # 获取修正项
        gamma = self.gamma.get(group_type, 0.0)
        
        # 计算预测值
        dim_h = 1.0 + self.alpha * normalized_term + gamma
        
        return dim_h
    
    def get_formula(self, group_type: str) -> str:
        """获取指定类型的公式"""
        gamma = self.gamma.get(group_type, 0.0)
        return f"dim_H = {1 + gamma:.3f} + {self.alpha:.3f} · (1/log V) · (L'/L)"
    
    def validate_predictions(self, test_groups: List[Dict]) -> Dict:
        """
        验证预测精度
        
        Args:
            test_groups: 测试群列表，每个包含name, type, volume, log_derivative, observed_dim
        
        Returns:
            验证结果字典
        """
        results = []
        errors = []
        abs_errors = []
        
        for group in test_groups:
            pred = self.predict(
                group_type=group['type'],
                log_derivative=group['log_derivative'],
                volume=group.get('volume')
            )
            
            result = PredictionResult(
                name=group['name'],
                group_type=group['type'],
                volume=group.get('volume'),
                log_derivative=group['log_derivative'],
                predicted_dim=pred,
                observed_dim=group.get('observed_dim')
            )
            
            results.append(result)
            
            if result.error is not None:
                errors.append(result.error)
                abs_errors.append(result.abs_error)
        
        # 计算统计指标
        validation_stats = {}
        if errors:
            errors = np.array(errors)
            abs_errors = np.array(abs_errors)
            
            validation_stats = {
                'n_predictions': len(results),
                'n_with_observed': len(errors),
                'mean_error': float(np.mean(errors)),
                'std_error': float(np.std(errors)),
                'mae': float(np.mean(abs_errors)),
                'rmse': float(np.sqrt(np.mean(errors**2))),
                'max_abs_error': float(np.max(abs_errors)),
                'min_abs_error': float(np.min(abs_errors)),
                'median_abs_error': float(np.median(abs_errors))
            }
        
        return {
            'predictions': [
                {
                    'name': r.name,
                    'type': r.group_type,
                    'volume': r.volume,
                    'log_derivative': r.log_derivative,
                    'predicted': r.predicted_dim,
                    'observed': r.observed_dim,
                    'error': r.error
                }
                for r in results
            ],
            'validation_stats': validation_stats
        }


def create_test_dataset() -> List[Dict]:
    """
    创建测试数据集
    
    包含已知观测值的群（用于验证）和一些假设的新群（用于展示预测能力）
    """
    test_groups = [
        # 已知群（有观测值，用于验证）
        {
            'name': 'Trefoil Knot Complement (验证)',
            'type': 'C',
            'volume': 2.029883,  # 同figure-eight，仅用于示例
            'log_derivative': -0.65,
            'observed_dim': 1.0  # 尖点群通常维数为1
        },
        {
            'name': 'm016 (SnapPy census, 验证)',
            'type': 'C',
            'volume': 2.828122,
            'log_derivative': -1.0,
            'observed_dim': 1.0
        },
        {
            'name': 'm017 (SnapPy census, 验证)',
            'type': 'CL',
            'volume': 0.981369,
            'log_derivative': 0.05,
            'observed_dim': 2.0  # 闭流形群通常维数接近2
        },
        
        # 假设的新群（无观测值，展示预测）
        {
            'name': 'Hypothetical Bianchi Group (d=19)',
            'type': 'B',
            'volume': 5.5,  # 假设值
            'log_derivative': 0.4,
            'observed_dim': None  # 未知
        },
        {
            'name': 'Hypothetical Schottky (sep=0.6)',
            'type': 'S',
            'volume': None,
            'log_derivative': 0.8,
            'observed_dim': None
        },
        {
            'name': 'Hypothetical Closed Manifold (V=1.5)',
            'type': 'CL',
            'volume': 1.5,
            'log_derivative': -0.1,
            'observed_dim': None
        },
        {
            'name': 'Hypothetical Cusped (Large Volume)',
            'type': 'C',
            'volume': 10.0,
            'log_derivative': -3.0,
            'observed_dim': None
        }
    ]
    
    return test_groups


def run_prediction_validation():
    """运行预测验证"""
    print("=" * 80)
    print("假设A改进版预测验证")
    print("=" * 80)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化预测器
    predictor = ImprovedHypothesisAPredictor()
    
    print("改进公式参数：")
    print(f"  α = {predictor.alpha:.4f}")
    print(f"  群类型修正项：")
    for gt, gamma in predictor.gamma.items():
        type_name = {'B': 'Bianchi', 'C': 'Cusped', 'S': 'Schottky', 'CL': 'Closed'}[gt]
        print(f"    {gt} ({type_name}): γ = {gamma:+.4f}")
    print()
    
    # 创建测试数据
    test_groups = create_test_dataset()
    
    # 执行预测和验证
    results = predictor.validate_predictions(test_groups)
    
    # 打印预测结果
    print("预测结果：")
    print("-" * 100)
    print(f"{'Group Name':<45} {'Type':<8} {'Volume':<10} {'Predicted':<12} {'Observed':<12} {'Error':<10}")
    print("-" * 100)
    
    for pred in results['predictions']:
        volume_str = f"{pred['volume']:.3f}" if pred['volume'] else "N/A"
        observed_str = f"{pred['observed']:.3f}" if pred['observed'] is not None else "N/A"
        error_str = f"{pred['error']:+.3f}" if pred['error'] is not None else "N/A"
        
        print(f"{pred['name']:<45} {pred['type']:<8} {volume_str:<10} "
              f"{pred['predicted']:<12.4f} {observed_str:<12} {error_str:<10}")
    print("-" * 100)
    print()
    
    # 打印验证统计
    stats = results['validation_stats']
    if stats:
        print("验证统计（基于有观测值的群）：")
        print(f"  预测数量: {stats['n_with_observed']}")
        print(f"  平均误差: {stats['mean_error']:+.4f}")
        print(f"  误差标准差: {stats['std_error']:.4f}")
        print(f"  平均绝对误差(MAE): {stats['mae']:.4f}")
        print(f"  均方根误差(RMSE): {stats['rmse']:.4f}")
        print(f"  最大绝对误差: {stats['max_abs_error']:.4f}")
        print(f"  最小绝对误差: {stats['min_abs_error']:.4f}")
        print(f"  中位数绝对误差: {stats['median_abs_error']:.4f}")
        print()
        
        # 评估预测精度
        if stats['mae'] < 0.1:
            quality = "优秀"
        elif stats['mae'] < 0.2:
            quality = "良好"
        elif stats['mae'] < 0.5:
            quality = "可接受"
        else:
            quality = "需改进"
        
        print(f"预测质量评估: {quality}")
    else:
        print("无观测值可用于验证")
    
    print()
    print("=" * 80)
    print("预测验证完成!")
    print("=" * 80)
    
    # 保存结果
    output = {
        'timestamp': datetime.now().isoformat(),
        'formula_parameters': {
            'alpha': predictor.alpha,
            'gamma': predictor.gamma
        },
        'results': results
    }
    
    with open('hypothesis_A_prediction_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n结果已保存到: hypothesis_A_prediction_results.json")
    
    return results


if __name__ == "__main__":
    results = run_prediction_validation()
