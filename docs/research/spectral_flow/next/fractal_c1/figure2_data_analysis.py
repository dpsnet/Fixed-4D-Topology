#!/usr/bin/env python3
"""
制作论文Figure 2：Cu2O数据分析图
包含：能级拟合、量子亏损、c1提取
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['legend.fontsize'] = 9

# 加载数据
df = pd.read_csv('cu2o_kazimierczuk_2014_data.csv')
n = df['n'].values
E_binding = df['Binding_Energy_meV'].values
E_total = 2172.08 - E_binding  # meV

# 定义拟合函数
def model_standard(n, Ry, Eg):
    """标准Rydberg"""
    return Eg - Ry / n**2

def model_constant_qd(n, Ry, Eg, delta):
    """常数量子亏损"""
    return Eg - Ry / (n - delta)**2

def model_dim_flow(n, Ry, Eg, n0, c1):
    """维度流模型"""
    delta_n = 0.5 / (1.0 + (n0 / n)**(1.0/c1))
    return Eg - Ry / (n - delta_n)**2

# 执行拟合
weights = np.ones_like(n)
weights[n > 15] = 0.5  # 高n数据权重降低

# 拟合1：标准Rydberg
popt1, _ = curve_fit(model_standard, n, E_total, p0=[92, 2172], sigma=1/weights)
E_fit1 = model_standard(n, *popt1)

# 拟合2：常数量子亏损
popt2, _ = curve_fit(model_constant_qd, n, E_total, p0=[92, 2172, 0.2], 
                     bounds=([70, 2170, -0.5], [110, 2175, 1]), sigma=1/weights)
E_fit2 = model_constant_qd(n, *popt2)

# 拟合3：维度流
popt3, _ = curve_fit(model_dim_flow, n, E_total, p0=[82, 2172, 5, 0.5],
                     bounds=([70, 2170, 1, 0.1], [110, 2175, 50, 2]), sigma=1/weights)
E_fit3 = model_dim_flow(n, *popt3)

Ry_fit, Eg_fit, n0_fit, c1_fit = popt3

print(f"拟合结果:")
print(f"  Ry = {Ry_fit:.2f} meV")
print(f"  Eg = {Eg_fit:.4f} meV")
print(f"  n0 = {n0_fit:.2f}")
print(f"  c1 = {c1_fit:.4f}")

# 创建图形
fig = plt.figure(figsize=(14, 10))

# ===== 子图a：能级拟合 =====
ax1 = plt.subplot(2, 2, 1)
ax1.scatter(n, E_binding, c='red', s=50, zorder=5, label='Experimental data')

n_fine = np.linspace(3, 25, 200)
E_bind_fit1 = popt1[0] / n_fine**2
E_bind_fit2 = popt2[0] / (n_fine - popt2[2])**2
delta_fine = 0.5 / (1.0 + (n0_fit / n_fine)**(1.0/c1_fit))
E_bind_fit3 = Ry_fit / (n_fine - delta_fine)**2

ax1.loglog(n_fine, E_bind_fit1, 'b--', alpha=0.6, label=f'Standard (δ=0)')
ax1.loglog(n_fine, E_bind_fit2, 'g:', alpha=0.6, label=f'Constant δ={popt2[2]:.3f}')
ax1.loglog(n_fine, E_bind_fit3, 'm-', linewidth=2, label=f'Dimension flow ($c_1$={c1_fit:.3f})')

ax1.set_xlabel('Principal quantum number $n$', fontsize=12)
ax1.set_ylabel('Binding energy (meV)', fontsize=12)
ax1.set_title('(a) Rydberg Exciton Energy Levels', fontsize=13, fontweight='bold')
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(2.5, 30)
ax1.set_ylim(0.1, 15)

# ===== 子图b：量子亏损 =====
ax2 = plt.subplot(2, 2, 2)

# 从数据反推量子亏损
delta_extracted = n - np.sqrt(92 / E_binding)
ax2.scatter(n, delta_extracted, c='red', s=50, zorder=5, label='Extracted from data')

delta_theory = 0.5 / (1.0 + (n0_fit / n_fine)**(1.0/c1_fit))
ax2.plot(n_fine, delta_theory, 'm-', linewidth=2, label=f'Dimension flow ($c_1$={c1_fit:.3f})')
ax2.axhline(y=popt2[2], color='green', linestyle=':', alpha=0.7, label=f'Constant δ={popt2[2]:.3f}')
ax2.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='3D limit (δ=0)')
ax2.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='2D limit (δ=0.5)')

ax2.set_xlabel('Principal quantum number $n$', fontsize=12)
ax2.set_ylabel('Quantum defect $\\delta(n)$', fontsize=12)
ax2.set_title('(b) Quantum Defect vs $n$', fontsize=13, fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(-0.1, 0.6)

# ===== 子图c：残差 =====
ax3 = plt.subplot(2, 2, 3)

res1 = (E_total - E_fit1) / E_total * 100
res2 = (E_total - E_fit2) / E_total * 100
res3 = (E_total - E_fit3) / E_total * 100

x_offset = np.array([-0.3, 0, 0.3])
width = 0.25

ax3.bar(n + x_offset[0], res1, width=width, color='blue', alpha=0.6, label='Standard')
ax3.bar(n + x_offset[1], res2, width=width, color='green', alpha=0.6, label='Constant δ')
ax3.bar(n + x_offset[2], res3, width=width, color='magenta', alpha=0.6, label='Dimension flow')

ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.set_xlabel('Principal quantum number $n$', fontsize=12)
ax3.set_ylabel('Residual (%)', fontsize=12)
ax3.set_title('(c) Fit Residuals', fontsize=13, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# ===== 子图d：c1提取的置信区间 =====
ax4 = plt.subplot(2, 2, 4)

# 扫描c1值，计算chi2
c1_scan = np.linspace(0.3, 0.8, 100)
chi2_scan = []

for c1_test in c1_scan:
    try:
        popt_scan, _ = curve_fit(lambda n, Ry, Eg, n0: model_dim_flow(n, Ry, Eg, n0, c1_test),
                                 n, E_total, p0=[85, 2172, 5], sigma=1/weights)
        E_fit_scan = model_dim_flow(n, *popt_scan, c1_test)
        chi2 = np.sum(((E_total - E_fit_scan) / (E_total * 0.01))**2)
        chi2_scan.append(chi2)
    except:
        chi2_scan.append(np.nan)

chi2_scan = np.array(chi2_scan)
chi2_min = np.nanmin(chi2_scan)
delta_chi2 = chi2_scan - chi2_min

ax4.plot(c1_scan, delta_chi2, 'b-', linewidth=2)
ax4.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='$\\Delta\\chi^2 = 1$ (1$\\sigma$)')
ax4.axvline(x=c1_fit, color='green', linestyle='-', alpha=0.7, label=f'Best fit: $c_1$={c1_fit:.3f}')

# 标记1sigma区间
mask_1sigma = delta_chi2 <= 1
if np.any(mask_1sigma):
    c1_lower = np.min(c1_scan[mask_1sigma])
    c1_upper = np.max(c1_scan[mask_1sigma])
    ax4.axvspan(c1_lower, c1_upper, alpha=0.2, color='green', label=f'1$\\sigma$ interval: [{c1_lower:.3f}, {c1_upper:.3f}]')

ax4.set_xlabel('$c_1$ parameter', fontsize=12)
ax4.set_ylabel('$\\Delta\\chi^2$', fontsize=12)
ax4.set_title('(d) $c_1$ Extraction from Profile Likelihood', fontsize=13, fontweight='bold')
ax4.legend(loc='upper right')
ax4.grid(True, alpha=0.3)
ax4.set_ylim(0, 5)

plt.tight_layout()
plt.savefig('figure2_data_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Figure 2 已保存: figure2_data_analysis.png")
plt.close()

print(f"\n1σ 置信区间: c1 = {c1_fit:.3f} [{c1_lower:.3f}, {c1_upper:.3f}]")
