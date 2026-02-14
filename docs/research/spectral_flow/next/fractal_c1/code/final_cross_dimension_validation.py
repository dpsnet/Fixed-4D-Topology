"""
最终跨维度验证
Final Cross-Dimension Validation

使用维度特定生成器和提取器进行验证
目标: 每个维度偏差 < 20%
"""

import numpy as np
from dimension_specific_fractal import DimensionSpecificFractalGenerator
from dimension_specific_extractor import DimensionSpecificExtractor
import json
from datetime import datetime


class FinalCrossDimensionValidator:
    """
    最终跨维度验证器
    """
    
    def __init__(self):
        self.results = {}
    
    def validate_dimension(self, dimension: int, n_samples: int = 15) -> dict:
        """
        验证特定维度
        
        Args:
            dimension: 空间维度
            n_samples: 样本数
        """
        print(f"\n{'='*70}")
        print(f"验证 {dimension} 维空间")
        print(f"理论 c1 = 1/{dimension} = {1.0/dimension:.6f}")
        print(f"目标: 偏差 < 20%")
        print(f"{'='*70}")
        
        # 创建生成器和提取器
        gen = DimensionSpecificFractalGenerator(dimension=dimension)
        extractor = DimensionSpecificExtractor(dimension=dimension)
        
        c1_values = []
        qualities = []
        
        for i in range(n_samples):
            if i % 5 == 0:
                print(f"  进度: {i}/{n_samples}")
            
            np.random.seed(i * 20 + dimension)
            
            # 交替使用两种生成方法
            if i % 2 == 0:
                points = gen.generate_dimension_optimized(n_points=500)
            else:
                points = gen.generate_three_region_fractal(n_points=500)
            
            # 提取c1
            result = extractor.extract_c1(points)
            
            if 'c1' in result and 0 < result['c1'] < 2:
                c1_values.append(result['c1'])
                qualities.append(result.get('quality', 0))
                
                status = "✓" if result.get('bias_percent', 100) < 20 else ""
                print(f"    样本{i+1}: c1 = {result['c1']:.4f} "
                      f"(偏差 {result.get('bias_percent', 0):.1f}%) {status}")
            else:
                print(f"    样本{i+1}: 失败 - {result.get('error', 'Unknown')[:40]}")
        
        # 统计分析
        if len(c1_values) == 0:
            return {'error': 'No valid c1 values', 'dimension': dimension}
        
        c1_values = np.array(c1_values)
        theory = 1.0 / dimension
        
        summary = {
            'dimension': dimension,
            'n_samples': n_samples,
            'successful': len(c1_values),
            'c1_theory': theory,
            'c1_mean': float(np.mean(c1_values)),
            'c1_median': float(np.median(c1_values)),
            'c1_std': float(np.std(c1_values)),
            'c1_sem': float(np.std(c1_values) / np.sqrt(len(c1_values))),
            'c1_min': float(np.min(c1_values)),
            'c1_max': float(np.max(c1_values)),
            'bias': float(np.mean(c1_values) - theory),
            'bias_percent': float(abs(np.mean(c1_values) - theory) / theory * 100),
            'mean_quality': float(np.mean(qualities)) if qualities else 0,
            'target_achieved': abs(np.mean(c1_values) - theory) / theory < 0.20,
        }
        
        # 打印结果
        print(f"\n  📊 统计结果:")
        print(f"    理论值: {summary['c1_theory']:.6f}")
        print(f"    提取均值: {summary['c1_mean']:.6f} ± {summary['c1_sem']:.6f}")
        print(f"    范围: [{summary['c1_min']:.4f}, {summary['c1_max']:.4f}]")
        print(f"    偏差: {summary['bias']:.6f} ({summary['bias_percent']:.2f}%)")
        print(f"    平均质量: {summary['mean_quality']:.3f}")
        
        if summary['target_achieved']:
            print(f"    ✅ 达到目标 (< 20% 偏差)")
        else:
            print(f"    ⚠️ 未达到目标 (≥ 20% 偏差)")
        
        return summary
    
    def run_full_validation(self, dimensions: list = [3, 4, 5]) -> dict:
        """
        运行完整验证
        """
        print("=" * 70)
        print("🎯 最终跨维度验证")
        print("=" * 70)
        print("\n理论预测:")
        for d in dimensions:
            print(f"  {d}维: c1 = 1/{d} = {1.0/d:.6f}")
        
        all_results = {}
        
        for dim in dimensions:
            result = self.validate_dimension(dim, n_samples=15)
            all_results[f"d{dim}"] = result
        
        # 汇总
        print("\n" + "=" * 70)
        print("📋 最终汇总")
        print("=" * 70)
        
        print(f"\n{'维度':>6} | {'理论c1':>10} | {'提取c1':>10} | {'偏差%':>8} | {'目标':>8}")
        print(f"{'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}-+-{'-'*8}")
        
        passed = 0
        total = 0
        
        for dim in dimensions:
            key = f"d{dim}"
            result = all_results[key]
            
            if 'error' not in result:
                total += 1
                theory = result['c1_theory']
                extracted = result['c1_mean']
                bias_pct = result['bias_percent']
                target = "✅ 通过" if result['target_achieved'] else "❌ 未通过"
                
                if result['target_achieved']:
                    passed += 1
                
                print(f"{dim:>6} | {theory:>10.4f} | {extracted:>10.4f} | "
                      f"{bias_pct:>8.2f} | {target:>8}")
        
        # 线性关系验证
        valid_results = [all_results[f"d{d}"] for d in dimensions 
                        if 'error' not in all_results[f"d{d}"]]
        
        if len(valid_results) >= 2:
            print(f"\n📈 线性关系: c1 ∝ 1/d")
            
            dims = np.array([r['dimension'] for r in valid_results])
            c1_means = np.array([r['c1_mean'] for r in valid_results])
            inv_dims = 1.0 / dims
            
            # 拟合 c1 = k * (1/d)
            k = np.sum(c1_means * inv_dims) / np.sum(inv_dims ** 2)
            
            print(f"  拟合: c1 = {k:.4f} * (1/d)")
            print(f"  理论: c1 = 1.0000 * (1/d)")
            print(f"  斜率偏差: {abs(k - 1.0) * 100:.1f}%")
            
            if abs(k - 1.0) < 0.15:
                print(f"\n  ✅ 强支持 c1 = 1/d 猜想!")
            elif abs(k - 1.0) < 0.30:
                print(f"\n  🟡 中等支持")
            else:
                print(f"\n  ⚠️ 需要更多优化")
        
        print(f"\n{'='*70}")
        print(f"结果: {passed}/{total} 个维度达到目标 (< 20% 偏差)")
        print(f"{'='*70}")
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"../data/final_cross_dim_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            save_data = {k: v for k, v in all_results.items() if 'error' not in v}
            json.dump({
                'timestamp': timestamp,
                'target': 'bias < 20%',
                'results': save_data
            }, f, indent=2)
        
        print(f"\n💾 已保存: {output_file}")
        
        return all_results


if __name__ == "__main__":
    validator = FinalCrossDimensionValidator()
    results = validator.run_full_validation(dimensions=[3, 4, 5])
