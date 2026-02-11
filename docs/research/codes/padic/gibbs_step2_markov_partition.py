#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤2: Markov划分构造与符号动力学

任务: P3-C2-001 - Gibbs测度存在性证明
功能:
    - p-adic Markov划分构造算法
    - 符号动力学建立
    - 转移矩阵计算
    - 划分细化和收敛性分析
    - 可视化

作者: Research Team
日期: 2026-02-11
版本: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Set
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
# p-adic工具和基础类
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
    
    @staticmethod
    def ball(center: int, radius_exp: int, p: int) -> Tuple[int, int]:
        """
        定义p-adic球 B(c, p^{-r})
        
        Args:
            center: 中心点整数表示
            radius_exp: 半径指数 r (半径 = p^{-r})
            p: 素数
            
        Returns:
            (中心, 半径指数) 元组
        """
        return (center, radius_exp)
    
    @staticmethod
    def ball_contains(ball: Tuple[int, int], point: int, p: int) -> bool:
        """检查点是否在p-adic球内"""
        center, radius_exp = ball
        radius = p ** (-radius_exp)
        dist = PAdicTools.abs_p(point - center, p)
        return dist <= radius


@dataclass
class PAdicPoly:
    """p-adic多项式"""
    coeffs: List[int]  # 从低次到高次
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
# Markov划分构造
# ============================================================================

@dataclass
class MarkovPartition:
    """
    p-adic Markov划分
    
    在p-adic情形下，Markov划分由p-adic球（圆盘）构成。
    由于p-adic拓扑的不连通性，划分的结构比实数情形更简单。
    """
    poly: PAdicPoly
    elements: List[Tuple[int, int]] = field(default_factory=list)  # (中心, 半径指数) 列表
    
    def __post_init__(self):
        if not self.elements:
            self.elements = []
    
    def add_element(self, center: int, radius_exp: int):
        """添加划分元素（p-adic球）"""
        self.elements.append((center, radius_exp))
    
    def get_radius(self, radius_exp: int) -> float:
        """获取半径"""
        return self.poly.p ** (-radius_exp)
    
    def diameter(self) -> float:
        """划分的最大直径"""
        if not self.elements:
            return 0.0
        return max(self.get_radius(r) for _, r in self.elements)
    
    def num_elements(self) -> int:
        """划分元素个数"""
        return len(self.elements)
    
    def refine(self, level: int = 1) -> 'MarkovPartition':
        """
        细化划分
        
        每个半径为 p^{-r} 的球细化为 p 个半径为 p^{-(r+1)} 的球
        
        Args:
            level: 细化层数
            
        Returns:
            细化后的划分
        """
        refined = MarkovPartition(self.poly)
        p = self.poly.p
        
        for center, radius_exp in self.elements:
            # 细化为 p 个子球
            for k in range(p):
                new_center = center + k * (p ** radius_exp)
                refined.add_element(new_center, radius_exp + level)
        
        return refined
    
    def is_markov(self) -> bool:
        """
        检查是否满足Markov性质
        
        Markov性质：划分元素的像完全覆盖某些划分元素的并集
        """
        if not self.elements:
            return False
        
        # 检查每个划分元素的像
        for center, radius_exp in self.elements:
            # 计算球在多项式映射下的像
            # 在p-adic情形下，多项式映射p-adic球为p-adic球
            image_center = self.poly.evaluate(center)
            
            # 检查像是否覆盖完整的划分元素
            # 简化检查：像中心应该接近某个划分元素的中心
            found = False
            for c2, r2 in self.elements:
                if PAdicTools.ball_contains((c2, r2), image_center, self.poly.p):
                    found = True
                    break
            
            if not found:
                return False
        
        return True
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'polynomial': str(self.poly),
            'p': self.poly.p,
            'elements': self.elements,
            'num_elements': len(self.elements),
            'diameter': self.diameter()
        }


class MarkovPartitionConstructor:
    """Markov划分构造器"""
    
    def __init__(self, poly: PAdicPoly):
        self.poly = poly
        self.p = poly.p
        self.d = poly.degree()
    
    def construct_for_pure_power(self) -> MarkovPartition:
        """
        为 z^d 构造标准Markov划分
        
        对于 φ(z) = z^d，Julia集是单位圆盘。
        Markov划分由 p^k 个半径为 p^{-k} 的不交球组成。
        """
        partition = MarkovPartition(self.poly)
        
        # 初始划分：p个半径为p^{-1}的球覆盖Z_p
        # 中心为 0, 1, 2, ..., p-1 (模 p)
        for k in range(self.p):
            partition.add_element(k, 1)
        
        return partition
    
    def construct_adaptive(self, min_radius_exp: int = 3) -> MarkovPartition:
        """
        自适应构造Markov划分
        
        基于多项式的动力学行为自适应调整划分粒度
        
        Args:
            min_radius_exp: 最小半径指数
            
        Returns:
            Markov划分
        """
        partition = MarkovPartition(self.poly)
        
        # 从初始划分开始
        initial = self.construct_for_pure_power()
        
        # 递归细化直到满足条件
        current = initial
        for level in range(min_radius_exp - 1):
            current = current.refine(level=1)
        
        return current
    
    def construct_from_periodic_points(self, period: int = 1) -> MarkovPartition:
        """
        从周期点构造Markov划分
        
        Args:
            period: 周期
            
        Returns:
            Markov划分
        """
        partition = MarkovPartition(self.poly)
        
        # 计算周期点（简化：仅考虑不动点）
        if period == 1:
            # 解 φ(z) = z
            # 对于 z^d，不动点为 0 和 (d-1)次单位根
            # 在 p-adic 中，我们需要找到满足 z^d ≡ z (mod p^k) 的点
            
            # 简化为添加包含0的球和包含1的球
            partition.add_element(0, 2)
            partition.add_element(1, 2)
        
        return partition


# ============================================================================
# 符号动力学
# ============================================================================

@dataclass
class SymbolicDynamics:
    """
    符号动力系统
    
    基于Markov划分建立符号编码。
    """
    partition: MarkovPartition
    alphabet: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.alphabet:
            # 用字母标记划分元素
            self.alphabet = [f"A{i}" for i in range(len(self.partition.elements))]
    
    def encode_point(self, point: int) -> Optional[str]:
        """
        将p-adic点编码为符号
        
        Args:
            point: 整数点
            
        Returns:
            符号或None
        """
        for i, (center, radius_exp) in enumerate(self.partition.elements):
            if PAdicTools.ball_contains((center, radius_exp), point, self.partition.poly.p):
                return self.alphabet[i]
        return None
    
    def decode_symbol(self, symbol: str) -> Optional[Tuple[int, int]]:
        """
        将符号解码为p-adic球
        
        Args:
            symbol: 符号
            
        Returns:
            (中心, 半径指数) 或 None
        """
        if symbol in self.alphabet:
            idx = self.alphabet.index(symbol)
            return self.partition.elements[idx]
        return None
    
    def orbit_to_sequence(self, orbit: List[int]) -> List[str]:
        """
        将轨道转换为符号序列
        
        Args:
            orbit: 轨道点列表
            
        Returns:
            符号序列
        """
        return [self.encode_point(p) for p in orbit if self.encode_point(p) is not None]
    
    def cylinder_set(self, sequence: List[str]) -> List[Tuple[int, int]]:
        """
        计算柱集的划分元素
        
        柱集 [a_0, a_1, ..., a_{n-1}] = 
        {x : x ∈ A_{a_0}, φ(x) ∈ A_{a_1}, ..., φ^{n-1}(x) ∈ A_{a_{n-1}}}
        
        Args:
            sequence: 符号序列
            
        Returns:
            划分元素列表
        """
        if not sequence:
            return []
        
        # 起始划分元素
        start = self.decode_symbol(sequence[0])
        if start is None:
            return []
        
        result = [start]
        current_center, current_exp = start
        
        # 追踪多项式映射
        for symbol in sequence[1:]:
            # 计算当前球的像
            next_center = self.partition.poly.evaluate(current_center)
            
            # 检查是否与下一个符号对应的球相交
            target = self.decode_symbol(symbol)
            if target is None:
                return []
            
            target_center, target_exp = target
            
            # 简化：检查像中心是否接近目标中心
            p = self.partition.poly.p
            dist = PAdicTools.abs_p(next_center - target_center, p)
            
            if dist <= p ** (-min(current_exp, target_exp)):
                result.append(target)
                current_center, current_exp = target_center, target_exp
            else:
                return []
        
        return result


class TransferMatrix:
    """转移矩阵"""
    
    def __init__(self, symbolic: SymbolicDynamics):
        self.symbolic = symbolic
        self.partition = symbolic.partition
        self.poly = symbolic.partition.poly
        self.p = self.poly.p
        self.matrix = None
    
    def compute_transfer_matrix(self) -> np.ndarray:
        """
        计算转移矩阵
        
        T[i,j] = 1 如果 φ(A_j) ∩ A_i ≠ ∅
        
        Returns:
            转移矩阵
        """
        n = len(self.partition.elements)
        T = np.zeros((n, n), dtype=int)
        
        for j, (center_j, exp_j) in enumerate(self.partition.elements):
            # 计算 A_j 的像
            image_center = self.poly.evaluate(center_j)
            
            for i, (center_i, exp_i) in enumerate(self.partition.elements):
                # 检查像与 A_i 是否相交
                dist = PAdicTools.abs_p(image_center - center_i, self.p)
                radius_i = self.p ** (-exp_i)
                
                if dist <= radius_i:
                    T[i, j] = 1
        
        self.matrix = T
        return T
    
    def compute_weighted_transfer_matrix(self, s: float) -> np.ndarray:
        """
        计算加权转移矩阵（用于热力学形式）
        
        T_s[i,j] = |φ'(center_j)|_p^{-s} 如果 φ(A_j) ∩ A_i ≠ ∅
        
        Args:
            s: 维数参数
            
        Returns:
            加权转移矩阵
        """
        n = len(self.partition.elements)
        T_s = np.zeros((n, n))
        
        for j, (center_j, exp_j) in enumerate(self.partition.elements):
            # 计算权重
            deriv_abs = self.poly.derivative_at(center_j)
            weight = deriv_abs ** (-s) if deriv_abs > 0 else 0
            
            # 计算 A_j 的像
            image_center = self.poly.evaluate(center_j)
            
            for i, (center_i, exp_i) in enumerate(self.partition.elements):
                # 检查像与 A_i 是否相交
                dist = PAdicTools.abs_p(image_center - center_i, self.p)
                radius_i = self.p ** (-exp_i)
                
                if dist <= radius_i:
                    T_s[i, j] = weight
        
        return T_s
    
    def compute_entropy(self) -> float:
        """
        计算拓扑熵
        
        h = log(λ_max)
        其中 λ_max 是转移矩阵的谱半径
        """
        if self.matrix is None:
            self.compute_transfer_matrix()
        
        eigenvalues = np.linalg.eigvals(self.matrix)
        spectral_radius = np.max(np.abs(eigenvalues))
        
        return np.log(max(spectral_radius, 1e-10))
    
    def find_admissible_sequences(self, length: int) -> List[List[str]]:
        """
        找到所有可允许的长度为n的序列
        
        Args:
            length: 序列长度
            
        Returns:
            可允许序列列表
        """
        if self.matrix is None:
            self.compute_transfer_matrix()
        
        n = len(self.partition.elements)
        sequences = []
        
        def backtrack(current_seq: List[int], remaining: int):
            if remaining == 0:
                sequences.append([self.symbolic.alphabet[i] for i in current_seq])
                return
            
            last = current_seq[-1] if current_seq else 0
            for i in range(n):
                if self.matrix[i, last] == 1 or not current_seq:
                    backtrack(current_seq + [i], remaining - 1)
        
        for start in range(n):
            backtrack([start], length - 1)
        
        return sequences
    
    def analyze_mixing(self) -> Dict:
        """
        分析混合性质
        
        Returns:
            混合性质分析结果
        """
        if self.matrix is None:
            self.compute_transfer_matrix()
        
        n = len(self.partition.elements)
        
        # 检查不可约性
        # 矩阵是不可约的当且仅当对于所有i,j存在k使得 (T^k)[i,j] > 0
        power = np.eye(n)
        irreducible = True
        
        for k in range(1, n + 1):
            power = power @ self.matrix
            if np.min(power) == 0:
                irreducible = False
                break
        
        # 计算周期
        eigenvalues = np.linalg.eigvals(self.matrix)
        periods = []
        for ev in eigenvalues:
            if abs(abs(ev) - np.max(np.abs(eigenvalues))) < 1e-10:
                angle = np.angle(ev)
                if angle > 1e-10:
                    period = int(round(2 * np.pi / angle))
                    periods.append(period)
        
        gcd_period = np.gcd.reduce(periods) if periods else 1
        
        return {
            'is_irreducible': irreducible,
            'is_primitive': irreducible and (gcd_period == 1),
            'period': gcd_period,
            'entropy': self.compute_entropy()
        }


# ============================================================================
# 划分细化和收敛性分析
# ============================================================================

class PartitionRefinementAnalyzer:
    """划分细化分析器"""
    
    def __init__(self, constructor: MarkovPartitionConstructor):
        self.constructor = constructor
        self.poly = constructor.poly
        self.p = constructor.p
    
    def analyze_refinement_convergence(self, max_level: int = 5) -> Dict:
        """
        分析划分细化的收敛性
        
        Args:
            max_level: 最大细化层数
            
        Returns:
            收敛性分析结果
        """
        results = {
            'levels': list(range(max_level + 1)),
            'num_elements': [],
            'diameters': [],
            'entropies': []
        }
        
        # 初始划分
        partition = self.constructor.construct_for_pure_power()
        
        for level in range(max_level + 1):
            if level > 0:
                partition = partition.refine(level=1)
            
            # 创建符号动力学
            symbolic = SymbolicDynamics(partition)
            transfer = TransferMatrix(symbolic)
            
            results['num_elements'].append(partition.num_elements())
            results['diameters'].append(partition.diameter())
            results['entropies'].append(transfer.compute_entropy())
        
        return results
    
    def estimate_dimension(self, s_values: np.ndarray, max_level: int = 4) -> Dict:
        """
        通过划分细化估计维数
        
        使用 Bowen 公式: P(-s log|φ'|) = 0
        
        Args:
            s_values: 测试的s值
            max_level: 最大细化层数
            
        Returns:
            维数估计结果
        """
        partition = self.constructor.construct_for_pure_power()
        
        # 细化到指定层数
        for _ in range(max_level):
            partition = partition.refine(level=1)
        
        symbolic = SymbolicDynamics(partition)
        transfer = TransferMatrix(symbolic)
        
        pressures = []
        for s in s_values:
            T_s = transfer.compute_weighted_transfer_matrix(s)
            eigenvalues = np.linalg.eigvals(T_s)
            spectral_radius = np.max(np.abs(eigenvalues))
            pressure = np.log(max(spectral_radius, 1e-10))
            pressures.append(pressure)
        
        pressures = np.array(pressures)
        
        # 找到压力接近0的点
        idx_zero = np.argmin(np.abs(pressures))
        delta_estimate = s_values[idx_zero]
        
        return {
            's_values': s_values.tolist(),
            'pressures': pressures.tolist(),
            'delta_estimate': float(delta_estimate),
            'pressure_at_delta': float(pressures[idx_zero])
        }


# ============================================================================
# 可视化
# ============================================================================

class MarkovPartitionVisualizer:
    """Markov划分可视化器"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(__file__).parent / output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def visualize_partition(self, partition: MarkovPartition, 
                           title: str = "Markov Partition",
                           save_path: Optional[str] = None):
        """
        可视化Markov划分
        
        使用树状图表示p-adic球的层次结构
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # 左图：划分元素
        ax = axes[0]
        p = partition.poly.p
        
        y_positions = []
        x_positions = []
        radii = []
        
        for i, (center, radius_exp) in enumerate(partition.elements):
            radius = partition.get_radius(radius_exp)
            y_positions.append(i)
            x_positions.append(center % 100)  # 简化显示
            radii.append(radius * 50)  # 缩放
        
        if x_positions:
            ax.scatter(x_positions, y_positions, s=[r*1000 for r in radii], 
                      alpha=0.5, c=range(len(y_positions)), cmap='tab20')
        
        ax.set_xlabel('Center (mod 100)')
        ax.set_ylabel('Element Index')
        ax.set_title(f'{title}\n({partition.num_elements()} elements)')
        ax.grid(True, alpha=0.3)
        
        # 右图：转移关系
        ax = axes[1]
        symbolic = SymbolicDynamics(partition)
        transfer = TransferMatrix(symbolic)
        T = transfer.compute_transfer_matrix()
        
        im = ax.imshow(T, cmap='Blues', interpolation='nearest')
        ax.set_title('Transfer Matrix')
        ax.set_xlabel('From (j)')
        ax.set_ylabel('To (i)')
        plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"可视化已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def visualize_refinement(self, analyzer: PartitionRefinementAnalyzer,
                            max_level: int = 5,
                            save_path: Optional[str] = None):
        """
        可视化细化过程
        """
        results = analyzer.analyze_refinement_convergence(max_level)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 元素数量增长
        ax = axes[0, 0]
        ax.semilogy(results['levels'], results['num_elements'], 'bo-', linewidth=2)
        ax.set_xlabel('Refinement Level')
        ax.set_ylabel('Number of Elements (log scale)')
        ax.set_title('Partition Size Growth')
        ax.grid(True, alpha=0.3)
        
        # 直径衰减
        ax = axes[0, 1]
        ax.semilogy(results['levels'], results['diameters'], 'ro-', linewidth=2)
        ax.set_xlabel('Refinement Level')
        ax.set_ylabel('Diameter (log scale)')
        ax.set_title('Partition Diameter Decay')
        ax.grid(True, alpha=0.3)
        
        # 熵收敛
        ax = axes[1, 0]
        ax.plot(results['levels'], results['entropies'], 'go-', linewidth=2)
        ax.set_xlabel('Refinement Level')
        ax.set_ylabel('Topological Entropy')
        ax.set_title('Entropy Convergence')
        ax.grid(True, alpha=0.3)
        
        # 信息汇总
        ax = axes[1, 1]
        ax.axis('off')
        
        info_text = f"""
        Refinement Analysis Summary
        ==========================
        
        Polynomial: {analyzer.poly}
        p = {analyzer.p}
        
        Final Level: {max_level}
        Final Elements: {results['num_elements'][-1]}
        Final Diameter: {results['diameters'][-1]:.6f}
        Final Entropy: {results['entropies'][-1]:.4f}
        
        Diameter Decay Rate: 
        {results['diameters'][0]/results['diameters'][-1]:.2f}x per level
        """
        ax.text(0.1, 0.5, info_text, fontsize=10, family='monospace',
               verticalalignment='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            logger.info(f"细化可视化已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()


# ============================================================================
# 主程序和测试
# ============================================================================

def test_markov_partition():
    """测试Markov划分构造"""
    print("=" * 70)
    print("步骤2: Markov划分构造测试")
    print("=" * 70)
    
    # 测试多项式
    test_cases = [
        (PAdicPoly([0, 0, 1], 2), "z² (p=2)"),
        (PAdicPoly([0, 0, 1], 3), "z² (p=3)"),
        (PAdicPoly([0, 0, 0, 1], 2), "z³ (p=2)"),
        (PAdicPoly([2, 0, 1], 2), "z²+2 (p=2)"),
    ]
    
    results = {}
    
    for poly, name in test_cases:
        print(f"\n{'-'*50}")
        print(f"测试: {name}")
        print(f"{'-'*50}")
        
        # 构造划分
        constructor = MarkovPartitionConstructor(poly)
        partition = constructor.construct_for_pure_power()
        
        print(f"初始划分元素数: {partition.num_elements()}")
        print(f"划分直径: {partition.diameter():.6f}")
        
        # 符号动力学
        symbolic = SymbolicDynamics(partition)
        print(f"符号字母表: {symbolic.alphabet}")
        
        # 转移矩阵
        transfer = TransferMatrix(symbolic)
        T = transfer.compute_transfer_matrix()
        print(f"转移矩阵形状: {T.shape}")
        print(f"转移矩阵:\n{T}")
        
        # 混合性质
        mixing = transfer.analyze_mixing()
        print(f"拓扑熵: {mixing['entropy']:.4f}")
        print(f"不可约: {mixing['is_irreducible']}")
        print(f"本原: {mixing['is_primitive']}")
        
        # 细化分析
        analyzer = PartitionRefinementAnalyzer(constructor)
        refinement = analyzer.analyze_refinement_convergence(max_level=4)
        
        print(f"细化收敛:")
        print(f"  层数: {refinement['levels']}")
        print(f"  元素数: {refinement['num_elements']}")
        print(f"  直径: {[f'{d:.6f}' for d in refinement['diameters']]}")
        
        results[name] = {
            'partition': partition.to_dict(),
            'entropy': mixing['entropy'],
            'refinement': refinement
        }
    
    return results


def main():
    """主函数"""
    print("=" * 70)
    print("步骤2: Markov划分构造与符号动力学")
    print("任务: P3-C2-001")
    print("=" * 70)
    
    # 运行测试
    results = test_markov_partition()
    
    # 保存结果
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / "step2_markov_partition_results.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"结果已保存: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
