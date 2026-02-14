"""
普适系数 c1 提取器
Universal Coefficient c1 Extractor

从分形数据中提取 c1 = 1/4 并验证核心猜想
"""

import numpy as np
from typing import Dict, List, Tuple
import json
from datetime import datetime
from fractal_laplacian import FractalLaplacian, FractalMeasure, verify_c1_conjecture
from random_fractal_generator import RandomFractalGenerator
import warnings


class C1Extractor:
    """
    c1 提取分析器
    
    任务:
    1. 从分形数据中提取谱维度流
    2. 拟合提取 c1
    3. 验证 c1 = 1/4 猜想
    4. 统计分析
    """
    
    def __init__(self, true_c1: float = 0.25):
        self.true_c1 = true_c1
        self.results = []
        
    def extract_from_fractal(self, points: np.ndarray, 
                             method: str = 'laplacian',
                             n_eigenvalues: int = 50) -> Dict:
        """
        从单个分形样本中提取 c1
        
        Args:
            points: 分形点集 (N, d)
            method: 提取方法 ('laplacian' 或 'box_counting')
            n_eigenvalues: 计算的 eigenvalue 数量
            
        Returns:
            提取结果字典
        """
        if method == 'laplacian':
            return self._extract_via_laplacian(points, n_eigenvalues)
        elif method == 'box_counting':
            return self._extract_via_box_counting(points)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _extract_via_laplacian(self, points: np.ndarray, 
                                n_eigenvalues: int) -> Dict:
        """使用拉普拉斯算子方法提取 c1"""
        
        fl = FractalLaplacian(dimension=points.shape[1])
        
        # 构建图拉普拉斯
        try:
            L = fl.construct_graph_laplacian(points, epsilon=None)
        except Exception as e:
            return {'error': f'Laplacian construction failed: {e}', 'c1': np.nan}
        
        # 计算谱维度
        try:
            t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=n_eigenvalues)
        except Exception as e:
            return {'error': f'Spectral dimension computation failed: {e}', 'c1': np.nan}
        
        # 提取 c1
        result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
        
        return result
    
    def _extract_via_box_counting(self, points: np.ndarray) -> Dict:
        """使用盒计数法提取 c1"""
        
        fm = FractalMeasure(c1=self.true_c1)
        
        # 计算盒计数维度
        eps_vals, d_f = fm.box_counting_dimension(points)
        
        # 从分形维度流中提取 c1
        # d_f(eps) = d_max - c1 / ln(eps/eps_0)
        
        valid_mask = (d_f > 1) & (d_f < 5) & (eps_vals > 0)
        eps_valid = eps_vals[valid_mask]
        d_f_valid = d_f[valid_mask]
        
        if len(eps_valid) < 5:
            return {'error': 'Insufficient data for box counting', 'c1': np.nan}
        
        # 拟合
        log_eps = np.log(eps_valid)
        x = 1.0 / log_eps
        y = d_f_valid
        
        # 线性拟合: y = d_max - c1 * x
        mask = np.abs(log_eps) > 0.1
        if np.sum(mask) < 5:
            mask = np.abs(log_eps) > 0.01
        
        x_fit = x[mask]
        y_fit = y[mask]
        
        A = np.vstack([x_fit, np.ones(len(x_fit))]).T
        try:
            c1_fit, d_max_fit = np.linalg.lstsq(A, y_fit, rcond=None)[0]
            c1_fit = -c1_fit
        except:
            return {'error': 'Fitting failed', 'c1': np.nan}
        
        # 计算 R^2
        y_pred = d_max_fit - c1_fit * x_fit
        ss_res = np.sum((y_fit - y_pred)**2)
        ss_tot = np.sum((y_fit - np.mean(y_fit))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        return {
            'c1': float(c1_fit),
            'd_max': float(d_max_fit),
            'quality': float(r_squared),
            'c1_error': abs(c1_fit - self.true_c1),
            'method': 'box_counting'
        }
    
    def analyze_dataset(self, fractal_data: List[np.ndarray],
                       method: str = 'laplacian') -> Dict:
        """
        分析整个分形数据集，统计验证 c1 = 1/4
        
        Args:
            fractal_data: 分形样本列表
            method: 提取方法
            
        Returns:
            统计分析结果
        """
        print(f"分析 {len(fractal_data)} 个分形样本...")
        
        all_c1 = []
        all_d_max = []
        all_quality = []
        errors = []
        
        for i, points in enumerate(fractal_data):
            if i % 10 == 0:
                print(f"  进度: {i}/{len(fractal_data)}")
            
            result = self.extract_from_fractal(points, method=method)
            
            if 'error' in result:
                errors.append((i, result['error']))
                continue
            
            if not np.isnan(result.get('c1', np.nan)):
                all_c1.append(result['c1'])
                all_d_max.append(result.get('d_max', np.nan))
                all_quality.append(result.get('quality', 0))
        
        # 统计分析
        all_c1 = np.array(all_c1)
        all_d_max = np.array(all_d_max)
        all_quality = np.array(all_quality)
        
        # 过滤异常值
        valid_mask = (all_c1 > 0) & (all_c1 < 1) & (all_quality > 0.1)
        valid_c1 = all_c1[valid_mask]
        
        if len(valid_c1) == 0:
            return {
                'error': 'No valid c1 extracted',
                'total_samples': len(fractal_data),
                'failed_samples': len(errors)
            }
        
        mean_c1 = np.mean(valid_c1)
        std_c1 = np.std(valid_c1)
        sem_c1 = std_c1 / np.sqrt(len(valid_c1))  # 标准误
        
        # 与理论值的偏差
        deviation = abs(mean_c1 - self.true_c1)
        n_sigma = deviation / sem_c1 if sem_c1 > 0 else np.inf
        
        # 假设检验 (c1 = 0.25)
        from scipy import stats
        t_stat, p_value = stats.ttest_1samp(valid_c1, self.true_c1)
        
        summary = {
            'total_samples': len(fractal_data),
            'successful_extractions': len(valid_c1),
            'failed_extractions': len(errors),
            'mean_c1': float(mean_c1),
            'std_c1': float(std_c1),
            'sem_c1': float(sem_c1),
            'ci_95': (float(mean_c1 - 1.96*sem_c1), float(mean_c1 + 1.96*sem_c1)),
            'true_c1': self.true_c1,
            'deviation_from_true': float(deviation),
            'n_sigma': float(n_sigma),
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'conjecture_verified': deviation < 2*sem_c1,  # 在2 sigma内
            'all_c1_values': valid_c1.tolist(),
            'mean_d_max': float(np.mean(all_d_max[valid_mask])) if len(all_d_max) > 0 else None,
            'mean_quality': float(np.mean(all_quality[valid_mask])) if len(all_quality) > 0 else None
        }
        
        return summary
    
    def print_report(self, summary: Dict):
        """打印分析报告"""
        print("\n" + "=" * 70)
        print("c1 = 1/4 猜想验证报告")
        print("=" * 70)
        
        if 'error' in summary:
            print(f"\n❌ 错误: {summary['error']}")
            return
        
        print(f"\n📊 样本统计:")
        print(f"   总样本数: {summary['total_samples']}")
        print(f"   成功提取: {summary['successful_extractions']}")
        print(f"   失败提取: {summary['failed_extractions']}")
        
        print(f"\n📈 c1 提取结果:")
        print(f"   提取的 c1: {summary['mean_c1']:.6f} ± {summary['sem_c1']:.6f}")
        print(f"   标准差: {summary['std_c1']:.6f}")
        print(f"   95% 置信区间: [{summary['ci_95'][0]:.6f}, {summary['ci_95'][1]:.6f}]")
        print(f"   理论值 c1: {summary['true_c1']:.6f}")
        
        print(f"\n✅ 验证结果:")
        print(f"   与理论值偏差: {summary['deviation_from_true']:.6f}")
        print(f"   n-sigma: {summary['n_sigma']:.2f}")
        print(f"   t-统计量: {summary['t_statistic']:.4f}")
        print(f"   p-值: {summary['p_value']:.4f}")
        
        if summary['conjecture_verified']:
            print(f"\n   🎉 结论: 猜想 c1 = 1/4 通过统计验证!")
        else:
            print(f"\n   ⚠️ 结论: 需要更多数据或改进提取方法")
        
        if summary['mean_d_max']:
            print(f"\n📐 分形维度:")
            print(f"   平均 d_max: {summary['mean_d_max']:.2f}")
            print(f"   平均拟合质量 R^2: {summary['mean_quality']:.4f}")
        
        print("=" * 70)
    
    def save_report(self, summary: Dict, filename: str):
        """保存报告到文件"""
        summary_save = {k: v for k, v in summary.items() if k != 'all_c1_values'}
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': summary_save
            }, f, indent=2)
        
        print(f"\n报告已保存到: {filename}")


def run_full_analysis(n_samples: int = 100, n_points: int = 300):
    """
    运行完整的 c1 提取分析
    
    Args:
        n_samples: 分形样本数量
        n_points: 每个样本的点数
    """
    print("=" * 70)
    print(f"c1 = 1/4 猜想完整验证分析")
    print(f"样本: {n_samples} x {n_points} 点")
    print("=" * 70)
    
    # 1. 首先验证核心猜想的一致性
    print("\n[1] 验证核心猜想一致性")
    conjecture_result = verify_c1_conjecture(d_f_max=4.0, d_f_min=2.0)
    print(f"   c1 = 1/d_f^max = {conjecture_result['c1_from_reciprocal']:.6f}")
    print(f"   c1 = (d_f^min/d_f^max)^2 = {conjecture_result['c1_from_ratio_squared']:.6f}")
    print(f"   两个猜想一致: {conjecture_result['conjectures_match']}")
    
    # 2. 生成测试数据
    print("\n[2] 生成分形数据集")
    generator = RandomFractalGenerator(dimension=4)
    
    fractal_data = []
    for i in range(n_samples):
        if i % 20 == 0:
            print(f"   生成进度: {i}/{n_samples}")
        
        # 混合使用不同类型的分形
        if i % 4 == 0:
            points = generator.generate_fractal_percolation(n_points, p=0.5 + 0.1*np.random.rand())
        elif i % 4 == 1:
            points = generator.generate_fractal_walk(n_points, alpha=0.4 + 0.2*np.random.rand())
        elif i % 4 == 2:
            points = generator.generate_spectral_fractal(n_points, c1=0.25)
        else:
            points = generator.generate_multifractal(n_points)
        
        fractal_data.append(points)
    
    print(f"   完成: 生成 {n_samples} 个分形样本")
    
    # 3. 分析数据集
    print("\n[3] 分析分形数据集 (拉普拉斯方法)")
    extractor = C1Extractor(true_c1=0.25)
    summary_lap = extractor.analyze_dataset(fractal_data, method='laplacian')
    extractor.print_report(summary_lap)
    
    # 4. 盒计数方法分析
    print("\n[4] 分析分形数据集 (盒计数方法)")
    summary_box = extractor.analyze_dataset(fractal_data, method='box_counting')
    extractor.print_report(summary_box)
    
    # 5. 保存结果
    print("\n[5] 保存分析结果")
    extractor.save_report(summary_lap, '../data/c1_analysis_laplacian.json')
    extractor.save_report(summary_box, '../data/c1_analysis_boxcounting.json')
    
    print("\n" + "=" * 70)
    print("分析完成!")
    print("=" * 70)
    
    return {
        'laplacian': summary_lap,
        'box_counting': summary_box
    }


if __name__ == "__main__":
    # 运行小规模测试
    print("运行小规模测试 (10样本)...")
    results = run_full_analysis(n_samples=10, n_points=200)
    
    print("\n" + "=" * 70)
    print("准备运行大规模分析 (100样本)...")
    print("在命令行运行: python c1_extractor.py --full")
    print("=" * 70)
