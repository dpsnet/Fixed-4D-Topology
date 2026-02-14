#!/usr/bin/env python3
"""
分析WSe2单层Rydberg激子数据
用于验证c1(d=2, w=0) = 1.0

数据源:
- WSe2: E1s = -172 meV, E2s = -41 meV, E3s = -20 meV, E4s = -11 meV
- 参考: arXiv:2407.01477v3 (2024) 引用 Liu et al. (2019) 和 Chernikov et al. (2014)

注意: WSe2是纯2D系统(单层)，但激子具有非氢原子性(nonhydrogenic)
这是由于介电屏蔽的非均匀性导致的
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

print("=" * 80)
print("WSe2单层Rydberg激子分析 - 验证c1(d=2, w=0) = 1.0")
print("=" * 80)

# ============================================================================
# 实验数据
# ============================================================================

# WSe2 Rydberg激子结合能 (meV)
# 来源: Liu et al. (2019), 引用自 arXiv:2407.01477v3
n_wse2 = np.array([1, 2, 3, 4])
E_binding_wse2 = np.array([172, 41, 20, 11])  # meV, 结合能取正值

# 估计不确定性 (基于典型实验误差)
sigma_wse2 = np.array([5, 2, 1, 1])  # meV

print("\nWSe2实验数据 (Liu et al. 2019):")
print("-" * 40)
for n, E, sig in zip(n_wse2, E_binding_wse2, sigma_wse2):
    print(f"  n = {n}: E = {E} ± {sig} meV")

# ============================================================================
# 理论背景
# ============================================================================

print("\n" + "=" * 80)
print("理论背景")
print("=" * 80)

print("""
WSe2是单层过渡金属硫化物(TMD)，具有纯2D结构。

理想2D氢原子: E_n = R_y^* / (n - 1/2)^2
- n=1: 4 × R_y^*
- n=2: 4/9 × R_y^* ≈ 0.44 × R_y^*
- n=3: 4/25 × R_y^* = 0.16 × R_y^*

但TMD激子是非氢原子性的，由于:
1. 介电环境的非均匀性 (2D材料在3D空间中)
2. 势能的Rytova-Keldysh形式: V(r) ∝ 1/r - 1/(r + r_0)
3. 激子波函数穿透到hBN衬底

维度流模型:
E_n = R_y^* / (n - δ(n))^2
其中 δ(n) = δ_∞ / (1 + (n_0/n)^(1/c1))

对于纯2D系统，预期c1 = 1.0
""")

# 理想2D Rydberg常数估计
# 从n=1数据: R_y^* = 172/4 = 43 meV (如果纯2D)
R_2D_estimate = E_binding_wse2[0] / 4
print(f"\n估计的理想2D Rydberg常数: {R_2D_estimate:.1f} meV")

# ============================================================================
# 拟合模型
# ============================================================================

def dimension_flow_model(n, Ry, n0, c1, delta_inf):
    """
    维度流修正的Rydberg公式
    
    E_n = Ry / (n - delta(n))^2
    delta(n) = delta_inf / (1 + (n0/n)^(1/c1))
    
    参数:
    - Ry: 有效Rydberg常数 (meV)
    - n0: 特征量子数
    - c1: 维度流参数 (目标值 = 1.0)
    - delta_inf: 大n极限下的量子亏损
    """
    delta_n = delta_inf / (1 + (n0 / n)**(1 / c1))
    return Ry / (n - delta_n)**2


def standard_2d_rydberg(n, Ry):
    """标准2D Rydberg: E_n = Ry / (n - 0.5)^2"""
    return Ry / (n - 0.5)**2


def hydrogenic_3d(n, Ry):
    """标准3D氢原子: E_n = Ry / n^2"""
    return Ry / n**2


# 拟合
print("\n" + "=" * 80)
print("模型拟合")
print("=" * 80)

# 1. 标准2D模型 (固定c1=1, delta_inf=0.5)
def model_2d_fixed(n, Ry, n0):
    return dimension_flow_model(n, Ry, n0, 1.0, 0.5)

popt_2d, _ = curve_fit(model_2d_fixed, n_wse2, E_binding_wse2, 
                        p0=[150, 1.0], sigma=sigma_wse2, absolute_sigma=True)
Ry_2d, n0_2d = popt_2d
chi2_2d = np.sum(((E_binding_wse2 - model_2d_fixed(n_wse2, *popt_2d)) / sigma_wse2)**2)

print(f"\n1. 固定c1=1.0 (理论2D):")
print(f"   Ry = {Ry_2d:.1f} meV")
print(f"   n0 = {n0_2d:.2f}")
print(f"   χ² = {chi2_2d:.2f}")

# 2. 自由拟合c1
popt_free, pcov_free = curve_fit(dimension_flow_model, n_wse2, E_binding_wse2,
                                  p0=[150, 1.0, 1.0, 0.5],
                                  sigma=sigma_wse2,
                                  bounds=([50, 0.1, 0.1, 0.0], [300, 5.0, 3.0, 1.0]),
                                  absolute_sigma=True)
Ry_free, n0_free, c1_free, delta_free = popt_free
Ry_err, n0_err, c1_err, delta_err = np.sqrt(np.diag(pcov_free))
chi2_free = np.sum(((E_binding_wse2 - dimension_flow_model(n_wse2, *popt_free)) / sigma_wse2)**2)

print(f"\n2. 自由拟合 (c1为自由参数):")
print(f"   Ry = {Ry_free:.1f} meV")
print(f"   n0 = {n0_free:.2f}")
print(f"   c1 = {c1_free:.3f} ± {c1_err:.3f}")
print(f"   δ∞ = {delta_free:.3f}")
print(f"   χ² = {chi2_free:.2f}")

# 与理论值比较
c1_theory = 1.0
deviation = (c1_free - c1_theory) / c1_err
print(f"\n与理论c1(2,0) = 1.0比较:")
print(f"   偏差: {deviation:.2f}σ")

# ============================================================================
# 可视化
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图: 结合能vs量子数
ax1 = axes[0]

n_fit = np.linspace(0.8, 5, 100)

# 实验数据
ax1.errorbar(n_wse2, E_binding_wse2, yerr=sigma_wse2,
            fmt='o', markersize=10, capsize=5, capthick=2,
            label='WSe2实验数据 (Liu 2019)', color='blue', zorder=5)

# 拟合曲线
ax1.plot(n_fit, dimension_flow_model(n_fit, *popt_free), 'r-',
        linewidth=2, label=f'维度流拟合 (c₁={c1_free:.2f})', zorder=3)
ax1.plot(n_fit, model_2d_fixed(n_fit, *popt_2d), 'g--',
        linewidth=2, label='固定c₁=1.0', alpha=0.7, zorder=2)

# 理想曲线
ax1.plot(n_fit, standard_2d_rydberg(n_fit, 172), 'k:',
        linewidth=1, label='理想2D (Ry=172)', alpha=0.5)

ax1.set_xlabel('主量子数 n', fontsize=12)
ax1.set_ylabel('结合能 (meV)', fontsize=12)
ax1.set_title('WSe2 Rydberg激子结合能', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right', fontsize=9)
ax1.set_xlim(0.5, 5)
ax1.set_ylim(0, 200)
ax1.grid(True, alpha=0.3)

# 添加拟合参数文本
textstr = f'自由拟合参数:\n'
textstr += f'Ry = {Ry_free:.1f} meV\n'
textstr += f'c₁ = {c1_free:.3f} ± {c1_err:.3f}\n'
textstr += f'δ∞ = {delta_free:.3f}\n'
textstr += f'χ² = {chi2_free:.2f}'
ax1.text(0.55, 0.6, textstr, transform=ax1.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 右图: 残差分析
ax2 = axes[1]

residual_free = (E_binding_wse2 - dimension_flow_model(n_wse2, *popt_free)) / sigma_wse2
residual_2d = (E_binding_wse2 - model_2d_fixed(n_wse2, *popt_2d)) / sigma_wse2

x_pos = np.arange(len(n_wse2))
width = 0.35

bars1 = ax2.bar(x_pos - width/2, residual_free, width, 
               label=f'自由拟合 (c₁={c1_free:.2f})', color='red', alpha=0.7)
bars2 = ax2.bar(x_pos + width/2, residual_2d, width,
               label='固定c₁=1.0', color='green', alpha=0.7)

ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(y=-1, color='gray', linestyle='--', alpha=0.5)
ax2.set_xlabel('主量子数 n', fontsize=12)
ax2.set_ylabel('归一化残差 (σ)', fontsize=12)
ax2.set_title('拟合残差比较', fontsize=13, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([str(n) for n in n_wse2])
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(-2, 2)

plt.tight_layout()
plt.savefig('wse2_rydberg_analysis.png', dpi=150, bbox_inches='tight')
print(f"\n图表已保存至: wse2_rydberg_analysis.png")

# ============================================================================
# 总结
# ============================================================================

print("\n" + "=" * 80)
print("总结")
print("=" * 80)

print(f"""
系统: WSe2单层 (纯2D系统, d=2, w=0)
数据源: Liu et al. (2019), 引用自 arXiv:2407.01477v3

提取的c₁值: {c1_free:.3f} ± {c1_err:.3f}
理论预期值: 1.0
偏差: {deviation:.2f}σ

状态: {"✓ 确认" if abs(deviation) < 2 else "⚠ 边缘" if abs(deviation) < 3 else "✗ 不一致"}

注意:
- WSe2激子是非氢原子性的(介电屏蔽效应)
- 只有4个数据点，统计受限
- 需要更多n值的数据以提高精度
""")

# 保存结果
results = {
    'system': 'WSe2 monolayer',
    'dimension': 2,
    'time_weight': 0,
    'c1_extracted': float(c1_free),
    'c1_uncertainty': float(c1_err),
    'c1_theory': 1.0,
    'deviation_sigma': float(deviation),
    'n_points': len(n_wse2),
    'binding_energies': E_binding_wse2.tolist(),
    'quantum_numbers': n_wse2.tolist(),
    'source': 'Liu et al. (2019) via arXiv:2407.01477v3'
}

import json
with open('wse2_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("结果已保存至: wse2_analysis_results.json")
