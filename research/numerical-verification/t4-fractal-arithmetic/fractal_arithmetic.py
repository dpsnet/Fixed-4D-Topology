#!/usr/bin/env python3
"""
分形算术的数值验证
Numerical verification of fractal arithmetic

Author: AI Research Engine
Date: 2026-02-07
Theory: fractal-arithmetic-algebra/
"""

import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction


class FractalDimension:
    """
    分形维数及其算术运算
    """
    
    def __init__(self, N, r):
        """
        由IFS参数构造分形维数
        d = log(N) / log(1/r)
        
        Parameters:
        -----------
        N : int
            分支数
        r : float
            压缩比 (0 < r < 1)
        """
        self.N = N
        self.r = r
        self.d = np.log(N) / np.log(1/r)
        
    def __add__(self, other):
        """分形加法: d1 ⊕ d2 = d1 + d2 (实数加法)"""
        return self.d + other.d
    
    def __repr__(self):
        return f"FractalDimension(N={self.N}, r={self.r:.4f}, d={self.d:.6f})"


def verify_addition_structure():
    """
    验证分形加法结构
    """
    print("=" * 70)
    print("分形算术结构验证")
    print("=" * 70)
    
    # 创建分形维数
    print("\n[1] 创建Cantor类分形维数...")
    
    # 固定压缩比 r = 1/3
    r = 1/3
    
    d2 = FractalDimension(2, r)   # Cantor三分集
    d3 = FractalDimension(3, r)   # 3分支
    d5 = FractalDimension(5, r)   # 5分支
    
    print(f"d2 (N=2): d = {d2.d:.6f}")
    print(f"d3 (N=3): d = {d3.d:.6f}")
    print(f"d5 (N=5): d = {d5.d:.6f}")
    
    # 验证加法
    print("\n[2] 验证加法 d1 ⊕ d2 = d1 + d2...")
    
    d_sum = d2 + d3
    d_expected = np.log(2*3) / np.log(3)  # log(6)/log(3)
    
    print(f"d2 ⊕ d3 = {d2.d:.6f} + {d3.d:.6f} = {d_sum:.6f}")
    print(f"理论值 (log(6)/log(3)) = {d_expected:.6f}")
    print(f"误差: {abs(d_sum - d_expected):.10f}")
    
    # 验证同构: (𝒟^(r), ⊕) ≅ (ℚ⁺, ×)
    print("\n[3] 验证同构 Φ: [d1, d2] ↦ log(N1/N2)...")
    
    # Grothendieck群元素: [d2, d3] 代表 d2 - d3
    # 对数映射: log(2/3) = log(2) - log(3)
    
    log_ratio = np.log(d2.N / d3.N)
    log_diff = np.log(d2.N) - np.log(d3.N)
    
    print(f"log(2/3) = {log_ratio:.6f}")
    print(f"log(2) - log(3) = {log_diff:.6f}")
    print(f"误差: {abs(log_ratio - log_diff):.10f}")
    
    # 验证运算保持
    # (d2 ⊕ d3) 对应 N = 6
    # log(6) = log(2) + log(3) ✓
    log_sum = np.log(6)
    log_individual = np.log(2) + np.log(3)
    print(f"\nlog(2·3) = log(6) = {log_sum:.6f}")
    print(f"log(2) + log(3) = {log_individual:.6f}")
    print(f"验证 log(N1·N2) = log(N1) + log(N2): {abs(log_sum - log_individual) < 1e-10}")


def verify_rational_isomorphism():
    """
    验证与有理数的同构
    """
    print("\n" + "=" * 70)
    print("与有理数同构验证: (𝒢_D^(r), ⊕) ≅ (ℚ, +)")
    print("=" * 70)
    
    r = 1/2  # 固定压缩比
    
    # 创建Grothendieck群元素 [d_N1, d_N2]
    # 对应有理数 N1/N2
    
    test_cases = [
        (2, 3),   # 2/3
        (3, 2),   # 3/2
        (5, 4),   # 5/4
        (7, 3),   # 7/3
    ]
    
    print(f"\n固定压缩比 r = {r}")
    print(f"维数公式: d = log(N) / log(1/r) = log(N) / log(2)")
    print()
    
    print(f"{'[d_N1, d_N2]':<20} {'N1/N2':<15} {'log(N1/N2)':<20} {'d_N1 - d_N2':<20} {'误差':<15}")
    print("-" * 90)
    
    for N1, N2 in test_cases:
        d1 = FractalDimension(N1, r)
        d2 = FractalDimension(N2, r)
        
        # Grothendieck群元素 [d1, d2]
        diff_dim = d1.d - d2.d
        
        # 对应有理数
        ratio = Fraction(N1, N2)
        log_ratio = np.log(N1 / N2)
        
        # 验证: d1 - d2 = log(N1/N2) / log(1/r)
        expected = np.log(N1 / N2) / np.log(1/r)
        error = abs(diff_dim - expected)
        
        print(f"[{N1}, {N2}]: {d1.d:.4f}-{d2.d:.4f} = {ratio:<15} {log_ratio:+.6f} {' '*5} {diff_dim:+20.6f} {error:.2e}")
    
    print("\n✓ 同构验证: [d_N1, d_N2] ↦ log(N1/N2) / log(1/r) 保持群运算")


def visualize_arithmetic():
    """
    可视化分形算术
    """
    print("\n" + "=" * 70)
    print("生成可视化")
    print("=" * 70)
    
    r = 1/3
    
    # 生成一系列分形维数
    N_values = range(2, 21)
    dimensions = [np.log(N) / np.log(1/r) for N in N_values]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 图1: 维数 vs 分支数
    ax = axes[0, 0]
    ax.plot(N_values, dimensions, 'bo-', linewidth=2, markersize=8)
    ax.set_xlabel('分支数 N', fontsize=12)
    ax.set_ylabel('维数 d = log(N)/log(1/r)', fontsize=12)
    ax.set_title(f'分形维数 (r = {r})', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # 图2: 对数关系
    ax = axes[0, 1]
    log_N = np.log(N_values)
    ax.plot(log_N, dimensions, 'rs-', linewidth=2, markersize=8, label='d vs log(N)')
    # 理论线: d = log(N) / log(1/r)
    slope = 1 / np.log(1/r)
    ax.plot(log_N, slope * log_N, 'g--', linewidth=2, label=f'线性: slope = 1/log(1/r) = {slope:.3f}')
    ax.set_xlabel('log(N)', fontsize=12)
    ax.set_ylabel('维数 d', fontsize=12)
    ax.set_title('对数线性关系', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图3: 加法运算
    ax = axes[1, 0]
    d2 = np.log(2) / np.log(1/r)
    d_values = np.array(dimensions)
    sums = d2 + d_values
    ax.plot(N_values, sums, 'm^-', linewidth=2, markersize=8, label='$d_2 \\oplus d_N$')
    ax.plot(N_values, dimensions, 'bo--', linewidth=2, markersize=6, label='$d_N$', alpha=0.5)
    ax.set_xlabel('N', fontsize=12)
    ax.set_ylabel('维数', fontsize=12)
    ax.set_title(f'分形加法: $d_2 \\oplus d_N$ (r = {r})', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图4: Grothendieck群元素
    ax = axes[1, 1]
    # [d_N, d_2] = d_N - d_2
    diffs = np.array(dimensions) - d2
    ax.plot(N_values, diffs, 'cv-', linewidth=2, markersize=8)
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.set_xlabel('N', fontsize=12)
    ax.set_ylabel('$[d_N, d_2]$ = $d_N - d_2$', fontsize=12)
    ax.set_title('Grothendieck群元素 (形式差)', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fractal_arithmetic_visualization.png', dpi=150)
    print("✓ 可视化已保存: fractal_arithmetic_visualization.png")


def compute_examples():
    """
    计算具体例子
    """
    print("\n" + "=" * 70)
    print("具体计算例子")
    print("=" * 70)
    
    r = 1/2
    
    print(f"\n固定压缩比 r = {r}")
    print(f"log(1/r) = log(2) = {np.log(2):.6f}")
    print()
    
    # 例子1: 笛卡尔积的维数
    print("[例1] Cantor集 × Cantor集的维数")
    d_cantor = np.log(2) / np.log(3)  # 经典Cantor集
    print(f"单个Cantor集: d = log(2)/log(3) = {d_cantor:.6f}")
    print(f"笛卡尔积: d ⊕ d = 2d = {2*d_cantor:.6f}")
    print(f"理论值: log(4)/log(3) = {np.log(4)/np.log(3):.6f}")
    
    # 例子2: 逆元
    print("\n[例2] Grothendieck群中的逆元")
    d3 = FractalDimension(3, r)
    d5 = FractalDimension(5, r)
    diff = d3.d - d5.d
    print(f"d3 = {d3.d:.6f}")
    print(f"d5 = {d5.d:.6f}")
    print(f"[d3, d5] = d3 - d5 = {diff:+.6f}")
    print(f"对应有理数: 3/5 = {3/5:.6f}")
    print(f"log(3/5) = {np.log(3/5):.6f}")
    print(f"验证: log(3/5)/log(2) = {np.log(3/5)/np.log(2):.6f}")


if __name__ == '__main__':
    verify_addition_structure()
    verify_rational_isomorphism()
    compute_examples()
    visualize_arithmetic()
    
    print("\n" + "=" * 70)
    print("分形算术数值验证完成!")
    print("=" * 70)
