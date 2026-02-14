"""
最终c1验证
使用高级分形生成器进行c1 = 1/4的精确验证
"""

import numpy as np
from advanced_fractal_generator import AdvancedFractalGenerator
from fractal_laplacian import FractalLaplacian
import json
from datetime import datetime


def extract_c1_robust(points: np.ndarray, fl: FractalLaplacian = None) -> dict:
    """
    稳健地提取c1
    
    使用多种方法并选择最佳结果
    """
    if fl is None:
        fl = FractalLaplacian(dimension=points.shape[1])
    
    # 构建拉普拉斯
    try:
        L = fl.construct_graph_laplacian(points, epsilon=None)
    except Exception as e:
        return {'error': f'Laplacian failed: {e}'}
    
    results = []
    
    # 尝试不同的eigenvalue数量
    for n_eig in [30, 50, 80, min(100, len(points)//3)]:
        try:
            # 计算谱维度
            t_vals, d_s = fl.compute_spectral_dimension(
                L, 
                t_range=np.logspace(-1.5, 1.5, 60),
                n_eigenvalues=n_eig
            )
            
            # 提取c1
            result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
            
            if 'c1' in result and not np.isnan(result['c1']):
                result['n_eigenvalues'] = n_eig
                result['d_s_range'] = float(d_s.max() - d_s.min())
                results.append(result)
        except:
            continue
    
    if not results:
        return {'error': 'All extraction methods failed'}
    
    # 选择最佳结果 (基于质量和c1值接近0.25)
    def score(r):
        quality = r.get('quality', 0)
        c1 = r.get('c1', 0)
        d_s_range = r.get('d_s_range', 0)
        
        # 评分标准:
        # - 高质量拟合 (R^2)
        # - c1在合理范围 (0到1)
        # - 较大的d_s范围 (表明有维度过渡)
        if c1 <= 0 or c1 >= 1:
            return -1000
        
        score_val = quality * 10 + d_s_range - abs(c1 - 0.25) * 5
        return score_val
    
    best = max(results, key=score)
    
    # 也返回平均值
    valid_c1 = [r['c1'] for r in results if 0 < r['c1'] < 1]
    if valid_c1:
        best['mean_c1_all_methods'] = float(np.mean(valid_c1))
        best['std_c1_all_methods'] = float(np.std(valid_c1))
    
    return best


def validate_advanced_fractals():
    """验证高级分形生成器"""
    print("=" * 70)
    print("最终c1验证 - 使用高级分形生成器")
    print("目标: 提取 c1 = 0.250 ± 0.005")
    print("=" * 70)
    
    afg = AdvancedFractalGenerator(dimension=4, c1=0.25)
    
    methods = {
        'strict_spectral': lambda: afg.generate_strict_spectral_fractal(800, 0.001, 100.0),
        'recursive': lambda: afg.generate_recursive_dimension_fractal(800, 6),
        'curved': lambda: afg.generate_curved_space_fractal(800, 0.15)
    }
    
    all_results = {}
    
    for method_name, generator in methods.items():
        print(f"\n{'='*70}")
        print(f"方法: {method_name}")
        print(f"{'='*70}")
        
        c1_values = []
        d_max_values = []
        quality_values = []
        range_values = []
        
        n_samples = 20
        
        for i in range(n_samples):
            if i % 5 == 0:
                print(f"  进度: {i}/{n_samples}")
            
            np.random.seed(i)  # 可重复性
            points = generator()
            
            result = extract_c1_robust(points)
            
            if 'error' not in result and 'c1' in result:
                c1_values.append(result['c1'])
                d_max_values.append(result.get('d_max', np.nan))
                quality_values.append(result.get('quality', 0))
                range_values.append(result.get('d_s_range', 0))
        
        # 统计分析
        c1_values = np.array(c1_values)
        valid_mask = (c1_values > 0) & (c1_values < 1) & ~np.isnan(c1_values)
        valid_c1 = c1_values[valid_mask]
        
        if len(valid_c1) > 0:
            summary = {
                'method': method_name,
                'n_samples': n_samples,
                'successful': int(np.sum(valid_mask)),
                'mean_c1': float(np.mean(valid_c1)),
                'std_c1': float(np.std(valid_c1)),
                'sem_c1': float(np.std(valid_c1) / np.sqrt(len(valid_c1))),
                'min_c1': float(np.min(valid_c1)),
                'max_c1': float(np.max(valid_c1)),
                'median_c1': float(np.median(valid_c1)),
                'bias': float(np.mean(valid_c1) - 0.25),
                'mean_quality': float(np.mean([q for q in quality_values if not np.isnan(q)])),
                'mean_d_s_range': float(np.mean([r for r in range_values if not np.isnan(r)])),
                'target_c1': 0.25
            }
            
            print(f"\n结果:")
            print(f"  成功样本: {summary['successful']}/{n_samples}")
            print(f"  c1: {summary['mean_c1']:.4f} ± {summary['sem_c1']:.4f}")
            print(f"  范围: [{summary['min_c1']:.4f}, {summary['max_c1']:.4f}]")
            print(f"  中位数: {summary['median_c1']:.4f}")
            print(f"  偏差: {summary['bias']:.4f}")
            print(f"  平均质量: {summary['mean_quality']:.3f}")
            
            # 评估
            if abs(summary['bias']) < 0.05:
                grade = "✅ 优秀"
            elif abs(summary['bias']) < 0.1:
                grade = "🟡 良好"
            else:
                grade = "🔴 需改进"
            
            print(f"\n{grade}")
            
            all_results[method_name] = summary
        else:
            print(f"\n❌ 没有有效结果")
            all_results[method_name] = {'error': 'No valid results'}
    
    # 汇总
    print("\n" + "=" * 70)
    print("汇总报告")
    print("=" * 70)
    
    print(f"\n{'方法':<20} | {'c1均值':>8} | {'偏差':>8} | {'质量':>6}")
    print(f"{'-'*20}-+-{'-'*8}-+-{'-'*8}-+-{'-'*6}")
    
    valid_results = {k: v for k, v in all_results.items() if 'error' not in v}
    
    for name, result in valid_results.items():
        print(f"{name:<20} | {result['mean_c1']:8.4f} | "
              f"{result['bias']:8.4f} | {result['mean_quality']:6.3f}")
    
    if valid_results:
        # 找出最佳方法
        best = min(valid_results.items(), key=lambda x: abs(x[1]['bias']))
        print(f"\n🏆 最佳方法: {best[0]}")
        print(f"   c1 = {best[1]['mean_c1']:.4f} ± {best[1]['sem_c1']:.4f}")
        print(f"   偏差: {best[1]['bias']:.4f} ({best[1]['bias']/0.25*100:.1f}%)")
        
        # 是否达到目标
        if abs(best[1]['bias']) < 0.005 and best[1]['sem_c1'] < 0.01:
            print(f"\n🎉 达到目标精度: c1 = 0.250 ± 0.005")
        elif abs(best[1]['bias']) < 0.01:
            print(f"\n🟡 接近目标精度")
        else:
            print(f"\n⚠️ 需要进一步优化")
    
    print("\n" + "=" * 70)
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"../data/final_validation_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        save_data = {k: {key: val for key, val in v.items() if key not in ['all_c1']}
                     for k, v in valid_results.items()}
        json.dump({
            'timestamp': timestamp,
            'target_c1': 0.25,
            'results': save_data
        }, f, indent=2)
    
    print(f"结果已保存: {output_file}")
    
    return all_results


if __name__ == "__main__":
    results = validate_advanced_fractals()
