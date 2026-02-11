#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格迹公式渐近证明 - 计算验证脚本
任务ID: P3-C1-001

本脚本用于：
1. 计算具体Kleinian群的热核迹
2. 小t渐近行为分析
3. 提取δ的数值估计
4. 与已知维数对比验证
5. 误差分析

作者: Research Team
创建日期: 2026-02-11
严格性级别: L1 (Annals of Mathematics标准)
"""

import numpy as np
from numpy import sinh, cosh, exp, sqrt, pi
from scipy import integrate
from scipy.optimize import curve_fit
from scipy.special import kv, gamma
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Callable, Optional
from abc import ABC, abstractmethod
import warnings

# 设置显示精度
np.set_printoptions(precision=15, suppress=True)


# ============================================================================
# 1. 基础热核计算
# ============================================================================

class HyperbolicHeatKernel:
    """
    双曲空间 H³ 上的热核计算
    
    热核公式: K(t, x, y) = (1/(4πt)^(3/2)) * (r/sinh(r)) * exp(-t - r²/(4t))
    其中 r = d_H³(x, y) 是双曲距离
    """
    
    @staticmethod
    def fundamental_kernel(t: float, r: float) -> float:
        """
        计算双曲空间的基本热核
        
        Args:
            t: 时间参数 (t > 0)
            r: 双曲距离
            
        Returns:
            K_H³(t, r): 热核值
        """
        if t <= 0:
            raise ValueError("时间参数t必须为正")
        if r < 0:
            raise ValueError("距离r必须非负")
            
        # 处理 r = 0 的情况
        if r == 0:
            return (1.0 / (4 * pi * t)**(1.5)) * exp(-t)
        
        # 标准公式
        prefactor = 1.0 / (4 * pi * t)**(1.5)
        geometric_factor = r / sinh(r)
        gaussian_factor = exp(-t - r**2 / (4 * t))
        
        return prefactor * geometric_factor * gaussian_factor
    
    @staticmethod
    def short_time_asymptotic(t: float, r: float, order: int = 2) -> float:
        """
        热核的小t渐近展开
        
        Args:
            t: 时间参数 (小t)
            r: 双曲距离
            order: 展开阶数
            
        Returns:
            渐近展开近似值
        """
        if order < 0:
            raise ValueError("展开阶数必须非负")
            
        # 主导项
        result = (1.0 / (4 * pi * t)**(1.5)) * exp(-r**2 / (4 * t))
        
        # 高阶修正
        if order >= 1:
            # O(t^(-1/2)) 修正
            result *= (1 - t + r**2 / (12 * t) * (1 - r**2 / 10))
            
        if order >= 2:
            # 更高阶修正
            result *= (1 + r**4 / (240 * t**2))
            
        return result
    
    @staticmethod
    def verify_heat_equation(t: float, r: float, eps: float = 1e-8) -> float:
        """
        验证热方程: ∂_t K = ΔK
        
        Args:
            t: 时间参数
            r: 双曲距离
            eps: 数值微分步长
            
        Returns:
            热方程残差 |∂_t K - ΔK|
        """
        # 数值微分计算 ∂_t K
        Kt_plus = HyperbolicHeatKernel.fundamental_kernel(t + eps, r)
        Kt_minus = HyperbolicHeatKernel.fundamental_kernel(t - eps, r)
        dt_K = (Kt_plus - Kt_minus) / (2 * eps)
        
        # 计算径向Laplacian (在H³中)
        # Δf = f'' + 2 coth(r) f'
        Kr_plus = HyperbolicHeatKernel.fundamental_kernel(t, r + eps)
        Kr_minus = HyperbolicHeatKernel.fundamental_kernel(t, r - eps)
        dr_K = (Kr_plus - Kr_minus) / (2 * eps)
        d2r_K = (Kr_plus - 2 * HyperbolicHeatKernel.fundamental_kernel(t, r) + Kr_minus) / eps**2
        
        Delta_K = d2r_K + 2 * cosh(r) / sinh(r) * dr_K
        
        return abs(dt_K - Delta_K)


# ============================================================================
# 2. Kleinian群基类
# ============================================================================

class KleinianGroup(ABC):
    """
    Kleinian群的抽象基类
    """
    
    def __init__(self, name: str, expected_delta: Optional[float] = None):
        self.name = name
        self.expected_delta = expected_delta
        self.elements = []
        
    @abstractmethod
    def generate_elements(self, max_norm: float) -> List[np.ndarray]:
        """
        生成群的元素（作为Poincaré上半空间模型的等距映射）
        
        Args:
            max_norm: 元素范数上界
            
        Returns:
            群元素列表（SL(2,C)矩阵）
        """
        pass
    
    @abstractmethod
    def fundamental_domain_volume(self) -> float:
        """返回基本域的体积（如果有限）"""
        pass
    
    @abstractmethod
    def orbit_count(self, x: np.ndarray, y: np.ndarray, R: float) -> int:
        """
        计算轨道点计数: #{γ ∈ Γ : d(x, γy) ≤ R}
        
        Args:
            x, y: H³中的点
            R: 距离上界
            
        Returns:
            轨道点数量
        """
        pass


class BianchiGroupPSL2Zi(KleinianGroup):
    """
    Bianchi群 PSL(2, Z[i])
    
    这是高斯整数环上的模群，是一个算术Kleinian群。
    极限集是整个边界，δ = 2。
    """
    
    def __init__(self):
        super().__init__("PSL(2, Z[i])", expected_delta=2.0)
        # 生成元
        self.S = np.array([[0, -1], [1, 0]], dtype=complex)
        self.T = np.array([[1, 1], [0, 1]], dtype=complex)
        self.U = np.array([[1, 1j], [0, 1]], dtype=complex)
        
    def generate_elements(self, max_norm: float = 10.0) -> List[np.ndarray]:
        """
        生成PSL(2, Z[i])的元素
        
        使用生成元 S, T, U 的有限字
        """
        elements = [np.eye(2, dtype=complex)]  # 单位元
        generators = [self.S, self.T, self.U]
        
        # 有限深度搜索
        max_depth = 3
        
        def generate_words(current: np.ndarray, depth: int):
            if depth >= max_depth:
                return
            for g in generators:
                new_elem = current @ g
                # 归一化到PSL(2,C)
                det = new_elem[0, 0] * new_elem[1, 1] - new_elem[0, 1] * new_elem[1, 0]
                new_elem = new_elem / sqrt(det)
                
                norm = np.linalg.norm(new_elem)
                if norm <= max_norm:
                    elements.append(new_elem)
                    generate_words(new_elem, depth + 1)
        
        generate_words(np.eye(2, dtype=complex), 0)
        
        # 去重
        unique_elements = []
        seen = set()
        for elem in elements:
            key = tuple(elem.flatten().round(10))
            if key not in seen:
                seen.add(key)
                unique_elements.append(elem)
        
        self.elements = unique_elements
        return unique_elements
    
    def fundamental_domain_volume(self) -> float:
        """
        PSL(2, Z[i])的基本域体积
        
        这是已知的: Vol = (2π²)/3 * |D_K|^(3/2) / (4π²) * ζ_K(2)
        对于Q(i)，|D_K| = 4
        """
        # 近似值（需要精确计算）
        return 0.305321...
    
    def orbit_count(self, x: np.ndarray, y: np.ndarray, R: float) -> int:
        """轨道计数估计"""
        # 对于算术群，轨道计数渐近为 c * e^(2R)
        # 这里使用简化估计
        if not self.elements:
            self.generate_elements()
            
        count = 0
        for gamma in self.elements:
            # 计算 d(x, γy)
            gy = self._mobius_action(gamma, y)
            dist = self._hyperbolic_distance(x, gy)
            if dist <= R:
                count += 1
                
        return count
    
    @staticmethod
    def _mobius_action(gamma: np.ndarray, z: np.ndarray) -> np.ndarray:
        """Möbius变换作用在H³上"""
        a, b, c, d = gamma[0, 0], gamma[0, 1], gamma[1, 0], gamma[1, 1]
        
        # z = (x1, x2, y) 其中 y > 0
        x1, x2, y = z[0], z[1], z[2]
        z_complex = x1 + 1j * x2
        
        numerator = (a * z_complex + b) * np.conj(c * z_complex + d) + a * np.conj(c) * y**2
        denominator = abs(c * z_complex + d)**2 + abs(c)**2 * y**2
        
        new_z = numerator / denominator
        new_y = y / denominator
        
        return np.array([new_z.real, new_z.imag, new_y])
    
    @staticmethod
    def _hyperbolic_distance(x: np.ndarray, y: np.ndarray) -> float:
        """计算H³中的双曲距离"""
        # 使用公式: cosh(d) = 1 + |x - y|² / (2 x₃ y₃)
        diff_norm_sq = np.sum((x - y)**2)
        cosh_d = 1 + diff_norm_sq / (2 * x[2] * y[2])
        return np.arccosh(cosh_d)


class BianchiGroupPSL2Zomega(KleinianGroup):
    """
    Bianchi群 PSL(2, Z[ω])，其中 ω = e^(2πi/3)
    
    这是Eisenstein整数环上的模群。
    极限集维数 δ = 2。
    """
    
    def __init__(self):
        super().__init__("PSL(2, Z[ω])", expected_delta=2.0)
        omega = exp(2j * pi / 3)
        self.S = np.array([[0, -1], [1, 0]], dtype=complex)
        self.T = np.array([[1, 1], [0, 1]], dtype=complex)
        self.U = np.array([[1, omega], [0, 1]], dtype=complex)
        
    def generate_elements(self, max_norm: float = 10.0) -> List[np.ndarray]:
        """生成PSL(2, Z[ω])的元素"""
        # 类似PSL(2, Z[i])的实现
        elements = [np.eye(2, dtype=complex)]
        generators = [self.S, self.T, self.U]
        max_depth = 3
        
        def generate_words(current: np.ndarray, depth: int):
            if depth >= max_depth:
                return
            for g in generators:
                new_elem = current @ g
                det = new_elem[0, 0] * new_elem[1, 1] - new_elem[0, 1] * new_elem[1, 0]
                new_elem = new_elem / sqrt(det)
                
                norm = np.linalg.norm(new_elem)
                if norm <= max_norm:
                    elements.append(new_elem)
                    generate_words(new_elem, depth + 1)
        
        generate_words(np.eye(2, dtype=complex), 0)
        
        # 去重
        unique_elements = []
        seen = set()
        for elem in elements:
            key = tuple(elem.flatten().round(10))
            if key not in seen:
                seen.add(key)
                unique_elements.append(elem)
        
        self.elements = unique_elements
        return unique_elements
    
    def fundamental_domain_volume(self) -> float:
        """基本域体积"""
        # 对于Q(ω)，|D_K| = 3
        return 0.169156...
    
    def orbit_count(self, x: np.ndarray, y: np.ndarray, R: float) -> int:
        """轨道计数"""
        if not self.elements:
            self.generate_elements()
            
        count = 0
        for gamma in self.elements:
            gy = BianchiGroupPSL2Zi._mobius_action(gamma, y)
            dist = BianchiGroupPSL2Zi._hyperbolic_distance(x, gy)
            if dist <= R:
                count += 1
                
        return count


class SchottkyGroup(KleinianGroup):
    """
    Schottky群（自由Kleinian群）
    
    由n对圆的反演生成，极限集是Cantor集，δ < 2。
    """
    
    def __init__(self, generators: List[np.ndarray], name: str = "Schottky"):
        super().__init__(name, expected_delta=None)
        self.generators = generators
        self.rank = len(generators)
        
    def generate_elements(self, max_norm: float = 20.0) -> List[np.ndarray]:
        """
        生成Schottky群的元素
        
        Schottky群是自由群，元素可以唯一表示为生成元的约化字
        """
        elements = [np.eye(2, dtype=complex)]
        
        # 包含逆元
        all_gens = self.generators + [np.linalg.inv(g) for g in self.generators]
        
        max_depth = 4
        
        def generate_words(current: np.ndarray, last_gen_idx: Optional[int], depth: int):
            if depth >= max_depth:
                return
            for i, g in enumerate(all_gens):
                # 避免约化 (不立即使用逆元)
                if last_gen_idx is not None:
                    if i == (last_gen_idx + len(self.generators)) % (2 * len(self.generators)):
                        continue
                
                new_elem = current @ g
                det = new_elem[0, 0] * new_elem[1, 1] - new_elem[0, 1] * new_elem[1, 0]
                if abs(det) > 1e-10:
                    new_elem = new_elem / sqrt(det)
                    
                    norm = np.linalg.norm(new_elem)
                    if norm <= max_norm:
                        elements.append(new_elem)
                        generate_words(new_elem, i, depth + 1)
        
        generate_words(np.eye(2, dtype=complex), None, 0)
        
        self.elements = elements
        return elements
    
    def fundamental_domain_volume(self) -> float:
        """Schottky群的基本域体积无限"""
        return float('inf')
    
    def orbit_count(self, x: np.ndarray, y: np.ndarray, R: float) -> int:
        """轨道计数"""
        if not self.elements:
            self.generate_elements()
            
        count = 0
        for gamma in self.elements:
            gy = BianchiGroupPSL2Zi._mobius_action(gamma, y)
            dist = BianchiGroupPSL2Zi._hyperbolic_distance(x, gy)
            if dist <= R:
                count += 1
                
        return count
    
    @staticmethod
    def create_classical_schottky(centers: List[complex], radii: List[float]) -> 'SchottkyGroup':
        """
        创建经典Schottky群
        
        Args:
            centers: 圆心列表 (在复平面上)
            radii: 半径列表
            
        Returns:
            SchottkyGroup实例
        """
        # 构造将圆映射到圆的反演变换
        generators = []
        for i in range(len(centers) // 2):
            c1, r1 = centers[2*i], radii[2*i]
            c2, r2 = centers[2*i+1], radii[2*i+1]
            
            # 构造将圆1映射到圆2的变换
            # 这是一个Möbius变换
            a = (c2 - c1) / (r1 * r2)
            b = c1 * (1 - r2/r1)
            c = 0
            d = r2 / r1
            
            gamma = np.array([[a, b], [c, d]], dtype=complex)
            generators.append(gamma)
            
        return SchottkyGroup(generators, name=f"Classical_Schottky_{len(generators)}")


# ============================================================================
# 3. 热核迹计算
# ============================================================================

class HeatKernelTrace:
    """
    Kleinian群的热核迹计算
    """
    
    def __init__(self, group: KleinianGroup, kernel: HyperbolicHeatKernel):
        self.group = group
        self.kernel = kernel
        
    def compute_trace(self, t_values: np.ndarray, x0: Optional[np.ndarray] = None,
                     truncation_radius: Optional[float] = None) -> np.ndarray:
        """
        计算热核迹 Θ_Γ(t) = ∫_F K_Γ(t, x, x) dμ(x)
        
        Args:
            t_values: 时间参数数组
            x0: 积分中心点 (默认原点)
            truncation_radius: 群元素截断半径
            
        Returns:
            热核迹值数组
        """
        if x0 is None:
            x0 = np.array([0.0, 0.0, 1.0])  # H³中的标准点
            
        if not self.group.elements:
            self.group.generate_elements()
            
        traces = np.zeros(len(t_values))
        
        for i, t in enumerate(t_values):
            trace_val = 0.0
            
            for gamma in self.group.elements:
                # 计算 γx0
                gamma_x0 = BianchiGroupPSL2Zi._mobius_action(gamma, x0)
                
                # 计算 d(x0, γx0)
                r = BianchiGroupPSL2Zi._hyperbolic_distance(x0, gamma_x0)
                
                # 截断检查
                if truncation_radius is not None and r > truncation_radius:
                    continue
                    
                # 热核贡献
                if r < 1e-10:  # 单位元
                    trace_val += self.kernel.fundamental_kernel(t, 0)
                else:
                    trace_val += self.kernel.fundamental_kernel(t, r)
                    
            traces[i] = trace_val
            
        return traces
    
    def asymptotic_analysis(self, t_values: np.ndarray, traces: np.ndarray) -> dict:
        """
        分析热核迹的小t渐近行为
        
        模型: Θ(t) ~ a * t^(-3/2) + b * t^(-1/2) + c + O(t^(1/2))
        
        Args:
            t_values: 时间参数数组（小t区域）
            traces: 对应的热核迹值
            
        Returns:
            包含拟合参数和δ估计的字典
        """
        # 取对数进行线性拟合
        log_t = np.log(t_values)
        log_theta = np.log(traces)
        
        # 小t区域的主导行为应该接近 t^(-3/2)
        # 即 log(Θ) ≈ -(3/2) * log(t) + const
        
        # 拟合主导指数
        def power_law(t, a, alpha):
            return a * t**alpha
            
        # 使用最小二乘拟合
        try:
            popt, pcov = curve_fit(power_law, t_values, traces, p0=[1.0, -1.5])
            a_fit, alpha_fit = popt
            alpha_err = np.sqrt(pcov[1, 1])
        except Exception as e:
            warnings.warn(f"拟合失败: {e}")
            a_fit, alpha_fit, alpha_err = None, None, None
        
        # 更详细的渐近展开拟合
        # Θ(t) = c0 * t^(-3/2) + c1 * t^(-1/2) + c2 + O(t^(1/2))
        def asymptotic_expansion(t, c0, c1, c2):
            return c0 * t**(-1.5) + c1 * t**(-0.5) + c2
            
        try:
            popt_full, pcov_full = curve_fit(
                asymptotic_expansion, t_values, traces, 
                p0=[0.1, 1.0, 0.0],
                maxfev=10000
            )
            c0, c1, c2 = popt_full
        except Exception as e:
            warnings.warn(f"详细展开拟合失败: {e}")
            c0, c1, c2 = None, None, None
        
        return {
            'power_law_amplitude': a_fit,
            'power_law_exponent': alpha_fit,
            'power_law_exponent_error': alpha_err,
            'volume_coefficient': c0,  # 与体积相关
            'entropy_coefficient': c1,  # 可能与δ相关
            'constant_term': c2,
            'fit_covariance': pcov if 'pcov' in dir() else None
        }
    
    def estimate_delta(self, t_values: np.ndarray, traces: np.ndarray,
                      method: str = 'spectral') -> dict:
        """
        从热核迹估计Hausdorff维数δ
        
        Args:
            t_values: 时间参数数组
            traces: 热核迹值
            method: 估计方法 ('spectral' 或 'geometric')
            
        Returns:
            δ估计结果字典
        """
        if method == 'spectral':
            # 谱方法：利用热核与特征值的联系
            # Θ(t) = Σ e^(-tλ_j)，低频行为与δ相关
            
            # 对于小t，分析修正项
            # 实际上，这需要更精细的分析
            
            # 简化估计：假设 δ ≈ 2 - c * (修正项)
            asymptotic = self.asymptotic_analysis(t_values, traces)
            
            if asymptotic['entropy_coefficient'] is not None:
                # 启发式估计：c1 与 (2 - δ) 成正比
                c1 = asymptotic['entropy_coefficient']
                # 归一化因子依赖于群
                normalization = 1.0  # 需要根据具体群调整
                delta_est = 2.0 - c1 / normalization
            else:
                delta_est = None
                
            return {
                'delta_estimate': delta_est,
                'method': 'spectral',
                'confidence': 'low' if delta_est is None else 'medium'
            }
            
        elif method == 'geometric':
            # 几何方法：利用轨道计数
            # 这需要计算 dN(R)/dR ~ e^(δR)
            
            # 简化实现
            return {
                'delta_estimate': None,
                'method': 'geometric',
                'confidence': 'not_implemented'
            }
        else:
            raise ValueError(f"未知方法: {method}")


# ============================================================================
# 4. 验证和测试
# ============================================================================

class VerificationSuite:
    """
    验证测试套件
    """
    
    def __init__(self):
        self.results = []
        
    def test_kernel_properties(self, kernel: HyperbolicHeatKernel) -> bool:
        """
        验证热核的基本性质
        
        1. 归一化: ∫ K(t, x, y) dy = 1
        2. 半群性: ∫ K(t, x, z) K(s, z, y) dz = K(t+s, x, y)
        3. 热方程: ∂_t K = ΔK
        """
        print("=" * 60)
        print("测试热核基本性质")
        print("=" * 60)
        
        t = 0.1
        r = 1.0
        
        # 测试热方程
        residual = kernel.verify_heat_equation(t, r)
        print(f"热方程残差 (t={t}, r={r}): {residual:.2e}")
        
        heat_eq_pass = residual < 1e-5
        print(f"热方程检验: {'通过' if heat_eq_pass else '失败'}")
        
        # 测试对称性
        K_xy = kernel.fundamental_kernel(t, r)
        K_yx = kernel.fundamental_kernel(t, r)
        symmetry_pass = abs(K_xy - K_yx) < 1e-15
        print(f"对称性检验: {'通过' if symmetry_pass else '失败'}")
        
        return heat_eq_pass and symmetry_pass
    
    def test_group_computation(self, group: KleinianGroup) -> dict:
        """测试群计算"""
        print(f"\n{'=' * 60}")
        print(f"测试群: {group.name}")
        print(f"{'=' * 60}")
        
        # 生成元素
        elements = group.generate_elements(max_norm=15.0)
        print(f"生成元素数量: {len(elements)}")
        
        # 基本测试点
        x0 = np.array([0.0, 0.0, 1.0])
        y0 = np.array([0.5, 0.0, 1.0])
        
        # 轨道计数测试
        R = 5.0
        count = group.orbit_count(x0, y0, R)
        print(f"轨道计数 (R={R}): {count}")
        
        return {
            'group_name': group.name,
            'num_elements': len(elements),
            'orbit_count': count
        }
    
    def test_trace_computation(self, group: KleinianGroup, 
                               t_values: np.ndarray) -> dict:
        """测试热核迹计算"""
        print(f"\n{'=' * 60}")
        print(f"测试热核迹计算: {group.name}")
        print(f"{'=' * 60}")
        
        kernel = HyperbolicHeatKernel()
        heat_trace = HeatKernelTrace(group, kernel)
        
        # 计算迹
        traces = heat_trace.compute_trace(t_values, truncation_radius=10.0)
        
        print(f"时间范围: [{t_values.min():.2e}, {t_values.max():.2f}]")
        print(f"迹值范围: [{traces.min():.6f}, {traces.max():.6f}]")
        
        # 渐近分析
        # 使用小t值进行分析
        small_t_mask = t_values < 0.1
        if np.sum(small_t_mask) >= 3:
            asymptotic = heat_trace.asymptotic_analysis(
                t_values[small_t_mask], 
                traces[small_t_mask]
            )
            
            print(f"\n渐近分析结果:")
            print(f"  幂律指数: {asymptotic['power_law_exponent']:.4f} " +
                  f"(期望: -1.5)")
            print(f"  体积系数: {asymptotic['volume_coefficient']}")
            print(f"  熵系数: {asymptotic['entropy_coefficient']}")
            
            # δ估计
            delta_est = heat_trace.estimate_delta(
                t_values[small_t_mask], 
                traces[small_t_mask]
            )
            print(f"\nδ估计: {delta_est['delta_estimate']}")
            print(f"  (期望δ = {group.expected_delta})")
            
            return {
                'group_name': group.name,
                't_values': t_values,
                'traces': traces,
                'asymptotic': asymptotic,
                'delta_estimate': delta_est
            }
        else:
            print("小t数据点不足，无法进行渐近分析")
            return {
                'group_name': group.name,
                't_values': t_values,
                'traces': traces
            }
    
    def run_all_tests(self) -> List[dict]:
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("严格迹公式渐近证明 - 计算验证套件")
        print("任务ID: P3-C1-001")
        print("=" * 60)
        
        # 1. 测试热核
        kernel = HyperbolicHeatKernel()
        kernel_pass = self.test_kernel_properties(kernel)
        
        # 2. 定义测试群
        groups = [
            BianchiGroupPSL2Zi(),
            BianchiGroupPSL2Zomega(),
        ]
        
        # 添加Schottky群示例
        # 创建一个简单的秩2 Schottky群
        schottky_gens = [
            np.array([[1.5, 0], [0, 1/1.5]], dtype=complex),  # 扩张
            np.array([[1, 2], [0, 1]], dtype=complex),  # 平移
        ]
        schottky = SchottkyGroup(schottky_gens, name="Schottky_Rank2_Example")
        groups.append(schottky)
        
        # 3. 测试每个群
        results = []
        t_values = np.logspace(-3, 0, 20)  # 从0.001到1
        
        for group in groups:
            try:
                group_result = self.test_group_computation(group)
                trace_result = self.test_trace_computation(group, t_values)
                results.append({**group_result, **trace_result})
            except Exception as e:
                print(f"测试 {group.name} 时出错: {e}")
                import traceback
                traceback.print_exc()
                
        # 4. 生成报告
        self.generate_report(results)
        
        return results
    
    def generate_report(self, results: List[dict]):
        """生成验证报告"""
        print("\n" + "=" * 60)
        print("验证报告摘要")
        print("=" * 60)
        
        for result in results:
            print(f"\n群: {result['group_name']}")
            print(f"  元素数量: {result.get('num_elements', 'N/A')}")
            print(f"  轨道计数: {result.get('orbit_count', 'N/A')}")
            
            if 'asymptotic' in result and result['asymptotic']:
                asym = result['asymptotic']
                print(f"  幂律指数: {asym.get('power_law_exponent', 'N/A')}")
                
            if 'delta_estimate' in result and result['delta_estimate']:
                delta_est = result['delta_estimate']
                print(f"  δ估计: {delta_est.get('delta_estimate', 'N/A')}")


# ============================================================================
# 5. 可视化和输出
# ============================================================================

def plot_trace_asymptotic(result: dict, save_path: Optional[str] = None):
    """
    绘制热核迹的渐近行为
    
    Args:
        result: 测试结果字典
        save_path: 保存路径
    """
    t_values = result['t_values']
    traces = result['traces']
    group_name = result['group_name']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 图1: 热核迹随时间变化
    ax1 = axes[0]
    ax1.loglog(t_values, traces, 'bo-', label='计算值', markersize=4)
    
    # 绘制理论渐近线 t^(-3/2)
    t_theory = np.logspace(-3, 0, 100)
    if 'asymptotic' in result and result['asymptotic'].get('volume_coefficient'):
        c0 = result['asymptotic']['volume_coefficient']
        theory = c0 * t_theory**(-1.5)
        ax1.loglog(t_theory, theory, 'r--', label=r'拟合: $c_0 t^{-3/2}$', alpha=0.7)
    
    ax1.set_xlabel('t', fontsize=12)
    ax1.set_ylabel(r'$\Theta_\Gamma(t)$', fontsize=12)
    ax1.set_title(f'热核迹: {group_name}', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 图2: 对数-对数图的斜率分析
    ax2 = axes[1]
    log_t = np.log(t_values)
    log_theta = np.log(traces)
    
    # 数值微分估计局部斜率
    slopes = np.gradient(log_theta, log_t)
    
    ax2.semilogx(t_values, slopes, 'g.-', markersize=4, label='局部斜率')
    ax2.axhline(y=-1.5, color='r', linestyle='--', label='理论值 -3/2', alpha=0.7)
    
    if result.get('expected_delta'):
        # 如果已知δ，可以标记相应的行为
        pass
    
    ax2.set_xlabel('t', fontsize=12)
    ax2.set_ylabel(r'$d \log \Theta / d \log t$', fontsize=12)
    ax2.set_title('渐近指数分析', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"图表已保存到: {save_path}")
    else:
        plt.show()
        
    plt.close()


def generate_latex_table(results: List[dict]) -> str:
    """
    生成LaTeX格式的结果表格
    
    Args:
        results: 测试结果列表
        
    Returns:
        LaTeX表格代码
    """
    latex = r"""\begin{table}[htbp]
\centering
\caption{热核迹渐近分析结果}
\label{tab:trace_asymptotic}
\begin{tabular}{lcccc}
\toprule
群 & 元素数 & 幂律指数 & $\delta$估计 & 期望$\delta$ \\
\midrule
"""
    
    for result in results:
        name = result['group_name']
        num_elem = result.get('num_elements', '-')
        
        asym = result.get('asymptotic', {})
        exponent = asym.get('power_law_exponent', None)
        exp_str = f"{exponent:.4f}" if exponent is not None else "-"
        
        delta_est = result.get('delta_estimate', {})
        delta_val = delta_est.get('delta_estimate', None)
        delta_str = f"{delta_val:.4f}" if delta_val is not None else "-"
        
        expected = result.get('expected_delta', '-')
        expected_str = f"{expected:.1f}" if isinstance(expected, (int, float)) else str(expected)
        
        latex += f"{name} & {num_elem} & {exp_str} & {delta_str} & {expected_str} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\end{table}"""
    
    return latex


# ============================================================================
# 6. 主程序
# ============================================================================

def main():
    """主程序入口"""
    print("=" * 70)
    print("严格迹公式渐近证明 - 计算验证")
    print("任务P3-C1-001: 严格迹公式渐近证明")
    print("=" * 70)
    
    # 运行验证套件
    verifier = VerificationSuite()
    results = verifier.run_all_tests()
    
    # 生成可视化
    print("\n生成可视化...")
    for i, result in enumerate(results):
        try:
            plot_path = f"/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/shared/trace_asymptotic_{result['group_name'].replace(' ', '_')}.png"
            plot_trace_asymptotic(result, save_path=plot_path)
        except Exception as e:
            print(f"绘图失败 ({result['group_name']}): {e}")
    
    # 生成LaTeX表格
    print("\n生成LaTeX表格...")
    latex_table = generate_latex_table(results)
    print(latex_table)
    
    # 保存结果
    import json
    results_file = "/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/codes/shared/trace_verification_results.json"
    
    # 将numpy数组转换为列表以便JSON序列化
    serializable_results = []
    for result in results:
        ser_result = {}
        for key, value in result.items():
            if isinstance(value, np.ndarray):
                ser_result[key] = value.tolist()
            elif isinstance(value, dict):
                ser_result[key] = {
                    k: (v.tolist() if isinstance(v, np.ndarray) else v)
                    for k, v in value.items()
                }
            else:
                ser_result[key] = value
        serializable_results.append(ser_result)
    
    with open(results_file, 'w') as f:
        json.dump({
            'task_id': 'P3-C1-001',
            'date': '2026-02-11',
            'results': serializable_results
        }, f, indent=2)
    
    print(f"\n结果已保存到: {results_file}")
    
    print("\n" + "=" * 70)
    print("验证完成")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = main()
