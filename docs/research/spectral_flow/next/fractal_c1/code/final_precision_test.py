"""
最终精度测试
Final Precision Test

使用优化分形生成器 + 稳健c1提取器
目标: 验证 c1 = 0.250 ± 0.005
"""

import numpy as np
from optimized_fractal_generator import OptimizedFractalGenerator
from fractal_laplacian import FractalLaplacian
from robust_c1_extractor import RobustC1Extractor
import json
from datetime import datetime


def compute_spectral_dimension_for_points(points: np.ndarray, 
                                           n_eigenvalues: int = 100) -> tuple:
    """
    计算点集的谱维度
    
    Returns:
        (ell_values, d_s_values) 或 (None, None) 如果失败
    """
    fl = FractalLaplacian(dimension=points.shape[1])
    
    try:
        # 构建拉普拉斯
        L = fl.construct_graph_laplacian(points, epsilon=None)
        
        # 计算谱维度
        t_vals, d_s = fl.compute_spectral_dimension(
            L,
            t_range=np.logspace(-2, 2, 80),
            n_eigenvalues=n_eigenvalues
        )
        
        # 转换为长度尺度
        ell_vals = np.sqrt(t_vals)
        
        return ell_vals, d_s
        
    except Exception as e:
        print(f"    计算失败: {e}")
        return None, None


def run_precision_test(n_samples: int = 50, n_points: int = 1500):
    """
    运行精度测试
    
    Args:
        n_samples: 样本数
        n_points: 每样本点数
    """
    print("=" * 70)
    print("最终精度测试 - c1 = 1/4 验证")
    print(f"样本: {n_samples} x {n_points} 点")
    print("=" * 70)
    
    ofg = OptimizedFractalGenerator(dimension=4, c1=0.25)
    extractor = RobustC1Extractor(true_c1=0.25)
    
    # 测试不同生成方法
    methods = {
        'dimension_cascade': lambda: ofg.generate_dimension_cascade(
            n_points, ell_min=0.0001, ell_max=1000.0
        ),
        'hierarchical': lambda: ofg.generate_hierarchical_fractal(n_points, 8),
        'anisotropic': lambda: ofg.generate_anisotropic_fractal(n_points),
        'shell_structure': lambda: ofg.generate_shell_structure(n_points, 30)
    }
    
    all_results = {}
    
    for method_name, generator in methods.items():
        print(f"\n{'='*70}")
        print(f"方法: {method_name}")
        print(f"{'='*70}")
        
        c1_values = []
        d_max_values = []
        quality_values = []
        d_s_ranges = []
        
        for i in range(n_samples):
            if i % 10 == 0:
                print(f"  进度: {i}/{n_samples}")
            
            np.random.seed(i + 100)  # 可重复但不同的种子
            
            # 生成分形
            points = generator()
            
            # 计算谱维度
            ell_vals, d_s_vals = compute_spectral_dimension_for_points(
                points, n_eigenvalues=min(100, len(points)//4)
            )
            
            if ell_vals is None:
                continue
            
            # 提取c1
            result = extractor.extract_robust(ell_vals, d_s_vals, combine_methods=True)
            
            if 'c1' in result:
                c1_values.append(result['c1'])
                d_s_ranges.append(result.get('d_s_range', d_s_vals.max() - d_s_vals.min()))
                
                # 获取第一个方法的结果用于d_max
                ind_results = result.get('individual_results', {})
                if ind_results:
                    first = list(ind_results.values())[0]
                    d_max_values.append(first.get('d_max', np.nan))
                    quality_values.append(first.get('quality', 0))
        
        # 统计分析
        c1_values = np.array(c1_values)
        valid_mask = (c1_values > 0) & (c1_values < 1) & ~np.isnan(c1_values)
        valid_c1 = c1_values[valid_mask]
        
        if len(valid_c1) == 0:
            print(f"\n❌ 没有有效结果")
            all_results[method_name] = {'error': 'No valid results'}
            continue
        
        # 统计量
        mean_c1 = np.mean(valid_c1)
        median_c1 = np.median(valid_c1)
        std_c1 = np.std(valid_c1)
        sem_c1 = std_c1 / np.sqrt(len(valid_c1))
        
        # 与理论值的比较
        bias = mean_c1 - 0.25
        bias_pct = abs(bias) / 0.25 * 100
        
        # 是否在目标范围内
        within_target = abs(bias) < 0.005  # ±0.005
        within_10pct = bias_pct < 10
        within_20pct = bias_pct < 20
        
        summary = {
            'method': method_name,
            'n_samples': n_samples,
            'successful': len(valid_c1),
            'mean_c1': float(mean_c1),
            'median_c1': float(median_c1),
            'std_c1': float(std_c1),
            'sem_c1': float(sem_c1),
            'min_c1': float(np.min(valid_c1)),
            'max_c1': float(np.max(valid_c1)),
            'ci_95': (float(mean_c1 - 1.96*sem_c1), float(mean_c1 + 1.96*sem_c1)),
            'bias': float(bias),
            'bias_percent': float(bias_pct),
            'within_target_0.005': bool(within_target),
            'within_10_percent': bool(within_10pct),
            'within_20_percent': bool(within_20pct),
            'mean_d_max': float(np.mean(d_max_values)) if d_max_values else None,
            'mean_quality': float(np.mean(quality_values)) if quality_values else None,
            'mean_d_s_range': float(np.mean(d_s_ranges)) if d_s_ranges else None,
            'all_c1': valid_c1.tolist()
        }
        
        print(f"\n📊 结果统计:")
        print(f"  成功样本: {summary['successful']}/{n_samples}")
        print(f"  c1 (均值): {summary['mean_c1']:.6f}")
        print(f"  c1 (中位数): {summary['median_c1']:.6f}")
        print(f"  标准差: {summary['std_c1']:.6f}")
        print(f"  标准误: {summary['sem_c1']:.6f}")
        print(f"  95% CI: [{summary['ci_95'][0]:.6f}, {summary['ci_95'][1]:.6f}]")
        print(f"  范围: [{summary['min_c1']:.6f}, {summary['max_c1']:.6f}]")
        
        print(f"\n📈 精度评估:")
        print(f"  偏差: {summary['bias']:.6f} ({summary['bias_percent']:.2f}%)")
        print(f"  目标 (±0.005): {'✓ YES' if within_target else '✗ NO'}")
        print(f"  < 10% 偏差: {'✓ YES' if within_10pct else '✗ NO'}")
        print(f"  < 20% 偏差: {'✓ YES' if within_20pct else '✗ NO'}")
        
        print(f"\n📐 其他指标:")
        print(f"  平均 d_max: {summary['mean_d_max']:.2f}" if summary['mean_d_max'] else "  平均 d_max: N/A")
        print(f"  平均质量: {summary['mean_quality']:.3f}" if summary['mean_quality'] else "  平均质量: N/A")
        print(f"  平均 d_s 范围: {summary['mean_d_s_range']:.2f}" if summary['mean_d_s_range'] else "  平均 d_s 范围: N/A")
        
        all_results[method_name] = summary
    
    # 汇总报告
    print("\n" + "=" * 70)
    print("📋 最终汇总报告")
    print("=" * 70)
    
    print(f"\n{'方法':<20} | {'c1 均值':>10} | {'偏差%':>8} | {'目标(±0.005)':>12}")
    print(f"{'-'*20}-+-{'-'*10}-+-{'-'*8}-+-{'-'*12}")
    
    valid_results = {k: v for k, v in all_results.items() if 'error' not in v}
    
    for name, result in valid_results.items():
        status = '✓' if result['within_target_0.005'] else ('~' if result['within_10_percent'] else '✗')
        print(f"{name:<20} | {result['mean_c1']:10.6f} | "
              f"{result['bias_percent']:8.2f} | {status:>12}")
    
    if valid_results:
        # 找出最佳方法
        best = min(valid_results.items(), key=lambda x: abs(x[1]['bias']))
        print(f"\n🏆 最佳方法: {best[0]}")
        print(f"   c1 = {best[1]['mean_c1']:.6f} ± {best[1]['sem_c1']:.6f}")
        print(f"   偏差: {best[1]['bias']:.6f} ({best[1]['bias_percent']:.2f}%)")
        print(f"   达到目标精度 (±0.005): {'✓ YES' if best[1]['within_target_0.005'] else '✗ NO'}")
        
        # 总体结论
        print(f"\n{'='*70}")
        if best[1]['within_target_0.005']:
            print("🎉 成功! 达到目标精度 c1 = 0.250 ± 0.005")
        elif best[1]['within_10_percent']:
            print("🟡 良好! 偏差 < 10%，接近目标")
        else:
            print("⚠️ 需要进一步优化以达到目标精度")
        print(f"{'='*70}")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"../data/precision_test_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        save_data = {k: {key: val for key, val in v.items() if key != 'all_c1'}
                     for k, v in valid_results.items()}
        json.dump({
            'timestamp': timestamp,
            'target_c1': 0.25,
            'tolerance': 0.005,
            'results': save_data
        }, f, indent=2)
    
    print(f"\n💾 结果已保存: {output_file}")
    
    return all_results


if __name__ == "__main__":
    # 运行测试 (使用较小样本快速测试)
    results = run_precision_test(n_samples=20, n_points=800)
    
    print("\n" + "=" * 70)
    print("提示: 使用更多样本获得更精确结果")
    print("命令: python final_precision_test.py (修改n_samples=100)")
    print("=" * 70)
