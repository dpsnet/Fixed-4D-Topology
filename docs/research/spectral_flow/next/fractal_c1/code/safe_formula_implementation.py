"""
安全公式实现
Safe Formula Implementation

使用无对数奇点的Logistic型过渡:
d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))
"""

import numpy as np
from typing import Tuple, Dict
from scipy.optimize import curve_fit


class SafeFormulaFractal:
    """
    使用安全公式的分形生成器
    
    公式: d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.d_min = 2.0
        self.d_max = float(dimension)
        self.c1_theory = 1.0 / dimension
    
    def spectral_dimension_safe(self, ell: np.ndarray, 
                                 ell_0: float = 1.0) -> np.ndarray:
        """
        安全的谱维度公式
        
        d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))
        
        特点:
        - 无对数，避免奇点
        - ℓ → 0: d_s → d_min
        - ℓ → ∞: d_s → d_max
        - ℓ = ℓ_0: d_s = (d_min + d_max)/2
        """
        ell = np.asarray(ell)
        
        # 避免除零
        ell_safe = np.maximum(ell, 1e-10)
        
        # 计算指数
        exponent = 1.0 / self.c1_theory
        
        # Logistic型过渡
        ratio = ell_0 / ell_safe
        transition = 1.0 / (1.0 + ratio ** exponent)
        
        d_s = self.d_min + (self.d_max - self.d_min) * transition
        
        return d_s
    
    def generate_fractal(self, n_points: int = 800,
                         ell_range: Tuple[float, float] = (0.01, 100.0),
                         ell_0: float = 1.0,
                         n_shells: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        生成分形
        
        每个壳层有明确的谱维度
        """
        points = []
        shell_centers = []
        shell_d_s = []
        
        # 创建壳层
        ell_edges = np.logspace(np.log10(ell_range[0]), 
                                np.log10(ell_range[1]), 
                                n_shells + 1)
        
        for i in range(n_shells):
            ell_inner = ell_edges[i]
            ell_outer = ell_edges[i + 1]
            ell_center = np.sqrt(ell_inner * ell_outer)
            
            # 计算该壳层的谱维度
            d_s = self.spectral_dimension_safe(np.array([ell_center]), ell_0)[0]
            
            # 该壳层的点数
            n_shell = max(5, n_points // n_shells)
            
            # 生成点
            for _ in range(n_shell):
                point = self._generate_point(ell_inner, ell_outer, d_s)
                points.append(point)
            
            shell_centers.append(ell_center)
            shell_d_s.append(d_s)
        
        points = np.array(points)
        
        # 标准化
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            extra = np.random.randn(n_points - len(points), self.d) * ell_range[1] / 10
            points = np.vstack([points, extra])
        
        return points, np.array(shell_centers), np.array(shell_d_s)
    
    def _generate_point(self, r_inner: float, r_outer: float, d_s: float) -> np.ndarray:
        """在壳层内生成具有特定维度的点"""
        # 随机方向
        direction = np.random.randn(self.d)
        direction /= np.linalg.norm(direction)
        
        # 径向距离
        u = np.random.rand()
        r = (r_inner ** self.d + u * (r_outer ** self.d - r_inner ** self.d)) ** (1.0 / self.d)
        
        # 基础位置
        base = r * direction
        
        # 添加具有d_s维特征的涨落
        n_active = max(2, min(self.d, int(np.round(d_s))))
        fluctuation = np.random.randn(self.d) * (r_outer - r_inner) / 3
        
        if n_active < self.d:
            compress_dims = np.random.choice(self.d, self.d - n_active, replace=False)
            fluctuation[compress_dims] *= 0.05
        
        return base + fluctuation


class SafeFormulaExtractor:
    """
    使用安全公式的c1提取器
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.d_min = 2.0
        self.d_max = float(dimension)
    
    def extract_c1(self, points: np.ndarray, ell_0: float = 1.0) -> Dict:
        """
        提取c1
        """
        try:
            from fractal_laplacian import FractalLaplacian
            
            # 构建拉普拉斯
            fl = FractalLaplacian(dimension=self.d)
            L = fl.construct_graph_laplacian(points, epsilon=None)
            
            # 计算谱维度
            t_range = np.logspace(-2, 2, 50)
            t_vals, d_s = fl.compute_spectral_dimension(
                L, 
                t_range=t_range,
                n_eigenvalues=min(40, len(points)//4)
            )
            
            # 转换为长度尺度
            ell_vals = np.sqrt(t_vals)
            
            # 过滤
            valid = (ell_vals > 0) & (d_s > 0.1) & (d_s < self.d + 0.5) & \
                    (~np.isnan(ell_vals)) & (~np.isnan(d_s))
            
            if np.sum(valid) < 10:
                return {'error': f'Insufficient points: {np.sum(valid)}'}
            
            ell = ell_vals[valid]
            d_s_meas = d_s[valid]
            
            # 拟合新公式
            # d_s = d_min + (d_max - d_min) / (1 + (ell_0/ell)^(1/c1))
            # 拟合参数: d_max, c1
            
            def model(ell, d_max, c1):
                if c1 <= 0.01:
                    return np.full_like(ell, np.nan)
                exponent = 1.0 / c1
                ratio = ell_0 / ell
                transition = 1.0 / (1.0 + ratio ** exponent)
                return self.d_min + (d_max - self.d_min) * transition
            
            # 初始猜测
            c1_theory = 1.0 / self.d
            p0 = [self.d_max, c1_theory]
            
            # 边界
            bounds = ([self.d_min + 0.5, 0.01], [self.d_max + 2, 2.0])
            
            popt, pcov = curve_fit(model, ell, d_s_meas, p0=p0, bounds=bounds, maxfev=10000)
            
            d_max_fit, c1_fit = popt
            
            # 计算R^2
            y_pred = model(ell, *popt)
            ss_res = np.sum((d_s_meas - y_pred)**2)
            ss_tot = np.sum((d_s_meas - np.mean(d_s_meas))**2)
            r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            
            c1_theory = 1.0 / self.d
            
            return {
                'c1': float(c1_fit),
                'c1_theory': c1_theory,
                'd_max': float(d_max_fit),
                'd_max_theory': self.d_max,
                'quality': float(r_squared),
                'bias': float(c1_fit - c1_theory),
                'bias_percent': float(abs(c1_fit - c1_theory) / c1_theory * 100),
                'd_s_range': (float(d_s_meas.min()), float(d_s_meas.max())),
                'n_points': len(d_s_meas),
            }
            
        except Exception as e:
            return {'error': str(e)}


def test_safe_formula():
    """测试安全公式实现"""
    print("=" * 70)
    print("安全公式实现 - 测试")
    print("新公式: d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))")
    print("=" * 70)
    
    for dim in [3, 4, 5]:
        print(f"\n{'='*70}")
        print(f"{dim}维空间 (c1 = 1/{dim} = {1.0/dim:.4f})")
        print(f"{'='*70}")
        
        # 测试公式
        fractal = SafeFormulaFractal(dimension=dim)
        extractor = SafeFormulaExtractor(dimension=dim)
        
        # 显示公式行为
        print("\n公式行为:")
        for ell in [0.01, 0.1, 1.0, 10.0, 100.0]:
            d_s = fractal.spectral_dimension_safe(np.array([ell]))[0]
            print(f"  ℓ = {ell:6.2f}: d_s = {d_s:.3f}")
        
        # 测试提取
        print("\n生成与提取测试:")
        c1_values = []
        
        for i in range(5):
            np.random.seed(i * 10 + dim)
            points, centers, d_s_targets = fractal.generate_fractal(n_points=500)
            
            result = extractor.extract_c1(points)
            
            if 'c1' in result:
                c1_values.append(result['c1'])
                bias = result.get('bias_percent', 0)
                status = '✓' if bias < 20 else ('~' if bias < 50 else '✗')
                print(f"  样本{i+1}: c1={result['c1']:.4f}, d_max={result['d_max']:.2f}, "
                      f"R²={result['quality']:.3f}, 偏差={bias:.1f}% {status}")
            else:
                print(f"  样本{i+1}: 失败 - {result.get('error', 'Unknown')[:40]}")
        
        if c1_values:
            c1_values = np.array(c1_values)
            mean_c1 = np.mean(c1_values)
            theory = 1.0 / dim
            bias_pct = abs(mean_c1 - theory) / theory * 100
            
            print(f"\n  统计:")
            print(f"    理论c1: {theory:.4f}")
            print(f"    提取均值: {mean_c1:.4f} ± {np.std(c1_values):.4f}")
            print(f"    偏差: {bias_pct:.1f}%")
            
            if bias_pct < 20:
                print(f"    ✅ 达到目标")
            elif bias_pct < 50:
                print(f"    🟡 接近")
            else:
                print(f"    ⚠️ 需要改进")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_safe_formula()
