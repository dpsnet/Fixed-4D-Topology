#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤3: 变分原理证明与Gibbs测度构造

任务: P3-C2-001 - Gibbs测度存在性证明
功能:
    - Gibbs测度迭代构造
    - 变分原理验证
    - 熵计算
    - 唯一性检验
    - 压力函数分析

作者: Research Team
日期: 2026-02-11
版本: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig
from scipy.optimize import minimize_scalar
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Callable
from collections import defaultdict
import json
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# p-adic工具和多项式
# ============================================================================

class PAdicTools:
    """p-adic数计算工具"""
    
    @staticmethod
    def valuation(n: int, p: int) -> int:
        """计算p-adic赋值 v_p(n)"""
        if n == 0:
            return float('inf')
        v = 0
        temp = abs(n)
        while temp % p == 0 and temp > 0:
            temp //= p
            v += 1
        return v
    
    @staticmethod
    def abs_p(n: int, p: int) -> float:
        """计算p-adic绝对值 |n|_p = p^{-v_p(n)}"""
        return p ** (-PAdicTools.valuation(n, p))


@dataclass
class PAdicPoly:
    """p-adic多项式"""
    coeffs: List[int]
    p: int
    
    def evaluate(self, z: int) -> int:
        """在整数点求值"""
        result = 0
        for i, c in enumerate(self.coeffs):
            result += c * (z ** i)
        return result
    
    def derivative_coeffs(self) -> List[int]:
        """返回导数系数"""
        return [c * i for i, c in enumerate(self.coeffs) if i > 0]
    
    def derivative_at(self, z: int) -> float:
        """在整数点求导数值的p-adic绝对值"""
        deriv_coeffs = self.derivative_coeffs()
        if not deriv_coeffs:
            return 0.0
        
        result = 0
        for i, c in enumerate(deriv_coeffs):
            result += c * (z ** i)
        
        return PAdicTools.abs_p(int(result), self.p)
    
    def degree(self) -> int:
        """多项式次数"""
        for i in range(len(self.coeffs) - 1, -1, -1):
            if self.coeffs[i] != 0:
                return i
        return 0
    
    def iterate(self, z: int, n: int) -> int:
        """n次迭代"""
        result = z
        for _ in range(n):
            result = self.evaluate(result)
        return result
    
    def preimages(self, x: int, n: int = 1) -> List[int]:
        """
        计算n次原像（简化版本）
        对于z^d，原像为x^{1/d} * ζ_d^k
        """
        # 简化为在模p^k下搜索原像
        d = self.degree()
        preimages = []
        
        # 搜索范围
        search_range = min(100, self.p ** (n + 2))
        
        for y in range(-search_range, search_range + 1):
            if self.iterate(y, n) == x:
                preimages.append(y)
        
        return preimages
    
    def __repr__(self):
        terms = []
        for i, c in enumerate(self.coeffs):
            if c != 0:
                if i == 0:
                    terms.append(f"{c}")
                elif i == 1:
                    terms.append(f"{c}z")
                else:
                    terms.append(f"{c}z^{i}")
        return " + ".join(terms) if terms else "0"


# ============================================================================
# Gibbs测度迭代构造
# ============================================================================

@dataclass
class DiscreteMeasure:
    """离散测度表示"""
    points: np.ndarray  # 支撑点
    weights: np.ndarray  # 权重
    
    def __post_init__(self):
        # 归一化
        total = np.sum(self.weights)
        if total > 0:
            self.weights = self.weights / total
    
    def integrate(self, func: Callable[[np.ndarray], np.ndarray]) -> float:
        """积分计算"""
        values = func(self.points)
        return np.sum(values * self.weights)
    
    def entropy(self) -> float:
        """计算熵 H = -Σ w_i log w_i"""
        # 避免log(0)
        w = self.weights[self.weights > 1e-15]
        return -np.sum(w * np.log(w))
    
    def distance(self, other: 'DiscreteMeasure') -> float:
        """计算两个测度间的距离（简化）"""
        # 使用支撑点集差异作为距离
        common_points = set(self.points) & set(other.points)
        if not common_points:
            return 1.0
        
        # 计算权重差异
        max_diff = 0.0
        for p in common_points:
            idx1 = np.where(self.points == p)[0]
            idx2 = np.where(other.points == p)[0]
            if len(idx1) > 0 and len(idx2) > 0:
                diff = abs(self.weights[idx1[0]] - other.weights[idx2[0]])
                max_diff = max(max_diff, diff)
        
        return max_diff
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'points': self.points.tolist(),
            'weights': self.weights.tolist(),
            'entropy': float(self.entropy())
        }


class GibbsMeasureConstructor:
    """
    Gibbs测度构造器
    
    使用迭代方法构造Gibbs测度：
    μ_n = (1/Z_n) Σ_{y∈φ^{-n}(x_0)} e^{S_n φ(y)} δ_y
    
    其中 S_n φ(y) = Σ_{k=0}^{n-1} φ(φ^k(y))
    """
    
    def __init__(self, poly: PAdicPoly, s: float):
        self.poly = poly
        self.p = poly.p
        self.s = s
        self.d = poly.degree()
        
        # 势函数 φ(y) = -s * log|φ'(y)|_p
        self.potential = lambda y: -s * np.log(max(poly.derivative_at(int(y)), 1e-15))
    
    def compute_preimages(self, x: int, n: int) -> List[int]:
        """
        计算n次原像
        
        对于z^d，n次原像有d^n个。
        这里使用模运算简化计算。
        """
        if n == 0:
            return [x]
        
        # 简化的原像计算
        # 对于z^d，在p-adic单位球内搜索
        preimages = []
        d = self.d
        
        # 使用离散化搜索
        modulus = self.p ** (n + 3)
        
        for y in range(modulus):
            # 计算y的n次迭代
            val = y
            for _ in range(n):
                val = self.poly.evaluate(val) % modulus
            
            if val == x % modulus:
                preimages.append(y)
        
        return preimages[:d**n] if len(preimages) > d**n else preimages
    
    def birkhoff_sum(self, y: int, n: int) -> float:
        """
        计算Birkhoff和 S_n φ(y)
        
        S_n φ(y) = Σ_{k=0}^{n-1} φ(φ^k(y))
        """
        total = 0.0
        current = y
        
        for _ in range(n):
            total += self.potential(current)
            current = self.poly.evaluate(current)
        
        return total
    
    def construct_measure(self, x0: int, n: int) -> DiscreteMeasure:
        """
        构造n阶Gibbs测度逼近
        
        Args:
            x0: 初始点
            n: 迭代次数
            
        Returns:
            离散测度
        """
        # 计算n次原像
        preimages = self.compute_preimages(x0, n)
        
        if not preimages:
            # 返回退化测度
            return DiscreteMeasure(np.array([x0]), np.array([1.0]))
        
        # 计算权重
        points = np.array(preimages)
        weights = np.array([np.exp(self.birkhoff_sum(y, n)) for y in preimages])
        
        # 归一化
        return DiscreteMeasure(points, weights)
    
    def iterate_construction(self, x0: int, max_iter: int = 10,
                            tolerance: float = 1e-6) -> Dict:
        """
        迭代构造直到收敛
        
        Args:
            x0: 初始点
            max_iter: 最大迭代次数
            tolerance: 收敛容差
            
        Returns:
            收敛结果
        """
        measures = []
        converged = False
        
        for n in range(1, max_iter + 1):
            measure = self.construct_measure(x0, n)
            measures.append(measure)
            
            if n > 1:
                dist = measure.distance(measures[n-2])
                logger.info(f"迭代 {n}: 与上一阶距离 = {dist:.8f}")
                
                if dist < tolerance:
                    converged = True
                    logger.info(f"收敛于迭代 {n}")
                    break
        
        return {
            'measures': measures,
            'converged': converged,
            'final_measure': measures[-1] if measures else None,
            'num_iterations': len(measures)
        }
    
    def verify_gibbs_property(self, measure: DiscreteMeasure, 
                              n_test: int = 10) -> Dict:
        """
        验证Gibbs性质
        
        Gibbs不等式:
        1/C ≤ μ(φ^{-n}(D)) / exp(-nP + S_n φ(x)) ≤ C
        
        Args:
            measure: 测度
            n_test: 测试点数
            
        Returns:
            验证结果
        """
        # 简化的验证：检查测度质量分布的均匀性
        weights = measure.weights
        
        # 最大最小比
        w_max = np.max(weights)
        w_min = np.min(weights[weights > 0])
        ratio = w_max / w_min if w_min > 0 else float('inf')
        
        # 理论：Gibbs测度应满足特定的权重分布
        # 这里检查权重是否不过于分散
        is_gibbs_like = ratio < 100  # 启发式阈值
        
        return {
            'weight_ratio': float(ratio),
            'is_gibbs_like': is_gibbs_like,
            'max_weight': float(w_max),
            'min_weight': float(w_min),
            'entropy': float(measure.entropy())
        }


# ============================================================================
# 变分原理
# ============================================================================

class VariationalPrinciple:
    """
    变分原理验证
    
    核心等式:
    P(φ) = sup_{μ} {h_μ(φ) + ∫ φ dμ}
    
    其中:
    - P(φ) 是拓扑压力
    - h_μ(φ) 是测度熵
    - ∫ φ dμ 是势函数的积分
    """
    
    def __init__(self, poly: PAdicPoly):
        self.poly = poly
        self.p = poly.p
    
    def compute_pressure_via_partition(self, s: float, n: int = 8) -> float:
        """
        通过配分函数计算压力
        
        P(φ) = lim_{n→∞} (1/n) log Z_n
        
        Z_n = Σ_{x∈Fix(φ^n)} exp(S_n φ(x))
        
        Args:
            s: 维数参数
            n: 周期长度
            
        Returns:
            压力估计
        """
        # 构造Gibbs测度构造器
        constructor = GibbsMeasureConstructor(self.poly, s)
        
        # 计算周期点（简化：考虑0的n次原像）
        x0 = 0
        measure = constructor.construct_measure(x0, n)
        
        # 配分函数
        Z_n = np.sum(np.exp([constructor.birkhoff_sum(int(y), n) 
                             for y in measure.points]))
        
        # 压力
        pressure = np.log(max(Z_n, 1e-15)) / n
        
        return pressure
    
    def compute_measure_functional(self, measure: DiscreteMeasure, 
                                   s: float) -> float:
        """
        计算变分泛函
        
        F(μ) = h_μ(φ) + ∫ φ dμ
        
        Args:
            measure: 测度
            s: 维数参数
            
        Returns:
            泛函值
        """
        # 势函数
        potential = lambda y: -s * np.log(max(self.poly.derivative_at(int(y)), 1e-15))
        
        # 熵
        entropy = measure.entropy()
        
        # 势函数积分
        integral = measure.integrate(potential)
        
        return entropy + integral
    
    def verify_variational_principle(self, s: float, 
                                     n_iterations: int = 8) -> Dict:
        """
        验证变分原理
        
        检查：P(φ) ≈ h_μ + ∫ φ dμ 对于Gibbs测度μ
        
        Args:
            s: 维数参数
            n_iterations: 迭代次数
            
        Returns:
            验证结果
        """
        # 计算压力
        pressure = self.compute_pressure_via_partition(s, n_iterations)
        
        # 构造Gibbs测度
        constructor = GibbsMeasureConstructor(self.poly, s)
        result = constructor.iterate_construction(x0=0, max_iter=n_iterations)
        
        if result['final_measure'] is None:
            return {'error': 'Failed to construct measure'}
        
        measure = result['final_measure']
        
        # 计算变分泛函
        functional = self.compute_measure_functional(measure, s)
        
        # 比较
        difference = abs(pressure - functional)
        relative_error = difference / abs(pressure) if pressure != 0 else float('inf')
        
        return {
            's': s,
            'pressure': float(pressure),
            'entropy': float(measure.entropy()),
            'potential_integral': float(functional - measure.entropy()),
            'variational_functional': float(functional),
            'difference': float(difference),
            'relative_error': float(relative_error),
            'verified': relative_error < 0.1  # 10%容差
        }
    
    def find_equilibrium_state(self, s_range: Tuple[float, float] = (0.1, 3.0),
                               n_points: int = 20) -> Dict:
        """
        寻找平衡态（压力最大化测度）
        
        Args:
            s_range: s值范围
            n_points: 采样点数
            
        Returns:
            平衡态分析结果
        """
        s_values = np.linspace(s_range[0], s_range[1], n_points)
        
        results = {
            's_values': s_values.tolist(),
            'pressures': [],
            'entropies': [],
            'functionals': []
        }
        
        for s in s_values:
            verification = self.verify_variational_principle(s, n_iterations=6)
            
            results['pressures'].append(verification.get('pressure', 0))
            results['entropies'].append(verification.get('entropy', 0))
            results['functionals'].append(verification.get('variational_functional', 0))
        
        # 找到零点（Bowen公式）
        pressures = np.array(results['pressures'])
        idx_zero = np.argmin(np.abs(pressures))
        
        results['bowen_estimate'] = {
            'delta': float(s_values[idx_zero]),
            'pressure_at_delta': float(pressures[idx_zero])
        }
        
        return results


# ============================================================================
# 唯一性检验
# ============================================================================

class UniquenessTester:
    """Gibbs测度唯一性检验"""
    
    def __init__(self, poly: PAdicPoly, s: float):
        self.poly = poly
        self.s = s
        self.p = poly.p
    
    def test_initial_condition_dependence(self, 
                                          x0_list: List[int],
                                          n_iterations: int = 6) -> Dict:
        """
        检验对不同初始条件的依赖性
        
        唯一性意味着极限测度与初始点x_0无关
        
        Args:
            x0_list: 初始点列表
            n_iterations: 迭代次数
            
        Returns:
            检验结果
        """
        constructor = GibbsMeasureConstructor(self.poly, self.s)
        
        measures = []
        for x0 in x0_list:
            result = constructor.iterate_construction(
                x0=x0, max_iter=n_iterations, tolerance=1e-5
            )
            if result['final_measure'] is not None:
                measures.append(result['final_measure'])
        
        if len(measures) < 2:
            return {'error': 'Insufficient measures'}
        
        # 计算测度间距离
        distances = []
        for i in range(len(measures)):
            for j in range(i + 1, len(measures)):
                dist = measures[i].distance(measures[j])
                distances.append(dist)
        
        avg_distance = np.mean(distances)
        max_distance = np.max(distances)
        
        # 唯一性判断
        is_unique = max_distance < 0.1  # 启发式阈值
        
        return {
            'num_initial_points': len(x0_list),
            'num_measures': len(measures),
            'distances': distances,
            'average_distance': float(avg_distance),
            'max_distance': float(max_distance),
            'uniqueness_suggested': is_unique
        }
    
    def test_perturbation_stability(self, 
                                    base_measure: DiscreteMeasure,
                                    epsilon: float = 0.1) -> Dict:
        """
        检验扰动稳定性
        
        Gibbs测度应该是稳定的
        
        Args:
            base_measure: 基础测度
            epsilon: 扰动大小
            
        Returns:
            稳定性结果
        """
        # 创建扰动测度
        perturbed_weights = base_measure.weights * (1 + epsilon * np.random.randn(
            len(base_measure.weights)))
        perturbed_weights = np.abs(perturbed_weights)
        perturbed_weights = perturbed_weights / np.sum(perturbed_weights)
        
        perturbed_measure = DiscreteMeasure(
            base_measure.points.copy(),
            perturbed_weights
        )
        
        # 计算距离
        distance = base_measure.distance(perturbed_measure)
        
        # 变分泛函值
        variational = VariationalPrinciple(self.poly)
        base_functional = variational.compute_measure_functional(base_measure, self.s)
        perturbed_functional = variational.compute_measure_functional(
            perturbed_measure, self.s
        )
        
        # Gibbs测度应使泛函最大化
        is_maximum = base_functional >= perturbed_functional
        
        return {
            'perturbation_size': epsilon,
            'measure_distance': float(distance),
            'base_functional': float(base_functional),
            'perturbed_functional': float(perturbed_functional),
            'functional_decrease': float(base_functional - perturbed_functional),
            'is_maximum': is_maximum
        }


# ============================================================================
# 可视化
# ============================================================================

class VariationalVisualizer:
    """变分原理可视化"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def plot_pressure_function(self, variational: VariationalPrinciple,
                               s_range: Tuple[float, float] = (0.1, 3.0),
                               n_points: int = 30,
                               save_path: Optional[str] = None):
        """
        绘制压力函数
        """
        s_values = np.linspace(s_range[0], s_range[1], n_points)
        pressures = []
        entropies = []
        
        for s in s_values:
            verification = variational.verify_variational_principle(s, n_iterations=6)
            pressures.append(verification.get('pressure', 0))
            entropies.append(verification.get('entropy', 0))
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # 压力函数
        ax = axes[0]
        ax.plot(s_values, pressures, 'b-', linewidth=2, label='P(s)')
        ax.axhline(y=0, color='r', linestyle='--', label='P(s)=0')
        
        # 找到零点
        pressures_arr = np.array(pressures)
        idx_zero = np.argmin(np.abs(pressures_arr))
        ax.scatter([s_values[idx_zero]], [pressures[idx_zero]], 
                  color='red', s=100, zorder=5, label=f'δ ≈ {s_values[idx_zero]:.3f}')
        
        ax.set_xlabel('s (Dimension parameter)')
        ax.set_ylabel('P(s)')
        ax.set_title(f'Pressure Function (p={variational.poly.p})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 熵
        ax = axes[1]
        ax.plot(s_values, entropies, 'g-', linewidth=2, label='h(s)')
        ax.set_xlabel('s (Dimension parameter)')
        ax.set_ylabel('Entropy')
        ax.set_title('Measure Entropy')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"压力函数图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_measure_convergence(self, constructor: GibbsMeasureConstructor,
                                 x0: int,
                                 save_path: Optional[str] = None):
        """
        绘制测度收敛过程
        """
        result = constructor.iterate_construction(x0=x0, max_iter=8)
        
        if not result['measures']:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 收敛的熵
        ax = axes[0, 0]
        entropies = [m.entropy() for m in result['measures']]
        iterations = range(1, len(entropies) + 1)
        ax.plot(iterations, entropies, 'bo-', linewidth=2)
        ax.set_xlabel('Iteration n')
        ax.set_ylabel('Entropy')
        ax.set_title('Entropy Convergence')
        ax.grid(True, alpha=0.3)
        
        # 测度支撑大小
        ax = axes[0, 1]
        support_sizes = [len(m.points) for m in result['measures']]
        ax.semilogy(iterations, support_sizes, 'ro-', linewidth=2)
        ax.set_xlabel('Iteration n')
        ax.set_ylabel('Support Size (log scale)')
        ax.set_title('Measure Support Growth')
        ax.grid(True, alpha=0.3)
        
        # 最终测度的权重分布
        ax = axes[1, 0]
        final_measure = result['final_measure']
        if final_measure is not None:
            ax.bar(range(len(final_measure.weights)), 
                  sorted(final_measure.weights, reverse=True))
            ax.set_xlabel('Point Index (sorted)')
            ax.set_ylabel('Weight')
            ax.set_title('Final Measure Weight Distribution')
        
        # 信息汇总
        ax = axes[1, 1]
        ax.axis('off')
        
        info_text = f"""
        Gibbs Measure Construction
        =========================
        
        Polynomial: {constructor.poly}
        p = {constructor.p}, s = {constructor.s}
        
        Converged: {result['converged']}
        Iterations: {result['num_iterations']}
        
        Final Entropy: {entropies[-1]:.4f}
        Final Support: {support_sizes[-1]}
        
        Convergence Check:
        - Entropy stable: {abs(entropies[-1] - entropies[-2]) < 0.01 if len(entropies) > 1 else 'N/A'}
        """
        ax.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
               verticalalignment='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"测度收敛图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()


# ============================================================================
# 主程序
# ============================================================================

def test_variational_principle():
    """测试变分原理"""
    print("=" * 70)
    print("步骤3: 变分原理验证测试")
    print("=" * 70)
    
    # 测试多项式
    test_cases = [
        (PAdicPoly([0, 0, 1], 2), 1.0, "z² (p=2, s=1.0)"),
        (PAdicPoly([0, 0, 1], 3), 1.0, "z² (p=3, s=1.0)"),
        (PAdicPoly([0, 0, 1], 2), 1.5, "z² (p=2, s=1.5)"),
    ]
    
    results = {}
    
    for poly, s, name in test_cases:
        print(f"\n{'-'*50}")
        print(f"测试: {name}")
        print(f"{'-'*50}")
        
        # Gibbs测度构造
        constructor = GibbsMeasureConstructor(poly, s)
        result = constructor.iterate_construction(x0=0, max_iter=6)
        
        print(f"收敛: {result['converged']}")
        print(f"迭代次数: {result['num_iterations']}")
        
        if result['final_measure'] is not None:
            measure = result['final_measure']
            print(f"最终测度熵: {measure.entropy():.4f}")
            print(f"支撑点数: {len(measure.points)}")
            
            # 验证Gibbs性质
            gibbs_check = constructor.verify_gibbs_property(measure)
            print(f"Gibbs性质检验:")
            print(f"  权重比: {gibbs_check['weight_ratio']:.4f}")
            print(f"  类似Gibbs: {gibbs_check['is_gibbs_like']}")
        
        # 变分原理验证
        variational = VariationalPrinciple(poly)
        vp_result = variational.verify_variational_principle(s, n_iterations=6)
        
        print(f"变分原理验证:")
        print(f"  压力 P(s): {vp_result.get('pressure', 0):.4f}")
        print(f"  变分泛函: {vp_result.get('variational_functional', 0):.4f}")
        print(f"  差值: {vp_result.get('difference', 0):.6f}")
        print(f"  验证通过: {vp_result.get('verified', False)}")
        
        # 唯一性检验
        uniqueness = UniquenessTester(poly, s)
        unique_result = uniqueness.test_initial_condition_dependence(
            x0_list=[0, 1, 2, 3], n_iterations=5
        )
        
        print(f"唯一性检验:")
        print(f"  平均距离: {unique_result.get('average_distance', 0):.6f}")
        print(f"  最大距离: {unique_result.get('max_distance', 0):.6f}")
        print(f"  建议唯一性: {unique_result.get('uniqueness_suggested', False)}")
        
        results[name] = {
            'gibbs_construction': {
                'converged': result['converged'],
                'num_iterations': result['num_iterations'],
                'entropy': float(measure.entropy()) if result['final_measure'] else None
            },
            'variational_principle': vp_result,
            'uniqueness': unique_result
        }
    
    return results


def main():
    """主函数"""
    print("=" * 70)
    print("步骤3: 变分原理证明与Gibbs测度构造")
    print("任务: P3-C2-001")
    print("=" * 70)
    
    # 运行测试
    results = test_variational_principle()
    
    # 保存结果
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / "step3_variational_results.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"结果已保存: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
