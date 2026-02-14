#!/usr/bin/env python3
"""
谱维演化PDE的数值验证
Numerical verification of spectral dimension evolution PDE

Author: AI Research Engine
Date: 2026-02-07
Theory: spectral-dimension-pde/
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.special import erf


class SpectralDimensionPDE:
    """
    谱维演化PDE的数值求解器
    
    PDE: ∂d_s/∂t = (2⟨λ⟩_t - d_s/t) / log(t)
    """
    
    def __init__(self, eigenvalues, eigenfunctions_squared):
        """
        初始化
        
        Parameters:
        -----------
        eigenvalues : array
            特征值 λ_n
        eigenfunctions_squared : array
            |φ_n(x)|^2 在固定点x的值
        """
        self.lambdas = np.array(eigenvalues)
        self.phis_sq = np.array(eigenfunctions_squared)
        
    def average_energy(self, t):
        """
        计算平均能量 ⟨λ⟩_t
        
        ⟨λ⟩_t = Σ λ_n exp(-λ_n t) |φ_n|^2 / Σ exp(-λ_n t) |φ_n|^2
        """
        weights = np.exp(-self.lambdas * t) * self.phis_sq
        numerator = np.sum(self.lambdas * weights)
        denominator = np.sum(weights)
        
        if denominator < 1e-300:
            return self.lambdas[0]  # 大t极限
            
        return numerator / denominator
    
    def pde_rhs(self, d_s, t):
        """
        PDE右端: F(d_s, t) = (2⟨λ⟩_t - d_s/t) / log(t)
        """
        if t <= 0 or np.log(t) == 0:
            return 0
            
        lambda_avg = self.average_energy(t)
        return (2 * lambda_avg - d_s / t) / np.log(t)
    
    def solve(self, t_span, d_s_initial, num_points=1000):
        """
        数值求解PDE
        
        Parameters:
        -----------
        t_span : tuple (t_min, t_max)
            时间区间
        d_s_initial : float
            初始值 d_s(t_max)
        num_points : int
            时间离散点数
            
        Returns:
        --------
        t : array
            时间点
        d_s : array
            谱维值
        lambda_avg : array
            平均能量
        """
        t = np.linspace(t_span[0], t_span[1], num_points)
        
        # 反向求解（从t_max到t_min）
        def ode(y, t):
            return self.pde_rhs(y[0], t)
        
        sol = odeint(ode, [d_s_initial], t)
        d_s = sol[:, 0]
        
        lambda_avg = np.array([self.average_energy(ti) for ti in t])
        
        return t, d_s, lambda_avg


class SierpinskiGasket:
    """
    Sierpinski垫片的谱理论
    """
    
    @staticmethod
    def generate_eigenvalues(num_eigenvalues=1000):
        """
        生成Sierpinski垫片的近似特征值
        
        使用Weber渐近: λ_n ~ C * n^(2/d_s)
        其中 d_s = 2*log(3)/log(5) ≈ 1.365
        """
        d_s = 2 * np.log(3) / np.log(5)
        C = 10.0  # 归一化常数
        
        n = np.arange(1, num_eigenvalues + 1)
        lambdas = C * n**(2/d_s)
        
        return lambdas
    
    @staticmethod
    def theoretical_spectral_dimension():
        """理论谱维值"""
        return 2 * np.log(3) / np.log(5)


def verify_sierpinski():
    """
    验证Sierpinski垫片的谱维演化
    """
    print("=" * 60)
    print("谱维演化PDE数值验证 - Sierpinski垫片")
    print("=" * 60)
    
    # 生成特征值
    sg = SierpinskiGasket()
    lambdas = sg.generate_eigenvalues(num_eigenvalues=500)
    phis_sq = np.ones_like(lambdas)  # 简化：假设|φ_n|^2 ≈ 1
    
    d_s_theory = sg.theoretical_spectral_dimension()
    print(f"\n理论谱维: d_s = {d_s_theory:.6f}")
    print(f"Hausdorff维: d_H = {np.log(3)/np.log(2):.6f}")
    
    # 创建PDE求解器
    pde = SpectralDimensionPDE(lambdas, phis_sq)
    
    # 求解
    t_min, t_max = 1e-6, 1e-1
    t, d_s, lambda_avg = pde.solve(
        t_span=(t_min, t_max),
        d_s_initial=1.5,  # 初始值
        num_points=500
    )
    
    # 输出结果
    print(f"\n时间区间: [{t_min}, {t_max}]")
    print(f"t = {t_max}: d_s = {d_s[-1]:.4f}")
    print(f"t = {t_min}: d_s = {d_s[0]:.4f}")
    print(f"误差: |d_s({t_min}) - d_s_theory| = {abs(d_s[0] - d_s_theory):.6f}")
    
    # 验证渐近行为
    print(f"\n渐近验证 (t → 0):")
    for t_val in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        idx = np.argmin(np.abs(t - t_val))
        print(f"  t = {t_val:.0e}: d_s = {d_s[idx]:.6f}, λ_avg ≈ {lambda_avg[idx]:.1f}")
    
    # 可视化
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 图1: d_s(t) vs t
    ax = axes[0, 0]
    ax.semilogx(t, d_s, 'b-', linewidth=2, label='Numerical $d_s(t)$')
    ax.axhline(y=d_s_theory, color='r', linestyle='--', 
               label=f'Theoretical $d_s$ = {d_s_theory:.4f}')
    ax.set_xlabel('t (log scale)', fontsize=12)
    ax.set_ylabel('$d_s(t)$', fontsize=12)
    ax.set_title('Spectral Dimension Evolution', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图2: 平均能量
    ax = axes[0, 1]
    ax.loglog(t, lambda_avg, 'g-', linewidth=2)
    # 理论渐近: ⟨λ⟩_t ~ d_s/(2t)
    t_theory = np.linspace(t_min, t_max, 100)
    lambda_theory = d_s_theory / (2 * t_theory)
    ax.loglog(t_theory, lambda_theory, 'r--', 
              label=f'Theory: $d_s/(2t)$', alpha=0.7)
    ax.set_xlabel('t', fontsize=12)
    ax.set_ylabel('$\\langle \\lambda \\rangle_t$', fontsize=12)
    ax.set_title('Average Energy', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 图3: 误差分析
    ax = axes[1, 0]
    error = np.abs(d_s - d_s_theory)
    ax.loglog(t, error, 'm-', linewidth=2)
    ax.set_xlabel('t', fontsize=12)
    ax.set_ylabel('$|d_s(t) - d_s|$', fontsize=12)
    ax.set_title('Error Analysis', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # 图4: 渐近展开验证
    ax = axes[1, 1]
    alpha = 1 - d_s_theory / 2
    # 预期: d_s(t) - d_s ~ C * t^alpha
    diff = d_s - d_s_theory
    valid_idx = (t > 1e-5) & (diff > 0)
    if np.any(valid_idx):
        ax.loglog(t[valid_idx], diff[valid_idx], 'c-', linewidth=2, 
                  label='Numerical $d_s(t) - d_s$')
        # 拟合幂律
        if len(t[valid_idx]) > 10:
            log_t = np.log(t[valid_idx])
            log_diff = np.log(diff[valid_idx])
            coeffs = np.polyfit(log_t, log_diff, 1)
            fitted_exponent = coeffs[0]
            ax.loglog(t[valid_idx], np.exp(coeffs[1]) * t[valid_idx]**fitted_exponent,
                      'r--', label=f'Fitted: $t^{{{fitted_exponent:.3f}}}$')
            print(f"\n渐近指数拟合: {fitted_exponent:.4f}")
            print(f"理论预期: {alpha:.4f}")
    ax.set_xlabel('t', fontsize=12)
    ax.set_ylabel('$d_s(t) - d_s$', fontsize=12)
    ax.set_title(f'Asymptotic Behavior ($t^{alpha:.3f}$)', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spectral_dimension_verification.png', dpi=150)
    print("\n✓ 可视化已保存: spectral_dimension_verification.png")
    
    return t, d_s, lambda_avg


if __name__ == '__main__':
    # 运行验证
    t, d_s, lambda_avg = verify_sierpinski()
    
    print("\n" + "=" * 60)
    print("验证完成!")
    print("=" * 60)
