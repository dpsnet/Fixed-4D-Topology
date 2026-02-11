#!/usr/bin/env python3
"""
Hejhal算法实现 - Maass形式特征值计算
================================================

本模块实现Hejhal配点法计算模群SL(2,Z)上Maass尖点形式的特征值。

基于:
- Sarnak, P. (2003). "Spectra of Hyperbolic Surfaces" (附录7)
- Hejhal, D. (1981). "Some observations concerning eigenvalues of the Laplacian"

作者: Research Team
日期: 2026-02-11
"""

import numpy as np
from scipy.linalg import svdvals, svd
from scipy.optimize import minimize_scalar
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import warnings
import time

warnings.filterwarnings('ignore')

# 尝试导入mpmath
try:
    import mpmath
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("警告: mpmath未安装，Bessel函数计算可能不准确")
    print("建议: pip install mpmath")


@dataclass
class HejhalConfig:
    """Hejhal算法配置参数"""
    truncation_M: int = 15          # Fourier截断参数
    num_points: int = 15            # 配点数量
    y_min: float = 0.866025403784   # 基本域底部 (sqrt(3)/2)
    y_max: float = 1.3              # y坐标上限
    tolerance: float = 1e-8         # 收敛容差
    parity: str = 'even'            # 'even' 或 'odd'
    mpmath_dps: int = 25            # mpmath精度


class MaassEigenvalueSolver:
    """
    Maass形式特征值求解器
    
    使用Hejhal配点法计算SL(2,Z)上Maass尖点形式的特征值。
    """
    
    # 已知特征值（来自文献，用于验证）
    # Hejhal (1992), Booker-Strömbergsson-Venkatesh (2006)
    KNOWN_EVEN_R = [
        13.779751351890, 17.738563381109, 19.423481346970,
        21.315796882311, 22.785280830796, 24.608206712860
    ]
    
    KNOWN_ODD_R = [
        9.533695261349, 12.173008240650, 14.358509516256,
        16.138121172691, 16.644259197914, 18.180913141642
    ]
    
    def __init__(self, config: Optional[HejhalConfig] = None):
        """
        初始化求解器
        
        参数:
            config: 配置参数，使用默认配置如果为None
        """
        self.config = config or HejhalConfig()
        
        if HAS_MPMATH:
            mpmath.mp.dps = self.config.mpmath_dps
        
        self.points = self._select_collocation_points()
        self._bessel_cache: Dict[Tuple[float, float], float] = {}
        
    def _select_collocation_points(self) -> List[complex]:
        """
        选择配点
        
        在基本域内选择点：|x| < 0.5, |z| > 1, y > sqrt(3)/2
        """
        M = self.config.num_points
        y_min = self.config.y_min
        y_max = self.config.y_max
        
        points = []
        ny = int(np.sqrt(M)) + 1
        
        # y坐标 - 指数分布，更多点在底部（Fourier展开收敛更好）
        y_vals = y_min + (y_max - y_min) * np.linspace(0, 1, ny)**0.5
        
        for y in y_vals:
            # 基本域边界: |x| < min(0.5, sqrt(y^2 - 1))
            x_bound = min(0.45, np.sqrt(max(0.05, y*y - 1)))
            if x_bound > 0.02:
                nx = int(M / len(y_vals)) + 1
                x_vals = np.linspace(-x_bound, x_bound, nx)
                for x in x_vals:
                    if len(points) < M:
                        points.append(complex(x, y))
        
        # 确保有M个点
        while len(points) < M:
            y = y_min + (y_max - y_min) * np.random.random()
            x_bound = min(0.45, np.sqrt(max(0.05, y*y - 1)))
            if x_bound > 0.02:
                x = (2*np.random.random() - 1) * x_bound
                points.append(complex(x, y))
        
        return points[:M]
    
    def _k_bessel(self, t: float, x: float) -> float:
        """
        计算修正Bessel函数 K_{it}(x)
        
        对于实数x，K_{it}(x)是实数。
        使用mpmath进行高精度计算。
        """
        if x <= 0:
            return 0.0
        
        # 检查缓存
        key = (round(t, 10), round(x, 10))
        if key in self._bessel_cache:
            return self._bessel_cache[key]
        
        if not HAS_MPMATH:
            # 后备：使用渐近展开
            if x > 10:
                return np.sqrt(np.pi / (2*x)) * np.exp(-x)
            return 0.0
        
        try:
            result = mpmath.besselk(1j * t, x)
            val = float(result.real)
            self._bessel_cache[key] = val
            return val
        except Exception:
            return 0.0
    
    def _compute_matrix_element(self, z: complex, n: int, t: float) -> float:
        """
        计算配点矩阵元素
        
        I_n(z; t) = term(z) - term(S(z))
        
        其中 S(z) = -1/z 是模变换。
        """
        x, y = z.real, z.imag
        
        # 原点处的项
        arg1 = 2 * np.pi * n * y
        k1 = self._k_bessel(t, arg1)
        b1 = np.sqrt(y) * k1
        
        if self.config.parity == 'even':
            term1 = b1 * np.cos(2 * np.pi * n * x)
        else:
            term1 = b1 * np.sin(2 * np.pi * n * x)
        
        # 变换点 S(z) = -1/z
        denom = x*x + y*y
        if denom < 1e-10:
            return term1
        
        x_s = -x / denom
        y_s = y / denom
        
        arg2 = 2 * np.pi * n * y_s
        k2 = self._k_bessel(t, arg2)
        b2 = np.sqrt(y_s) * k2
        
        if self.config.parity == 'even':
            term2 = b2 * np.cos(2 * np.pi * n * x_s)
        else:
            term2 = b2 * np.sin(2 * np.pi * n * x_s)
        
        return term1 - term2
    
    def construct_matrix(self, t: float) -> np.ndarray:
        """构造配点矩阵 A(t)"""
        M = self.config.truncation_M
        A = np.zeros((M, M))
        
        for j, z in enumerate(self.points[:M]):
            for n in range(1, M + 1):
                A[j, n-1] = self._compute_matrix_element(z, n, t)
        
        return A
    
    def matrix_condition(self, t: float) -> float:
        """
        计算矩阵条件指标
        
        使用归一化后的最小奇异值与最大奇异值之比。
        在特征值处，这个比值应该很小。
        """
        try:
            A = self.construct_matrix(t)
            norm = np.linalg.norm(A)
            if norm < 1e-300:
                return 1.0
            
            A_norm = A / norm
            s = svdvals(A_norm)
            s_filtered = s[s > 1e-15]
            
            if len(s_filtered) < 2:
                return 1.0
            
            return float(s_filtered[-1] / s_filtered[0])
        except:
            return 1.0
    
    def find_eigenvalue(self, t_guess: float, 
                       half_width: float = 0.4) -> Optional[Tuple[float, float]]:
        """
        在t_guess附近搜索特征值
        
        返回:
            (t_opt, condition_ratio) 如果找到，否则None
        """
        # 粗搜索
        t_vals = np.linspace(t_guess - half_width, t_guess + half_width, 40)
        conditions = []
        
        for t in t_vals:
            cond = self.matrix_condition(t)
            conditions.append(cond)
        
        conditions = np.array(conditions)
        min_idx = np.argmin(conditions)
        min_cond = conditions[min_idx]
        
        if min_cond > 0.3:  # 没有明显的极小值
            return None
        
        # 精化
        t_best = t_vals[min_idx]
        try:
            result = minimize_scalar(
                self.matrix_condition,
                bounds=(max(0.1, t_best - 0.1), t_best + 0.1),
                method='bounded',
                options={'xatol': self.config.tolerance, 'maxiter': 30}
            )
            if result.success:
                return result.x, result.fun
        except:
            pass
        
        return t_best, min_cond
    
    def compute_eigenvalues(self, n: int = 3, 
                           parity: str = 'even') -> List[Tuple[int, float, float, float]]:
        """
        计算前n个特征值
        
        参数:
            n: 特征值数量
            parity: 'even' 或 'odd'
            
        返回:
            [(序号, R, λ, 误差), ...]
        """
        self.config.parity = parity
        known = self.KNOWN_EVEN_R if parity == 'even' else self.KNOWN_ODD_R
        
        results = []
        print(f"\n计算前{n}个{parity}形式特征值")
        print("=" * 70)
        
        for i in range(min(n, len(known))):
            R_known = known[i]
            print(f"\n第{i+1}个 (文献值 R = {R_known:.6f}):")
            
            start = time.time()
            result = self.find_eigenvalue(R_known, half_width=0.5)
            elapsed = time.time() - start
            
            if result:
                t, cond = result
                lam = 0.25 + t*t
                error = abs(t - R_known)
                results.append((i+1, t, lam, error))
                print(f"  ✓ R = {t:.8f}, λ = {lam:.4f}")
                print(f"    误差 = {error:.2e}, 条件数 = {cond:.2e}, 时间 = {elapsed:.1f}s")
            else:
                print(f"  ✗ 未找到")
        
        return results
    
    def get_fourier_coefficients(self, t: float) -> np.ndarray:
        """
        获取Fourier系数
        
        使用SVD的右奇异向量作为Fourier系数。
        """
        A = self.construct_matrix(t)
        try:
            _, _, Vh = svd(A)
            coeffs = Vh[-1, :].copy()
            # 归一化
            max_c = np.max(np.abs(coeffs))
            if max_c > 0:
                coeffs = coeffs / max_c
            return coeffs
        except:
            return np.zeros(self.config.truncation_M)


def demo_quick():
    """快速演示"""
    print("=" * 70)
    print("Hejhal算法 - Maass形式特征值计算 (快速演示)")
    print("=" * 70)
    
    # 第一个偶形式
    print("\n【测试1】第一个偶形式 (文献值 R ≈ 13.78)")
    print("-" * 70)
    
    config = HejhalConfig(truncation_M=10, num_points=10, parity='even', mpmath_dps=20)
    solver = MaassEigenvalueSolver(config)
    
    result = solver.find_eigenvalue(13.8, half_width=0.5)
    if result:
        t, cond = result
        known = MaassEigenvalueSolver.KNOWN_EVEN_R[0]
        print(f"✓ 找到: R = {t:.6f}")
        print(f"  文献值: R = {known:.6f}")
        print(f"  误差: {abs(t - known):.4f}")
    
    # 第一个奇形式
    print("\n【测试2】第一个奇形式 (文献值 R ≈ 9.53)")
    print("-" * 70)
    
    config = HejhalConfig(truncation_M=8, num_points=8, parity='odd', mpmath_dps=20)
    solver = MaassEigenvalueSolver(config)
    
    result = solver.find_eigenvalue(9.5, half_width=0.5)
    if result:
        t, cond = result
        known = MaassEigenvalueSolver.KNOWN_ODD_R[0]
        print(f"✓ 找到: R = {t:.6f}")
        print(f"  文献值: R = {known:.6f}")
        print(f"  误差: {abs(t - known):.4f}")
    
    print("\n" + "=" * 70)
    print("说明: 快速演示使用较低精度，完整计算需要 truncation_M=15-20")
    print("=" * 70)


def compute_full(n_even: int = 3, n_odd: int = 2):
    """完整计算"""
    print("=" * 70)
    print("Hejhal算法 - 完整计算")
    print("=" * 70)
    
    # 偶形式
    config = HejhalConfig(truncation_M=15, num_points=15, parity='even', mpmath_dps=25)
    solver = MaassEigenvalueSolver(config)
    results_even = solver.compute_eigenvalues(n_even, 'even')
    
    # 奇形式
    config = HejhalConfig(truncation_M=12, num_points=12, parity='odd', mpmath_dps=25)
    solver = MaassEigenvalueSolver(config)
    results_odd = solver.compute_eigenvalues(n_odd, 'odd')
    
    # 总结
    print("\n" + "=" * 70)
    print("结果总结")
    print("=" * 70)
    
    if results_even:
        print("\n偶形式:")
        print(f"{'序号':<6}{'R':<18}{'λ':<20}{'误差':<12}")
        print("-" * 60)
        for idx, t, lam, err in results_even:
            print(f"{idx:<6}{t:<18.8f}{lam:<20.4f}{err:<12.2e}")
    
    if results_odd:
        print("\n奇形式:")
        print(f"{'序号':<6}{'R':<18}{'λ':<20}{'误差':<12}")
        print("-" * 60)
        for idx, t, lam, err in results_odd:
            print(f"{idx:<6}{t:<18.8f}{lam:<20.4f}{err:<12.2e}")


def main():
    import sys
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'demo'
    
    if command == 'demo':
        demo_quick()
    elif command == 'compute':
        n_even = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        n_odd = int(sys.argv[3]) if len(sys.argv) > 3 else 2
        compute_full(n_even, n_odd)
    elif command == 'even':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        config = HejhalConfig(truncation_M=15, num_points=15, parity='even', mpmath_dps=25)
        solver = MaassEigenvalueSolver(config)
        results = solver.compute_eigenvalues(n, 'even')
        
        print(f"\n{'序号':<6}{'R':<18}{'λ':<20}{'误差':<12}")
        print("=" * 60)
        for idx, t, lam, err in results:
            print(f"{idx:<6}{t:<18.8f}{lam:<20.4f}{err:<12.2e}")
    elif command == 'odd':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        config = HejhalConfig(truncation_M=12, num_points=12, parity='odd', mpmath_dps=25)
        solver = MaassEigenvalueSolver(config)
        results = solver.compute_eigenvalues(n, 'odd')
        
        print(f"\n{'序号':<6}{'R':<18}{'λ':<20}{'误差':<12}")
        print("=" * 60)
        for idx, t, lam, err in results:
            print(f"{idx:<6}{t:<18.8f}{lam:<20.4f}{err:<12.2e}")
    else:
        print("用法: python hejhal_maass.py [demo|compute|even|odd]")
        demo_quick()


if __name__ == '__main__':
    main()
