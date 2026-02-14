#!/usr/bin/env python3
"""
WKB近似下的维度流拟合分析
基于严格推导的公式拟合能级数据
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def effective_dimension(n, n0, c1):
    """
    有效维度流公式
    d_eff(n) = 2 + 1 / (1 + (n/n0)^(1/c1))
    """
    return 2.0 + 1.0 / (1.0 + (n / n0)**(1.0/c1))


def quantum_defect(n, n0, c1):
    """
    量子亏损 δ(n) = 0.5 * (3 - d_eff)
    """
    d_eff = effective_dimension(n, n0, c1)
    return 0.5 * (3.0 - d_eff)


def energy_wkb(n, Ry, n0, c1):
    """
    WKB能级公式: E_n = -Ry / (n - δ(n))²
    """
    delta = quantum_defect(n, n0, c1)
    return -Ry / (n - delta)**2


def level_spacing_wkb(n, Ry, n0, c1):
    """
    能级间距 ΔE_n = E_{n+1} - E_n
    """
    E_n = energy_wkb(n, Ry, n0, c1)
    E_n1 = energy_wkb(n + 1, Ry, n0, c1)
    return E_n1 - E_n  # 注意：E_n为负值，但ΔE_n为正


def generate_synthetic_data(Ry_true=4.2, n0_true=8.0, c1_true=0.5, 
                           noise_level=0.01, n_max=25):
    """
    生成模拟实验数据
    参数基于Cu2O的实际值
    """
    n_values = np.arange(3, n_max + 1)
    
    # 真实能级
    E_true = np.array([energy_wkb(n, Ry_true, n0_true, c1_true) for n in n_values])
    
    # 添加高斯噪声（模拟实验误差）
    E_noisy = E_true * (1 + noise_level * np.random.randn(len(n_values)))
    
    # 能级间距
    delta_E_true = np.array([level_spacing_wkb(n, Ry_true, n0_true, c1_true) 
                             for n in n_values[:-1]])
    delta_E_noisy = np.diff(E_noisy)
    
    return {
        'n': n_values,
        'E_true': E_true,
        'E_noisy': E_noisy,
        'delta_E_true': delta_E_true,
        'delta_E_noisy': delta_E_noisy,
        'params': {'Ry': Ry_true, 'n0': n0_true, 'c1': c1_true, 'noise': noise_level}
    }


def fit_energy_levels(n_data, E_data, sigma=None):
    """
    用WKB公式拟合能级数据
    """
    # 初始猜测
    Ry_guess = -E_data[0] * 9  # E_3 ≈ -Ry/9
    n0_guess = 5.0
    c1_guess = 0.5
    
    try:
        popt, pcov = curve_fit(energy_wkb, n_data, E_data, 
                               p0=[Ry_guess, n0_guess, c1_guess],
                               sigma=sigma,
                               bounds=([0.5, 0.5, 0.1], [20.0, 50.0, 2.0]))
        
        Ry_fit, n0_fit, c1_fit = popt
        Ry_err, n0_err, c1_err = np.sqrt(np.diag(pcov))
        
        # 计算χ²
        E_fit = np.array([energy_wkb(n, *popt) for n in n_data])
        if sigma is None:
            sigma = np.abs(E_data) * 0.01
        chi2 = np.sum(((E_data - E_fit) / sigma)**2)
        dof = len(n_data) - 3
        chi2_red = chi2 / dof
        
        return {
            'Ry': (Ry_fit, Ry_err),
            'n0': (n0_fit, n0_err),
            'c1': (c1_fit, c1_err),
            'chi2': chi2,
            'chi2_red': chi2_red,
            'dof': dof,
            'success': True
        }
    except Exception as e:
        print(f"拟合失败: {e}")
        return {'success': False}


def compare_c1_values(n_data, E_data, Ry_fixed, n0_fixed):
    """
    比较不同c1值的拟合质量
    """
    c1_test_values = [0.25, 0.35, 0.5, 0.7, 1.0, 1.5]
    results = []
    
    for c1_test in c1_test_values:
        E_pred = np.array([energy_wkb(n, Ry_fixed, n0_fixed, c1_test) for n in n_data])
        residuals = E_data - E_pred
        chi2 = np.sum(residuals**2 / (0.01 * np.abs(E_data))**2)
        results.append((c1_test, chi2))
    
    return results


def analyze_quantum_defect(data, fit_result):
    """
    分析量子亏损的能量依赖性
    """
    n = data['n']
    E_noisy = data['E_noisy']
    Ry_fit = fit_result['Ry'][0]
    n0_fit = fit_result['n0'][0]
    c1_fit = fit_result['c1'][0]
    
    # 从"实验"能级反推量子亏损
    delta_exp = n - np.sqrt(-Ry_fit / E_noisy)
    
    # 理论量子亏损
    delta_theory = np.array([quantum_defect(ni, n0_fit, c1_fit) for ni in n])
    
    return {
        'n': n,
        'delta_exp': delta_exp,
        'delta_theory': delta_theory
    }


def plot_analysis(data, fit_result, qd_analysis):
    """
    绘制完整分析图
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    n = data['n']
    E_true = data['E_true']
    E_noisy = data['E_noisy']
    params = data['params']
    
    Ry_fit, Ry_err = fit_result['Ry']
    n0_fit, n0_err = fit_result['n0']
    c1_fit, c1_err = fit_result['c1']
    
    # 图1: 能级图
    ax1 = axes[0, 0]
    ax1.plot(n, E_true, 'b-', linewidth=2, label='True (Theory)')
    ax1.scatter(n, E_noisy, c='red', s=50, zorder=5, label='Synthetic Data')
    
    # 拟合曲线
    n_fine = np.linspace(n.min(), n.max(), 200)
    E_fit_curve = np.array([energy_wkb(ni, Ry_fit, n0_fit, c1_fit) for ni in n_fine])
    ax1.plot(n_fine, E_fit_curve, 'g--', linewidth=2, label=f'Fit (c₁={c1_fit:.3f})')
    
    ax1.set_xlabel('Principal Quantum Number n', fontsize=12)
    ax1.set_ylabel('Energy (meV)', fontsize=12)
    ax1.set_title('Energy Levels: WKB Model Fit', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 图2: 量子亏损
    ax2 = axes[0, 1]
    ax2.scatter(qd_analysis['n'], qd_analysis['delta_exp'], 
               c='red', s=50, label='Extracted from Data')
    ax2.plot(qd_analysis['n'], qd_analysis['delta_theory'], 
            'b-', linewidth=2, label='Theory (c₁={})'.format(c1_fit))
    ax2.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='3D limit (δ=0)')
    ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='2D limit (δ=0.5)')
    ax2.set_xlabel('Principal Quantum Number n', fontsize=12)
    ax2.set_ylabel('Quantum Defect δ(n)', fontsize=12)
    ax2.set_title('Quantum Defect vs n', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.1, 0.6)
    
    # 图3: 残差
    ax3 = axes[1, 0]
    E_fit = np.array([energy_wkb(ni, Ry_fit, n0_fit, c1_fit) for ni in n])
    residuals = E_noisy - E_fit
    ax3.bar(n, residuals, color='purple', alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.set_xlabel('Principal Quantum Number n', fontsize=12)
    ax3.set_ylabel('Residual (meV)', fontsize=12)
    ax3.set_title(f'Fit Residuals (χ²/DOF = {fit_result["chi2_red"]:.2f})', fontsize=14)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 图4: 不同c1值的比较
    ax4 = axes[1, 1]
    c1_comparison = compare_c1_values(n, E_noisy, Ry_fit, n0_fit)
    c1_vals = [r[0] for r in c1_comparison]
    chi2_vals = [r[1] for r in c1_comparison]
    
    colors = ['red' if c != 0.5 else 'green' for c in c1_vals]
    ax4.bar(range(len(c1_vals)), chi2_vals, color=colors, alpha=0.7)
    ax4.set_xticks(range(len(c1_vals)))
    ax4.set_xticklabels([f'{c:.2f}' for c in c1_vals], rotation=45)
    ax4.set_xlabel('c₁ Value', fontsize=12)
    ax4.set_ylabel('χ²', fontsize=12)
    ax4.set_title('χ² Comparison for Different c₁', fontsize=14)
    ax4.axvline(x=1, color='green', linestyle='--', linewidth=2, label='True c₁=0.5')
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('wkb_fitting_analysis.png', dpi=150, bbox_inches='tight')
    print("✓ 图片已保存: wkb_fitting_analysis.png")
    plt.close()


def print_summary(data, fit_result):
    """
    打印分析摘要
    """
    params = data['params']
    
    print("\n" + "="*70)
    print("WKB维度流拟合分析结果")
    print("="*70)
    
    print("\n【真实参数】")
    print(f"  Rydberg能量: Ry = {params['Ry']:.3f} meV")
    print(f"  过渡量子数: n₀ = {params['n0']:.2f}")
    print(f"  c₁参数: c₁ = {params['c1']:.4f}")
    print(f"  噪声水平: {params['noise']*100:.1f}%")
    
    print("\n【拟合结果】")
    Ry_fit, Ry_err = fit_result['Ry']
    n0_fit, n0_err = fit_result['n0']
    c1_fit, c1_err = fit_result['c1']
    
    print(f"  Rydberg能量: Ry = {Ry_fit:.3f} ± {Ry_err:.3f} meV")
    print(f"  过渡量子数: n₀ = {n0_fit:.2f} ± {n0_err:.2f}")
    print(f"  c₁参数: c₁ = {c1_fit:.4f} ± {c1_err:.4f}")
    
    print("\n【精度评估】")
    print(f"  c₁相对偏差: {(c1_fit - params['c1'])/params['c1']*100:+.2f}%")
    print(f"  χ² = {fit_result['chi2']:.2f}")
    print(f"  χ²/DOF = {fit_result['chi2_red']:.2f}")
    print(f"  自由度 = {fit_result['dof']}")
    
    print("\n【c₁值比较】")
    c1_comparison = compare_c1_values(data['n'], data['E_noisy'], Ry_fit, n0_fit)
    print(f"  {'c₁':<8} {'χ²':<10} 评估")
    print("  " + "-"*35)
    for c1_val, chi2_val in c1_comparison:
        marker = "✅" if c1_val == params['c1'] else ""
        quality = "优" if chi2_val < 20 else "中" if chi2_val < 50 else "差"
        print(f"  {c1_val:<8.2f} {chi2_val:<10.2f} {quality} {marker}")
    
    print("\n【结论】")
    if abs(c1_fit - params['c1']) / params['c1'] < 0.1:
        print("  ✅ c₁参数被成功提取，偏差 < 10%")
    else:
        print("  ⚠️ c₁参数提取存在较大偏差")
    
    if fit_result['chi2_red'] < 2:
        print("  ✅ 拟合质量良好 (χ²/DOF < 2)")
    else:
        print("  ⚠️ 拟合质量一般")
    
    print("="*70)


def main():
    """主程序"""
    print("="*70)
    print("WKB维度流拟合分析")
    print("基于严格推导的能级公式")
    print("="*70)
    
    np.random.seed(42)
    
    # 生成模拟数据 (Cu2O参数)
    print("\n[1] 生成模拟数据 (基于Cu2O参数)...")
    data = generate_synthetic_data(
        Ry_true=4.2,      # Cu2O的Rydberg能量 (meV)
        n0_true=8.0,      # 过渡量子数
        c1_true=0.5,      # 理论预测值
        noise_level=0.005, # 0.5%噪声 (高质量数据)
        n_max=25          # 观测到n=25 (如文献报道)
    )
    print(f"    生成 {len(data['n'])} 个能级 (n=3 到 n={data['n'][-1]})")
    
    # 拟合
    print("\n[2] 用WKB公式拟合能级数据...")
    sigma = np.abs(data['E_noisy']) * data['params']['noise']
    fit_result = fit_energy_levels(data['n'], data['E_noisy'], sigma)
    
    if not fit_result['success']:
        print("拟合失败，退出")
        return
    
    # 分析量子亏损
    print("\n[3] 分析量子亏损的能量依赖性...")
    qd_analysis = analyze_quantum_defect(data, fit_result)
    
    # 绘制结果
    print("\n[4] 生成可视化...")
    plot_analysis(data, fit_result, qd_analysis)
    
    # 打印摘要
    print_summary(data, fit_result)


if __name__ == "__main__":
    main()
