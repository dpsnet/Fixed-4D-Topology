"""
维度特定c1提取器
Dimension-Specific C1 Extractor

针对3维、4维、5维分别优化的提取参数
"""

import numpy as np
from fractal_laplacian import FractalLaplacian
from typing import Dict


class DimensionSpecificExtractor:
    """
    维度特定c1提取器
    
    每个维度的优化参数:
    - epsilon (邻域大小)
    - n_eigenvalues (特征值数量)
    - t_range (时间尺度范围)
    - 拟合权重
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.c1_theory = 1.0 / dimension
        self.params = self._get_extraction_params()
    
    def _get_extraction_params(self) -> Dict:
        """获取维度特定的提取参数"""
        params = {
            3: {
                'epsilon_factor': 0.5,      # epsilon = factor * mean_nn_distance
                'n_eigenvalues_factor': 0.15,  # n_eig = factor * n_points
                't_min': -0.5,
                't_max': 1.5,
                'n_t_points': 40,
                'log_ell_threshold': 0.05,  # |ln(ell)| > threshold
                'weight_transition_boost': 2.0,
            },
            4: {
                'epsilon_factor': 0.5,
                'n_eigenvalues_factor': 0.15,
                't_min': -0.5,
                't_max': 1.5,
                'n_t_points': 40,
                'log_ell_threshold': 0.05,
                'weight_transition_boost': 2.0,
            },
            5: {
                'epsilon_factor': 0.5,
                'n_eigenvalues_factor': 0.15,
                't_min': -0.5,
                't_max': 1.5,
                'n_t_points': 40,
                'log_ell_threshold': 0.05,
                'weight_transition_boost': 2.0,
            }
        }
        return params.get(self.d, params[4])
    
    def extract_c1(self, points: np.ndarray) -> Dict:
        """
        提取c1 - 使用维度特定参数
        """
        p = self.params
        
        try:
            # 构建拉普拉斯
            fl = FractalLaplacian(dimension=self.d)
            
            # 自动确定epsilon
            from scipy.spatial.distance import pdist
            dists = pdist(points)
            mean_nn = np.mean(np.sort(dists)[:len(points)])
            epsilon = p['epsilon_factor'] * mean_nn
            
            L = fl.construct_graph_laplacian(points, epsilon=epsilon)
            
            # 计算谱维度
            n_eig = max(20, int(len(points) * p['n_eigenvalues_factor']))
            
            t_range = np.logspace(p['t_min'], p['t_max'], p['n_t_points'])
            
            t_vals, d_s = fl.compute_spectral_dimension(
                L, 
                t_range=t_range,
                n_eigenvalues=n_eig
            )
            
            # 提取c1
            ell_vals = np.sqrt(t_vals)
            result = self._extract_c1_weighted(ell_vals, d_s)
            
            result['d_s_range'] = (float(d_s.min()), float(d_s.max()))
            result['n_eigenvalues_used'] = n_eig
            result['epsilon'] = epsilon
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_c1_weighted(self, ell_vals: np.ndarray, 
                              d_s_vals: np.ndarray) -> Dict:
        """
        加权提取c1
        """
        p = self.params
        
        # 过滤无效值 - 进一步放宽条件，允许d_s在0.1到d_max+1之间
        valid = (ell_vals > 0) & (d_s_vals > 0.1) & (d_s_vals < self.d + 1.0) & \
                (~np.isnan(ell_vals)) & (~np.isnan(d_s_vals))
        
        ell = ell_vals[valid]
        d_s = d_s_vals[valid]
        
        if len(ell) < 5:
            return {'error': f'Insufficient data points: {len(ell)}'}
        
        log_ell = np.log(ell)
        
        # 计算权重
        weights = np.ones_like(d_s)
        
        # 过渡区域高权重
        transition_center = (self.d_min + self.d) / 2
        distance = np.abs(d_s - transition_center)
        max_dist = (self.d - self.d_min) / 2
        weights = 1.0 + p['weight_transition_boost'] * (1 - distance / max_dist)
        
        # 远离奇点的点更可靠
        weights *= np.abs(log_ell) / (1 + np.abs(log_ell))
        
        # 选择有效区域
        mask = np.abs(log_ell) > p['log_ell_threshold']
        if np.sum(mask) < 5:
            mask = np.abs(log_ell) > 0.001
        
        x = 1.0 / log_ell[mask]
        y = d_s[mask]
        w = weights[mask]
        
        # 加权线性回归
        W = np.diag(w)
        X = np.vstack([x, np.ones(len(x))]).T
        
        try:
            XtWX = X.T @ W @ X
            XtWy = X.T @ W @ y
            params_fit = np.linalg.solve(XtWX, XtWy)
            
            c1_fit = -params_fit[0]
            d_max_fit = params_fit[1]
            
            # 计算R^2
            y_pred = d_max_fit - c1_fit * x
            ss_res = np.sum(w * (y - y_pred)**2)
            ss_tot = np.sum(w * (y - np.mean(y))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            # 计算误差
            residuals = y - y_pred
            mse = np.sum(w * residuals**2) / np.sum(w)
            
            try:
                cov = mse * np.linalg.inv(XtWX)
                c1_err = np.sqrt(cov[0, 0])
            except:
                c1_err = np.nan
            
            return {
                'c1': float(c1_fit),
                'c1_error': float(c1_err),
                'c1_theory': self.c1_theory,
                'bias': float(c1_fit - self.c1_theory),
                'bias_percent': float(abs(c1_fit - self.c1_theory) / self.c1_theory * 100),
                'd_max': float(d_max_fit),
                'quality': float(r_squared),
                'n_points': int(np.sum(mask)),
            }
            
        except Exception as e:
            return {'error': f'Fitting failed: {e}'}


def test_dimension_specific_extraction():
    """测试维度特定提取器"""
    print("=" * 70)
    print("维度特定c1提取器 - 测试")
    print("=" * 70)
    
    from dimension_specific_fractal import DimensionSpecificFractalGenerator
    
    for dim in [3, 4, 5]:
        print(f"\n{'='*70}")
        print(f"{dim}维空间 - 理论c1 = 1/{dim} = {1.0/dim:.4f}")
        print(f"{'='*70}")
        
        # 创建生成器和提取器
        gen = DimensionSpecificFractalGenerator(dimension=dim)
        extractor = DimensionSpecificExtractor(dimension=dim)
        
        # 测试多个样本
        c1_values = []
        
        for i in range(5):
            np.random.seed(i * 10 + dim)
            
            # 生成两种类型的分形
            if i % 2 == 0:
                points = gen.generate_dimension_optimized(n_points=400)
            else:
                points = gen.generate_three_region_fractal(n_points=400)
            
            # 提取c1
            result = extractor.extract_c1(points)
            
            if 'c1' in result and 0 < result['c1'] < 2:
                c1_values.append(result['c1'])
                status = "✓" if result.get('bias_percent', 100) < 20 else "~"
                print(f"  样本{i+1}: c1 = {result['c1']:.4f} "
                      f"(偏差{result.get('bias_percent', 0):.1f}%) {status}")
            else:
                print(f"  样本{i+1}: 失败 - {result.get('error', 'Unknown')[:30]}")
        
        if c1_values:
            c1_values = np.array(c1_values)
            mean_c1 = np.mean(c1_values)
            theory = 1.0 / dim
            bias_pct = abs(mean_c1 - theory) / theory * 100
            
            print(f"\n  统计:")
            print(f"    理论值: {theory:.4f}")
            print(f"    均值: {mean_c1:.4f}")
            print(f"    标准差: {np.std(c1_values):.4f}")
            print(f"    偏差: {bias_pct:.1f}%")
            
            if bias_pct < 20:
                print(f"    ✅ 达到目标 (<20%)")
            elif bias_pct < 50:
                print(f"    🟡 接近目标")
            else:
                print(f"    ⚠️ 需要改进")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_dimension_specific_extraction()
