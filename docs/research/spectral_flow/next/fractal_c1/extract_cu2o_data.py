#!/usr/bin/env python3
"""
Cu2O Rydberg激子数据提取与分析
基于文献中的信息重建能级数据
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# 从Kazimierczuk et al. Nature 2014 论文中提取的已知参数
CU2O_PARAMETERS = {
    "Ry": 92,           # meV, Rydberg能量
    "Eg": 2172.08,      # meV, 带隙能量 (2.17208 eV)
    "n_max": 25,        # 观测到的最高量子数
    "delta_approx": 0.2,  # 量子亏损近似值（文献提及）
}


def energy_rydberg_hydrogen(n, Ry, Eg):
    """
    标准氢原子Rydberg公式
    E_n = Eg - Ry/n²
    """
    return Eg - Ry / n**2


def energy_rydberg_quantum_defect(n, Ry, Eg, delta):
    """
    含量子亏损的Rydberg公式
    E_n = Eg - Ry/(n - δ)²
    """
    return Eg - Ry / (n - delta)**2


def energy_dimension_flow(n, Ry, Eg, n0, c1):
    """
    维度流修正的Rydberg公式
    δ(n) = 0.5 / (1 + (n₀/n)^(1/c₁))
    """
    delta = 0.5 / (1.0 + (n0 / n)**(1.0/c1))
    return Eg - Ry / (n - delta)**2


def generate_literature_based_data():
    """
    基于文献信息重建能级数据
    
    策略：
    1. 使用量子亏损模型生成"真实"能级
    2. 添加合理噪声模拟实验误差
    3. 尝试用维度流模型拟合
    """
    
    params = CU2O_PARAMETERS
    n_values = np.arange(3, params["n_max"] + 1)
    
    # 方法1: 使用常数量子亏损 (文献中δ≈0.2)
    delta_constant = 0.22
    E_constant_qd = np.array([energy_rydberg_quantum_defect(n, params["Ry"], 
                                                               params["Eg"], 
                                                               delta_constant) 
                               for n in n_values])
    
    # 方法2: 使用维度流模型 (c₁=0.5理论预测)
    n0_guess = 15.0  # 过渡量子数
    c1_theory = 0.5
    E_dim_flow = np.array([energy_dimension_flow(n, params["Ry"], 
                                                  params["Eg"], 
                                                  n0_guess, 
                                                  c1_theory) 
                            for n in n_values])
    
    # 方法3: 纯氢原子（无修正）
    E_hydrogen = np.array([energy_rydberg_hydrogen(n, params["Ry"], params["Eg"]) 
                           for n in n_values])
    
    # 添加噪声（模拟实验数据）
    noise_level = 0.001  # 0.1% 能量分辨率 (~2-20 μeV)
    E_simulated = E_constant_qd * (1 + noise_level * np.random.randn(len(n_values)))
    
    return {
        "n": n_values,
        "E_constant_qd": E_constant_qd,
        "E_dim_flow": E_dim_flow,
        "E_hydrogen": E_hydrogen,
        "E_simulated": E_simulated,
        "params": params,
        "noise_level": noise_level
    }


def fit_models(data):
    """
    用不同模型拟合数据，比较拟合质量
    """
    n = data["n"]
    E = data["E_simulated"]
    params = data["params"]
    
    # 模型1: 纯氢原子 (δ=0)
    def model_hydrogen(n, Ry, Eg):
        return Eg - Ry / n**2
    
    # 模型2: 常数量子亏损
    def model_constant_qd(n, Ry, Eg, delta):
        return Eg - Ry / (n - delta)**2
    
    # 模型3: 维度流
    def model_dim_flow(n, Ry, Eg, n0, c1):
        delta_n = 0.5 / (1.0 + (n0 / n)**(1.0/c1))
        return Eg - Ry / (n - delta_n)**2
    
    results = {}
    
    # 拟合模型1
    try:
        popt1, _ = curve_fit(model_hydrogen, n, E, 
                            p0=[params["Ry"], params["Eg"]],
                            maxfev=10000)
        E_fit1 = model_hydrogen(n, *popt1)
        chi2_1 = np.sum(((E - E_fit1) / (E * data["noise_level"]))**2)
        results["hydrogen"] = {
            "params": popt1,
            "chi2": chi2_1,
            "Ry": popt1[0],
            "Eg": popt1[1]
        }
    except Exception as e:
        results["hydrogen"] = {"error": str(e)}
    
    # 拟合模型2
    try:
        popt2, _ = curve_fit(model_constant_qd, n, E,
                            p0=[params["Ry"], params["Eg"], 0.2],
                            bounds=([50, 2150, 0], [150, 2200, 1]),
                            maxfev=10000)
        E_fit2 = model_constant_qd(n, *popt2)
        chi2_2 = np.sum(((E - E_fit2) / (E * data["noise_level"]))**2)
        results["constant_qd"] = {
            "params": popt2,
            "chi2": chi2_2,
            "Ry": popt2[0],
            "Eg": popt2[1],
            "delta": popt2[2]
        }
    except Exception as e:
        results["constant_qd"] = {"error": str(e)}
    
    # 拟合模型3
    try:
        popt3, _ = curve_fit(model_dim_flow, n, E,
                            p0=[params["Ry"], params["Eg"], 10.0, 0.5],
                            bounds=([50, 2150, 1, 0.1], [150, 2200, 50, 2]),
                            maxfev=10000)
        E_fit3 = model_dim_flow(n, *popt3)
        chi2_3 = np.sum(((E - E_fit3) / (E * data["noise_level"]))**2)
        results["dim_flow"] = {
            "params": popt3,
            "chi2": chi2_3,
            "Ry": popt3[0],
            "Eg": popt3[1],
            "n0": popt3[2],
            "c1": popt3[3]
        }
    except Exception as e:
        results["dim_flow"] = {"error": str(e)}
    
    return results


def plot_comparison(data, fit_results):
    """
    绘制不同模型的比较
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    n = data["n"]
    E_sim = data["E_simulated"]
    params = data["params"]
    
    # 图1: 能级图
    ax1 = axes[0, 0]
    ax1.scatter(n, E_sim, c='red', s=50, label='Simulated Data', zorder=5)
    ax1.plot(n, data["E_hydrogen"], 'b--', label='Hydrogen (δ=0)', alpha=0.7)
    ax1.plot(n, data["E_constant_qd"], 'g:', label=f'Constant δ={CU2O_PARAMETERS["delta_approx"]}', alpha=0.7)
    ax1.plot(n, data["E_dim_flow"], 'm-', label='Dimension Flow (c₁=0.5)', alpha=0.7)
    ax1.set_xlabel('Principal Quantum Number n', fontsize=12)
    ax1.set_ylabel('Energy (meV)', fontsize=12)
    ax1.set_title('Cu2O Rydberg Exciton Energy Levels', fontsize=14)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # 图2: 相对于带隙的结合能
    ax2 = axes[0, 1]
    binding_sim = params["Eg"] - E_sim
    binding_h = params["Eg"] - data["E_hydrogen"]
    binding_qd = params["Eg"] - data["E_constant_qd"]
    binding_df = params["Eg"] - data["E_dim_flow"]
    
    ax2.loglog(n, binding_sim, 'ro', label='Data')
    ax2.loglog(n, binding_h, 'b--', label='Hydrogen ∝ 1/n²', alpha=0.7)
    ax2.loglog(n, binding_qd, 'g:', label='Constant δ', alpha=0.7)
    ax2.loglog(n, binding_df, 'm-', label='Dimension Flow', alpha=0.7)
    ax2.set_xlabel('n', fontsize=12)
    ax2.set_ylabel('Binding Energy (meV)', fontsize=12)
    ax2.set_title('Binding Energy vs n (Log-Log)', fontsize=14)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # 图3: 量子亏损提取
    ax3 = axes[1, 0]
    # 从数据反推量子亏损
    delta_extracted = n - np.sqrt(params["Ry"] / (params["Eg"] - E_sim))
    # 理论曲线
    n_fine = np.linspace(3, 25, 100)
    delta_theory = 0.5 / (1.0 + (15.0/n_fine)**2)  # c₁=0.5, n₀=15
    delta_constant = np.full_like(n_fine, 0.22)
    
    ax3.scatter(n, delta_extracted, c='red', s=50, label='Extracted from Data')
    ax3.plot(n_fine, delta_theory, 'm-', linewidth=2, label='Dimension Flow (c₁=0.5)')
    ax3.plot(n_fine, delta_constant, 'g:', linewidth=2, label='Constant δ=0.22')
    ax3.axhline(y=0, color='blue', linestyle='--', alpha=0.5, label='Hydrogen (δ=0)')
    ax3.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='2D limit (δ=0.5)')
    ax3.set_xlabel('n', fontsize=12)
    ax3.set_ylabel('Quantum Defect δ(n)', fontsize=12)
    ax3.set_title('Quantum Defect vs n', fontsize=14)
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-0.1, 0.6)
    
    # 图4: 拟合比较
    ax4 = axes[1, 1]
    models = []
    chi2_vals = []
    colors = []
    
    if "hydrogen" in fit_results and "chi2" in fit_results["hydrogen"]:
        models.append("Hydrogen\n(δ=0)")
        chi2_vals.append(fit_results["hydrogen"]["chi2"])
        colors.append('blue')
    
    if "constant_qd" in fit_results and "chi2" in fit_results["constant_qd"]:
        models.append(f"Constant δ\n(δ={fit_results['constant_qd']['delta']:.3f})")
        chi2_vals.append(fit_results["constant_qd"]["chi2"])
        colors.append('green')
    
    if "dim_flow" in fit_results and "chi2" in fit_results["dim_flow"]:
        c1_fit = fit_results["dim_flow"]["c1"]
        models.append(f"Dimension Flow\n(c₁={c1_fit:.3f})")
        chi2_vals.append(fit_results["dim_flow"]["chi2"])
        colors.append('magenta' if abs(c1_fit - 0.5) < 0.1 else 'orange')
    
    bars = ax4.bar(range(len(models)), chi2_vals, color=colors, alpha=0.7)
    ax4.set_xticks(range(len(models)))
    ax4.set_xticklabels(models, fontsize=10)
    ax4.set_ylabel('χ²', fontsize=12)
    ax4.set_title('Fit Quality Comparison', fontsize=14)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for bar, chi2 in zip(bars, chi2_vals):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{chi2:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('cu2o_analysis_simulated.png', dpi=150, bbox_inches='tight')
    print("✓ 分析图已保存: cu2o_analysis_simulated.png")
    plt.close()


def print_analysis_results(data, fit_results):
    """
    打印分析结果摘要
    """
    params = data["params"]
    
    print("\n" + "="*70)
    print("Cu2O Rydberg激子分析结果")
    print("="*70)
    
    print("\n【已知参数 (来自Kazimierczuk et al. Nature 2014)】")
    print(f"  Rydberg能量: Ry = {params['Ry']} meV")
    print(f"  带隙能量: Eg = {params['Eg']} meV ({params['Eg']/1000:.3f} eV)")
    print(f"  最高观测n: n_max = {params['n_max']}")
    print(f"  文献量子亏损: δ ≈ {params['delta_approx']}")
    
    print("\n【拟合结果比较】")
    print(f"  {'模型':<25} {'χ²':<12} {'关键参数':<20}")
    print("  " + "-"*60)
    
    for model_name, result in fit_results.items():
        if "chi2" in result:
            if model_name == "hydrogen":
                print(f"  {'Hydrogen (δ=0)':<25} {result['chi2']:<12.2f} {'Ry='+str(result['Ry']):<20}")
            elif model_name == "constant_qd":
                delta_val = result["delta"]
                print(f"  {'Constant δ':<25} {result['chi2']:<12.2f} {'δ='+f'{delta_val:.3f}':<20}")
            elif model_name == "dim_flow":
                c1_str = f"c₁={result['c1']:.3f}"
                marker = " ✅" if abs(result['c1'] - 0.5) < 0.05 else ""
                print(f"  {'Dimension Flow':<25} {result['chi2']:<12.2f} {c1_str:<20}{marker}")
    
    # 判断最佳模型
    if "dim_flow" in fit_results and "chi2" in fit_results["dim_flow"]:
        c1_fit = fit_results["dim_flow"]["c1"]
        print("\n【维度流模型关键发现】")
        print(f"  拟合c₁值: {c1_fit:.4f}")
        print(f"  理论预测: 0.5000")
        print(f"  偏差: {(c1_fit - 0.5)/0.5 * 100:+.2f}%")
        
        if abs(c1_fit - 0.5) < 0.1:
            print("  ✅ 拟合结果与理论预测 c₁ = 0.5 一致！")
        else:
            print("  ⚠️ 拟合结果与理论预测有偏差")
    
    print("="*70)


def main():
    """主程序"""
    print("="*70)
    print("Cu2O Rydberg激子数据分析")
    print("基于Kazimierczuk et al. Nature 2014")
    print("="*70)
    
    np.random.seed(42)
    
    # 生成基于文献的模拟数据
    print("\n[1] 生成基于文献的模拟数据...")
    data = generate_literature_based_data()
    print(f"    生成 {len(data['n'])} 个能级 (n=3 到 n={data['n'][-1]})")
    
    # 拟合不同模型
    print("\n[2] 拟合不同模型...")
    fit_results = fit_models(data)
    
    # 绘制比较图
    print("\n[3] 生成可视化...")
    plot_comparison(data, fit_results)
    
    # 打印结果
    print_analysis_results(data, fit_results)
    
    print("\n【说明】")
    print("  本分析使用基于文献参数的模拟数据")
    print("  下一步：获取真实实验数据进行验证")
    print("="*70)


if __name__ == "__main__":
    main()
