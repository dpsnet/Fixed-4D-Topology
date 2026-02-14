"""
跨维度验证
Cross-Dimension Validation

验证核心猜想: c1 = 1/d_f^max 在不同维度是否成立

测试:
- 3维空间: c1 = 1/3 ≈ 0.333
- 4维空间: c1 = 1/4 = 0.250  
- 5维空间: c1 = 1/5 = 0.200
- 6维空间: c1 = 1/6 ≈ 0.167

如果猜想正确，提取的c1应该与1/dimension成正比
"""

import numpy as np
from optimized_fractal_generator import OptimizedFractalGenerator
from fractal_laplacian import FractalLaplacian
from robust_c1_extractor import RobustC1Extractor
import json
from datetime import datetime


class CrossDimensionValidator:
    """
    跨维度验证器
    
    验证 c1 = 1/d_f^max 在不同维度是否成立
    """
    
    def __init__(self):
        self.results = {}
        
    def validate_dimension(self, dimension: int, n_samples: int = 10,
                          n_points: int = 600) -> dict:
        """
        验证特定维度的c1
        
        Args:
            dimension: 空间维度 (3, 4, 5, 6)
            n_samples: 样本数
            n_points: 每样本点数
            
        Returns:
            验证结果
        """
        print(f"\n{'='*70}")
        print(f"验证 {dimension} 维空间")
        print(f"理论 c1 = 1/{dimension} = {1.0/dimension:.6f}")
        print(f"{'='*70}")
        
        # 根据维度设置参数
        d_min = 2.0  # 最小维度固定为2
        d_max = float(dimension)
        c1_theory = 1.0 / dimension
        
        # 创建生成器和提取器
        ofg = OptimizedFractalGenerator(dimension=dimension, c1=c1_theory)
        extractor = RobustC1Extractor(true_c1=c1_theory)
        
        c1_values = []
        d_s_ranges = []
        
        for i in range(n_samples):
            if i % 3 == 0:
                print(f"  进度: {i}/{n_samples}")
            
            np.random.seed(i * 100 + dimension)
            
            # 生成分形
            try:
                points = ofg.generate_dimension_cascade(
                    n_points=n_points,
                    ell_min=0.001,
                    ell_max=100.0,
                    ell_0=1.0
                )
                
                # 计算谱维度
                fl = FractalLaplacian(dimension=dimension)
                L = fl.construct_graph_laplacian(points, epsilon=None)
                
                t_vals, d_s = fl.compute_spectral_dimension(
                    L,
                    t_range=np.logspace(-1.5, 1.5, 50),
                    n_eigenvalues=min(40, len(points)//5)
                )
                
                ell_vals = np.sqrt(t_vals)
                d_s_range = d_s.max() - d_s.min()
                
                # 提取c1
                result = extractor.extract_weighted_fit(ell_vals, d_s)
                
                if 'c1' in result and 0 < result['c1'] < 2:
                    c1_values.append(result['c1'])
                    d_s_ranges.append(d_s_range)
                    print(f"    样本{i+1}: c1 = {result['c1']:.4f}, "
                          f"d_s范围 = [{d_s.min():.2f}, {d_s.max():.2f}]")
                
            except Exception as e:
                print(f"    样本{i+1}: 失败 - {str(e)[:50]}")
                continue
        
        # 统计分析
        if len(c1_values) == 0:
            return {'error': 'No valid c1 extracted', 'dimension': dimension}
        
        c1_values = np.array(c1_values)
        
        summary = {
            'dimension': dimension,
            'n_samples': n_samples,
            'successful': len(c1_values),
            'c1_theory': c1_theory,
            'c1_mean': float(np.mean(c1_values)),
            'c1_median': float(np.median(c1_values)),
            'c1_std': float(np.std(c1_values)),
            'c1_sem': float(np.std(c1_values) / np.sqrt(len(c1_values))),
            'c1_min': float(np.min(c1_values)),
            'c1_max': float(np.max(c1_values)),
            'bias': float(np.mean(c1_values) - c1_theory),
            'bias_percent': float(abs(np.mean(c1_values) - c1_theory) / c1_theory * 100),
            'all_c1': c1_values.tolist()
        }
        
        # 评估
        print(f"\n📊 {dimension}维结果:")
        print(f"  理论c1: {summary['c1_theory']:.6f}")
        print(f"  提取c1: {summary['c1_mean']:.6f} ± {summary['c1_sem']:.6f}")
        print(f"  偏差: {summary['bias']:.6f} ({summary['bias_percent']:.2f}%)")
        print(f"  成功样本: {summary['successful']}/{n_samples}")
        
        # 验证是否接近理论值
        if summary['bias_percent'] < 10:
            status = "✅ 验证通过"
        elif summary['bias_percent'] < 20:
            status = "🟡 接近"
        else:
            status = "⚠️ 偏差较大"
        
        print(f"  状态: {status}")
        
        return summary
    
    def run_cross_dimension_test(self, dimensions: list = [3, 4, 5],
                                  n_samples: int = 10) -> dict:
        """
        运行跨维度测试
        
        Args:
            dimensions: 要测试的维度列表
            n_samples: 每维度样本数
            
        Returns:
            所有维度的结果
        """
        print("=" * 70)
        print("跨维度验证 - c1 = 1/d_f^max")
        print("=" * 70)
        print("\n核心猜想验证:")
        print("  如果 c1 = 1/d_f^max 成立，则:")
        for d in dimensions:
            print(f"    {d}维空间: c1 = 1/{d} = {1.0/d:.6f}")
        
        all_results = {}
        
        for dim in dimensions:
            result = self.validate_dimension(dim, n_samples=n_samples)
            all_results[f"d{dim}"] = result
        
        # 汇总分析
        print("\n" + "=" * 70)
        print("📋 跨维度汇总")
        print("=" * 70)
        
        print(f"\n{'维度':>6} | {'理论c1':>10} | {'提取c1':>10} | {'偏差%':>8} | {'状态':>10}")
        print(f"{'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}-+-{'-'*10}")
        
        valid_results = []
        for dim_key, result in all_results.items():
            if 'error' not in result:
                dim = result['dimension']
                theory = result['c1_theory']
                extracted = result['c1_mean']
                bias_pct = result['bias_percent']
                
                if bias_pct < 10:
                    status = "✅ 通过"
                elif bias_pct < 20:
                    status = "🟡 接近"
                else:
                    status = "⚠️ 偏差"
                
                print(f"{dim:>6} | {theory:>10.6f} | {extracted:>10.6f} | "
                      f"{bias_pct:>8.2f} | {status:>10}")
                
                valid_results.append(result)
        
        # 验证线性关系 c1 ∝ 1/d
        if len(valid_results) >= 2:
            print(f"\n📈 线性关系验证: c1 ∝ 1/d")
            
            dims = np.array([r['dimension'] for r in valid_results])
            c1_means = np.array([r['c1_mean'] for r in valid_results])
            inv_dims = 1.0 / dims
            
            # 拟合 c1 = k * (1/d)
            # 应该 k ≈ 1
            A = np.vstack([inv_dims, np.ones(len(inv_dims))]).T
            k, b = np.linalg.lstsq(A, c1_means, rcond=None)[0]
            
            print(f"  拟合: c1 = {k:.4f} * (1/d) + {b:.6f}")
            print(f"  斜率k = {k:.4f} (理论值 = 1.0)")
            print(f"  截距b = {b:.6f} (理论值 = 0.0)")
            
            # 计算R^2
            y_pred = k * inv_dims + b
            ss_res = np.sum((c1_means - y_pred)**2)
            ss_tot = np.sum((c1_means - np.mean(c1_means))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            print(f"  R² = {r_squared:.4f}")
            
            if abs(k - 1.0) < 0.1 and r_squared > 0.9:
                print(f"\n  🎉 强支持: c1 = 1/d_f^max 猜想!")
            elif abs(k - 1.0) < 0.2:
                print(f"\n  🟡 中等支持: 需要更多数据")
            else:
                print(f"\n  ⚠️ 线性关系不明显")
        
        print("\n" + "=" * 70)
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"../data/cross_dimension_test_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            save_data = {k: {key: val for key, val in v.items() if key != 'all_c1'}
                        for k, v in all_results.items() if 'error' not in v}
            json.dump({
                'timestamp': timestamp,
                'conjecture': 'c1 = 1/d_f^max',
                'results': save_data
            }, f, indent=2)
        
        print(f"\n💾 结果已保存: {output_file}")
        
        return all_results


if __name__ == "__main__":
    # 运行跨维度测试
    validator = CrossDimensionValidator()
    
    # 测试3, 4, 5维
    results = validator.run_cross_dimension_test(
        dimensions=[3, 4, 5],
        n_samples=8  # 每维度样本数
    )
    
    print("\n" + "=" * 70)
    print("提示: 使用更多样本(n_samples=20+)获得更精确结果")
    print("=" * 70)
