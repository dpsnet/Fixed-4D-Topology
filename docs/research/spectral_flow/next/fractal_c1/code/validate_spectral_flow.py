"""
谱维度流验证脚本
Validation of Spectral Dimension Flow in Generated Fractals

目标: 使用改进的分形生成器验证 c1 = 1/4 提取精度
"""

import numpy as np
from spectral_flow_fractal import SpectralFlowFractal
from fractal_laplacian import FractalLaplacian
import json
from datetime import datetime


class SpectralFlowValidator:
    """
    谱维度流验证器
    
    验证生成的分形是否具有正确的谱维度流特征
    """
    
    def __init__(self, true_c1: float = 0.25):
        self.true_c1 = true_c1
        
    def validate_fractal(self, points: np.ndarray, 
                         method: str = 'laplacian') -> dict:
        """
        验证单个分形样本
        
        Returns:
            验证结果字典
        """
        fl = FractalLaplacian(dimension=points.shape[1])
        
        # 构建拉普拉斯
        try:
            L = fl.construct_graph_laplacian(points, epsilon=None)
        except Exception as e:
            return {'error': f'Laplacian failed: {e}'}
        
        # 计算谱维度
        try:
            t_vals, d_s = fl.compute_spectral_dimension(
                L, n_eigenvalues=min(50, len(points)//4)
            )
        except Exception as e:
            return {'error': f'Spectral dimension failed: {e}'}
        
        # 检查谱维度范围
        d_s_min = np.min(d_s)
        d_s_max = np.max(d_s)
        d_s_range = d_s_max - d_s_min
        
        # 提取c1
        result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
        
        # 添加额外信息
        result['d_s_min'] = float(d_s_min)
        result['d_s_max'] = float(d_s_max)
        result['d_s_range'] = float(d_s_range)
        result['expected_range'] = 2.0  # 期望从4到2
        result['range_quality'] = min(d_s_range / 2.0, 1.0)
        
        return result
    
    def batch_validate(self, fractal_generator: SpectralFlowFractal,
                       n_samples: int = 50,
                       n_points: int = 300,
                       fractal_type: str = 'layered') -> dict:
        """
        批量验证分形样本
        
        Args:
            fractal_generator: 分形生成器
            n_samples: 样本数量
            n_points: 每样本点数
            fractal_type: 分形类型
            
        Returns:
            统计验证结果
        """
        print(f"批量验证: {n_samples} 样本 x {n_points} 点 ({fractal_type})")
        
        results = []
        
        for i in range(n_samples):
            if i % 10 == 0:
                print(f"  进度: {i}/{n_samples}")
            
            # 生成不同类型的分形
            if fractal_type == 'layered':
                points, _, _ = fractal_generator.generate_layered_fractal(n_points)
            elif fractal_type == 'ifs':
                points = fractal_generator.generate_ifs_fractal(n_points)
            elif fractal_type == 'smooth':
                points = fractal_generator.generate_dimension_transition_fractal(
                    n_points, transition_type='smooth'
                )
            elif fractal_type == 'quantum':
                points = fractal_generator.generate_quantum_spacetime_fractal(n_points)
            else:
                points = fractal_generator.generate_layered_fractal(n_points)
            
            # 验证
            result = self.validate_fractal(points)
            
            if 'error' not in result and not np.isnan(result.get('c1', np.nan)):
                results.append(result)
        
        # 统计分析
        if len(results) == 0:
            return {'error': 'No valid results'}
        
        c1_values = [r['c1'] for r in results if 'c1' in r]
        quality_values = [r['quality'] for r in results if 'quality' in r]
        range_values = [r['d_s_range'] for r in results if 'd_s_range' in r]
        
        c1_values = np.array(c1_values)
        
        # 过滤异常值 (c1应在合理范围)
        valid_mask = (c1_values > 0) & (c1_values < 1.0)
        valid_c1 = c1_values[valid_mask]
        
        if len(valid_c1) == 0:
            return {'error': 'No valid c1 values'}
        
        summary = {
            'fractal_type': fractal_type,
            'n_samples': n_samples,
            'successful': len(valid_c1),
            'mean_c1': float(np.mean(valid_c1)),
            'std_c1': float(np.std(valid_c1)),
            'sem_c1': float(np.std(valid_c1) / np.sqrt(len(valid_c1))),
            'min_c1': float(np.min(valid_c1)),
            'max_c1': float(np.max(valid_c1)),
            'true_c1': self.true_c1,
            'bias': float(np.mean(valid_c1) - self.true_c1),
            'mean_quality': float(np.mean(quality_values)) if quality_values else 0,
            'mean_d_s_range': float(np.mean(range_values)) if range_values else 0,
            'all_c1': valid_c1.tolist()
        }
        
        return summary
    
    def print_validation_report(self, summary: dict):
        """打印验证报告"""
        print("\n" + "=" * 70)
        print(f"谱维度流验证报告 - {summary.get('fractal_type', 'Unknown')}")
        print("=" * 70)
        
        if 'error' in summary:
            print(f"\n❌ 错误: {summary['error']}")
            return
        
        print(f"\n📊 样本统计:")
        print(f"   总样本: {summary['n_samples']}")
        print(f"   成功验证: {summary['successful']}")
        
        print(f"\n🎯 c1 提取结果:")
        print(f"   理论值: {summary['true_c1']:.6f}")
        print(f"   提取均值: {summary['mean_c1']:.6f}")
        print(f"   标准差: {summary['std_c1']:.6f}")
        print(f"   标准误: {summary['sem_c1']:.6f}")
        print(f"   范围: [{summary['min_c1']:.6f}, {summary['max_c1']:.6f}]")
        
        print(f"\n📈 质量评估:")
        print(f"   偏差 (提取-理论): {summary['bias']:.6f}")
        print(f"   平均拟合质量: {summary['mean_quality']:.4f}")
        print(f"   平均谱维度范围: {summary['mean_d_s_range']:.2f}")
        
        # 评估
        bias_pct = abs(summary['bias']) / summary['true_c1'] * 100
        if bias_pct < 10:
            grade = "✅ 优秀"
        elif bias_pct < 20:
            grade = "🟡 良好"
        else:
            grade = "🔴 需改进"
        
        print(f"\n{grade} - 偏差: {bias_pct:.1f}%")
        
        print("=" * 70)


def run_comprehensive_validation():
    """运行综合验证"""
    print("=" * 70)
    print("谱维度流分形综合验证")
    print("目标: 验证改进的分形生成器能否准确提取 c1 = 0.25")
    print("=" * 70)
    
    validator = SpectralFlowValidator(true_c1=0.25)
    sff = SpectralFlowFractal(dimension=4, c1=0.25)
    
    fractal_types = ['layered', 'ifs', 'smooth', 'quantum']
    all_results = {}
    
    for ft in fractal_types:
        print(f"\n{'='*70}")
        print(f"验证分形类型: {ft}")
        print(f"{'='*70}")
        
        summary = validator.batch_validate(
            sff, n_samples=30, n_points=250, fractal_type=ft
        )
        
        validator.print_validation_report(summary)
        all_results[ft] = summary
    
    # 汇总报告
    print("\n" + "=" * 70)
    print("汇总报告")
    print("=" * 70)
    
    print(f"\n{'分形类型':<12} | {'c1均值':>10} | {'偏差':>10} | {'质量':>8}")
    print(f"{'-'*12}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}")
    
    for ft, result in all_results.items():
        if 'error' not in result:
            print(f"{ft:<12} | {result['mean_c1']:10.4f} | "
                  f"{result['bias']:10.4f} | {result['mean_quality']:8.3f}")
    
    # 找出最佳方法
    valid_results = {k: v for k, v in all_results.items() 
                     if 'error' not in v}
    
    if valid_results:
        best_method = min(valid_results.items(), 
                         key=lambda x: abs(x[1]['bias']))
        print(f"\n✅ 最佳方法: {best_method[0]}")
        print(f"   c1 = {best_method[1]['mean_c1']:.4f} ± {best_method[1]['sem_c1']:.4f}")
        print(f"   偏差: {best_method[1]['bias']:.4f}")
    
    print("\n" + "=" * 70)
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"../data/validation_results_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        # 过滤掉numpy数组
        save_results = {}
        for k, v in all_results.items():
            if 'error' not in v:
                save_results[k] = {key: val for key, val in v.items() 
                                  if key != 'all_c1'}
        
        json.dump({
            'timestamp': timestamp,
            'true_c1': 0.25,
            'results': save_results
        }, f, indent=2)
    
    print(f"\n结果已保存: {output_file}")
    
    return all_results


if __name__ == "__main__":
    results = run_comprehensive_validation()
