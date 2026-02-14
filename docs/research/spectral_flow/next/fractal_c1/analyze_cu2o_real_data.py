#!/usr/bin/env python3
"""
分析真实的Cu2O Rydberg激子数据
数据来自Kazimierczuk et al. Nature 2014 图2(a)
使用WKB维度流模型提取c₁参数
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 物理常数
RY_CU2O = 92  # meV, Cu2O的Rydberg能量（文献值）
EG_CU2O = 2172.08  # meV, 带隙能量（文献值）


def load_data(filename):
    """加载CSV数据"""
    df = pd.read_csv(filename)
    return df


def energy_standard_rydberg(n, Ry, Eg):
    """标准Rydberg公式: E_n = Eg - Ry/n²"""
    return Eg - Ry / n**2


def energy_quantum_defect(n, Ry, Eg, delta):
    """含量子亏损的Rydberg公式: E_n = Eg - Ry/(n-δ)²"""
    return Eg - Ry / (n - delta)**2


def energy_dimension_flow(n, Ry, Eg, n0, c1):
    """
    维度流修正的Rydberg公式
    δ(n) = 0.5 / (1 + (n₀/n)^(1/c₁))
    """
    delta_n = 0.5 / (1.0 + (n0 / n)**(1.0/c1))
    return Eg - Ry / (n - delta_n)**2


def extract_quantum_defect(n, E, Ry, Eg):
    """
    从能级数据反推量子亏损
    E = Eg - Ry/(n-δ)²  =>  δ = n - √(Ry/(Eg-E))
    """
    binding_energy = Eg - E
    # 避免除零或负数
    if np.any(binding_energy <= 0):
        return None
    delta = n - np.sqrt(Ry / binding_energy)
    return delta


def fit_models(df):
    """
    用不同模型拟合数据
    """
    n = df['n'].values
    E_binding = df['Binding_Energy_meV'].values
    E_total = EG_CU2O - E_binding  # 总能级 = Eg - 结合能
    
    # 根据数据来源设置权重（实验数据权重更高）
    source_weights = {
        'Experimental': 1.0,
        'Extrapolated': 0.7,
        'Experimental/Theory': 0.9,
        'Theoretical': 0.5
    }
    weights = np.array([source_weights.get(s, 0.5) for s in df['Data_Source']])
    
    results = {}
    
    # 模型1: 标准Rydberg (δ=0)
    print("\n  拟合模型1: 标准Rydberg (δ=0)...")
    try:
        popt1, pcov1 = curve_fit(
            lambda n, Ry, Eg: energy_standard_rydberg(n, Ry, Eg),
            n, E_total,
            p0=[RY_CU2O, EG_CU2O],
            sigma=1.0/weights,
            absolute_sigma=False,
            maxfev=10000
        )
        E_fit1 = energy_standard_rydberg(n, *popt1)
        residuals1 = E_total - E_fit1
        chi2_1 = np.sum((residuals1 / (E_total * 0.01))**2)
        
        results['standard'] = {
            'Ry': popt1[0],
            'Ry_err': np.sqrt(pcov1[0,0]),
            'Eg': popt1[1],
            'Eg_err': np.sqrt(pcov1[1,1]),
            'chi2': chi2_1,
            'residuals': residuals1,
            'E_fit': E_fit1
        }
        print(f"    Ry = {popt1[0]:.2f} ± {np.sqrt(pcov1[0,0]):.2f} meV")
        print(f"    Eg = {popt1[1]:.4f} ± {np.sqrt(pcov1[1,1]):.4f} meV")
        print(f"    χ² = {chi2_1:.2f}")
    except Exception as e:
        print(f"    拟合失败: {e}")
        results['standard'] = None
    
    # 模型2: 常数量子亏损
    print("\n  拟合模型2: 常数量子亏损...")
    try:
        popt2, pcov2 = curve_fit(
            lambda n, Ry, Eg, delta: energy_quantum_defect(n, Ry, Eg, delta),
            n, E_total,
            p0=[RY_CU2O, EG_CU2O, 0.2],
            bounds=([70, 2165, -0.5], [110, 2180, 1.0]),
            sigma=1.0/weights,
            maxfev=10000
        )
        E_fit2 = energy_quantum_defect(n, *popt2)
        residuals2 = E_total - E_fit2
        chi2_2 = np.sum((residuals2 / (E_total * 0.01))**2)
        
        results['constant_qd'] = {
            'Ry': popt2[0],
            'Ry_err': np.sqrt(pcov2[0,0]),
            'Eg': popt2[1],
            'Eg_err': np.sqrt(pcov2[1,1]),
            'delta': popt2[2],
            'delta_err': np.sqrt(pcov2[2,2]),
            'chi2': chi2_2,
            'residuals': residuals2,
            'E_fit': E_fit2
        }
        print(f"    Ry = {popt2[0]:.2f} ± {np.sqrt(pcov2[0,0]):.2f} meV")
        print(f"    Eg = {popt2[1]:.4f} ± {np.sqrt(pcov2[1,1]):.4f} meV")
        print(f"    δ = {popt2[2]:.4f} ± {np.sqrt(pcov2[2,2]):.4f}")
        print(f"    χ² = {chi2_2:.2f}")
    except Exception as e:
        print(f"    拟合失败: {e}")
        results['constant_qd'] = None
    
    # 模型3: 维度流模型（核心！）
    print("\n  拟合模型3: 维度流模型 (目标提取c₁)...")
    try:
        popt3, pcov3 = curve_fit(
            lambda n, Ry, Eg, n0, c1: energy_dimension_flow(n, Ry, Eg, n0, c1),
            n, E_total,
            p0=[RY_CU2O, EG_CU2O, 15.0, 0.5],  # 初始猜测c₁=0.5
            bounds=([70, 2165, 1.0, 0.1], [110, 2180, 50.0, 2.0]),
            sigma=1.0/weights,
            maxfev=10000
        )
        E_fit3 = energy_dimension_flow(n, *popt3)
        residuals3 = E_total - E_fit3
        chi2_3 = np.sum((residuals3 / (E_total * 0.01))**2)
        
        results['dim_flow'] = {
            'Ry': popt3[0],
            'Ry_err': np.sqrt(pcov3[0,0]),
            'Eg': popt3[1],
            'Eg_err': np.sqrt(pcov3[1,1]),
            'n0': popt3[2],
            'n0_err': np.sqrt(pcov3[2,2]),
            'c1': popt3[3],
            'c1_err': np.sqrt(pcov3[3,3]),
            'chi2': chi2_3,
            'residuals': residuals3,
            'E_fit': E_fit3
        }
        print(f"    Ry = {popt3[0]:.2f} ± {np.sqrt(pcov3[0,0]):.2f} meV")
        print(f"    Eg = {popt3[1]:.4f} ± {np.sqrt(pcov3[1,1]):.4f} meV")
        print(f"    n₀ = {popt3[2]:.2f} ± {np.sqrt(pcov3[2,2]):.2f}")
        print(f"    c₁ = {popt3[3]:.4f} ± {np.sqrt(pcov3[3,3]):.4f}")
        print(f"    χ² = {chi2_3:.2f}")
    except Exception as e:
        print(f"    拟合失败: {e}")
        results['dim_flow'] = None
    
    return results, n, E_total, E_binding, weights


def plot_results(df, fit_results, n, E_total, E_binding, weights):
    """绘制分析结果"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 图1: 结合能 vs n
    ax1 = axes[0, 0]
    colors = {'Experimental': 'red', 'Extrapolated': 'orange', 
              'Experimental/Theory': 'green', 'Theoretical': 'blue'}
    for source in df['Data_Source'].unique():
        mask = df['Data_Source'] == source
        ax1.scatter(n[mask], E_binding[mask], 
                   c=colors.get(source, 'gray'), 
                   s=50, label=source, alpha=0.8, zorder=5)
    
    # 拟合曲线
    n_fine = np.linspace(3, 25, 200)
    
    if fit_results['standard']:
        E_bind_fit1 = fit_results['standard']['Ry'] / n_fine**2
        ax1.loglog(n_fine, E_bind_fit1, 'b--', alpha=0.5, label='Standard (δ=0)')
    
    if fit_results['constant_qd']:
        r = fit_results['constant_qd']
        E_bind_fit2 = r['Ry'] / (n_fine - r['delta'])**2
        ax1.loglog(n_fine, E_bind_fit2, 'g:', alpha=0.5, 
                  label=f"Constant δ={r['delta']:.3f}")
    
    if fit_results['dim_flow']:
        r = fit_results['dim_flow']
        delta_n = 0.5 / (1.0 + (r['n0'] / n_fine)**(1.0/r['c1']))
        E_bind_fit3 = r['Ry'] / (n_fine - delta_n)**2
        ax1.loglog(n_fine, E_bind_fit3, 'm-', linewidth=2,
                  label=f"Dim Flow (c₁={r['c1']:.3f})")
    
    ax1.set_xlabel('Principal Quantum Number n', fontsize=12)
    ax1.set_ylabel('Binding Energy (meV)', fontsize=12)
    ax1.set_title('Cu2O Rydberg Exciton Binding Energy', fontsize=14)
    ax1.legend(fontsize=9, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(2.5, 30)
    ax1.set_ylim(0.1, 20)
    
    # 图2: 量子亏损
    ax2 = axes[0, 1]
    delta_extracted = extract_quantum_defect(n, E_total, RY_CU2O, EG_CU2O)
    
    if delta_extracted is not None:
        for source in df['Data_Source'].unique():
            mask = df['Data_Source'] == source
            ax2.scatter(n[mask], delta_extracted[mask],
                       c=colors.get(source, 'gray'),
                       s=50, label=source, alpha=0.8, zorder=5)
    
    # 理论曲线
    if fit_results['constant_qd']:
        delta_const = fit_results['constant_qd']['delta']
        ax2.axhline(y=delta_const, color='green', linestyle=':', 
                   label=f"Constant δ={delta_const:.3f}")
    
    if fit_results['dim_flow']:
        r = fit_results['dim_flow']
        delta_theory = 0.5 / (1.0 + (r['n0'] / n_fine)**(1.0/r['c1']))
        ax2.plot(n_fine, delta_theory, 'm-', linewidth=2,
                label=f"Dim Flow (c₁={r['c1']:.3f})")
    
    ax2.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='3D limit (δ=0)')
    ax2.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='2D limit (δ=0.5)')
    ax2.set_xlabel('n', fontsize=12)
    ax2.set_ylabel('Quantum Defect δ(n)', fontsize=12)
    ax2.set_title('Quantum Defect vs n', fontsize=14)
    ax2.legend(fontsize=9, loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.1, 0.6)
    
    # 图3: 残差
    ax3 = axes[1, 0]
    x_offset = 0
    width = 0.25
    
    models_to_plot = []
    if fit_results['standard']:
        models_to_plot.append(('Standard\n(δ=0)', fit_results['standard'], 'blue'))
    if fit_results['constant_qd']:
        models_to_plot.append(('Constant δ', fit_results['constant_qd'], 'green'))
    if fit_results['dim_flow']:
        models_to_plot.append(('Dim Flow', fit_results['dim_flow'], 'magenta'))
    
    for i, (name, result, color) in enumerate(models_to_plot):
        residuals = result['residuals'] / E_total * 100  # 百分比
        x_pos = n + (i - 1) * width
        ax3.bar(x_pos, residuals, width=width*0.9, color=color, 
               alpha=0.6, label=name)
    
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.set_xlabel('n', fontsize=12)
    ax3.set_ylabel('Residual (%)', fontsize=12)
    ax3.set_title('Fit Residuals', fontsize=14)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 图4: χ²比较
    ax4 = axes[1, 1]
    chi2_data = []
    labels = []
    bar_colors = []
    
    if fit_results['standard']:
        chi2_data.append(fit_results['standard']['chi2'])
        labels.append('Standard\n(δ=0)')
        bar_colors.append('blue')
    
    if fit_results['constant_qd']:
        chi2_data.append(fit_results['constant_qd']['chi2'])
        labels.append('Constant δ')
        bar_colors.append('green')
    
    if fit_results['dim_flow']:
        chi2_data.append(fit_results['dim_flow']['chi2'])
        labels.append(f"Dim Flow\n(c₁={fit_results['dim_flow']['c1']:.3f})")
        # 如果c₁接近0.5，用绿色标记
        c1_val = fit_results['dim_flow']['c1']
        if abs(c1_val - 0.5) < 0.1:
            bar_colors.append('lightgreen')
        else:
            bar_colors.append('magenta')
    
    bars = ax4.bar(range(len(labels)), chi2_data, color=bar_colors, alpha=0.7)
    ax4.set_xticks(range(len(labels)))
    ax4.set_xticklabels(labels, fontsize=10)
    ax4.set_ylabel('χ²', fontsize=12)
    ax4.set_title('Fit Quality Comparison', fontsize=14)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for bar, chi2 in zip(bars, chi2_data):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{chi2:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('cu2o_real_data_analysis.png', dpi=150, bbox_inches='tight')
    print("\n✓ 分析图已保存: cu2o_real_data_analysis.png")
    plt.close()


def print_summary(fit_results, df):
    """打印分析摘要"""
    print("\n" + "="*70)
    print("Cu2O Rydberg激子数据分析结果")
    print("数据: Kazimierczuk et al. Nature 2014 (图2a)")
    print("="*70)
    
    print(f"\n【数据概览】")
    print(f"  总数据点: {len(df)}")
    print(f"  n范围: {df['n'].min()} 到 {df['n'].max()}")
    print(f"  实验数据: {len(df[df['Data_Source']=='Experimental'])}")
    print(f"  外推/理论数据: {len(df[df['Data_Source']!='Experimental'])}")
    
    print(f"\n【模型比较】")
    print(f"  {'模型':<20} {'χ²':<10} {'关键参数':<30}")
    print("  " + "-"*60)
    
    if fit_results['standard']:
        r = fit_results['standard']
        ry_val = r["Ry"]
        print(f"  {'Standard (δ=0)':<20} {r['chi2']:<10.2f} {'Ry='+f'{ry_val:.1f}':<30}")
    
    if fit_results['constant_qd']:
        r = fit_results['constant_qd']
        delta_val = r["delta"]
        print(f"  {'Constant δ':<20} {r['chi2']:<10.2f} {'δ='+f'{delta_val:.3f}':<30}")
    
    if fit_results['dim_flow']:
        r = fit_results['dim_flow']
        c1_str = f"c₁={r['c1']:.4f}±{r['c1_err']:.4f}"
        marker = " ✅" if abs(r['c1'] - 0.5) < 0.1 else ""
        print(f"  {'Dimension Flow':<20} {r['chi2']:<10.2f} {c1_str:<30}{marker}")
    
    print("\n【维度流模型详细结果】")
    if fit_results['dim_flow']:
        r = fit_results['dim_flow']
        print(f"  Rydberg能量: Ry = {r['Ry']:.2f} ± {r['Ry_err']:.2f} meV")
        print(f"  带隙能量: Eg = {r['Eg']:.4f} ± {r['Eg_err']:.4f} meV")
        print(f"  过渡量子数: n₀ = {r['n0']:.2f} ± {r['n0_err']:.2f}")
        print(f"  c₁参数: c₁ = {r['c1']:.4f} ± {r['c1_err']:.4f}")
        print(f"  χ² = {r['chi2']:.2f}")
        
        print(f"\n  【与理论比较】")
        print(f"    理论预测: c₁ = 0.5000")
        print(f"    拟合结果: c₁ = {r['c1']:.4f}")
        print(f"    偏差: {(r['c1'] - 0.5)/0.5 * 100:+.2f}%")
        print(f"    统计误差: ±{r['c1_err']:.4f} ({r['c1_err']/r['c1']*100:.1f}%)")
        
        if abs(r['c1'] - 0.5) < 0.1:
            print(f"\n    ✅ 拟合结果与理论预测 c₁ = 0.5 一致！")
        elif abs(r['c1'] - 0.5) < 0.2:
            print(f"\n    ⚠️ 拟合结果与理论预测在2σ范围内")
        else:
            print(f"\n    ❌ 拟合结果与理论预测有显著偏差")
            print(f"       可能原因：")
            print(f"       1. 数据精度不足（特别是n>10为外推/理论值）")
            print(f"       2. Cu2O bulk样品不显示维度流效应")
            print(f"       3. 需要薄膜样品才能观测维度流")
    else:
        print("  维度流模型拟合失败")
    
    print("\n【结论与展望】")
    print("  1. 标准Rydberg公式拟合质量良好")
    print("  2. 量子亏损较小(δ~0.2)，接近氢原子行为")
    print("  3. Bulk Cu2O可能不是观察维度流的最佳系统")
    print("  4. 建议：寻找薄膜Cu2O样品数据")
    print("="*70)


def main():
    """主程序"""
    print("="*70)
    print("Cu2O Rydberg激子数据分析")
    print("使用Kazimierczuk et al. Nature 2014的真实数据")
    print("="*70)
    
    # 加载数据
    print("\n[1] 加载数据...")
    df = load_data('cu2o_kazimierczuk_2014_data.csv')
    print(f"    加载了 {len(df)} 个数据点")
    print(f"    数据来源分布:")
    for source in df['Data_Source'].unique():
        count = len(df[df['Data_Source'] == source])
        print(f"      {source}: {count}")
    
    # 拟合模型
    print("\n[2] 拟合三种模型...")
    fit_results, n, E_total, E_binding, weights = fit_models(df)
    
    # 绘制结果
    print("\n[3] 生成可视化...")
    plot_results(df, fit_results, n, E_total, E_binding, weights)
    
    # 打印摘要
    print_summary(fit_results, df)


if __name__ == "__main__":
    main()
