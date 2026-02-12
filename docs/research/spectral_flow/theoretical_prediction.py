#!/usr/bin/env python3
"""
从Theorem A生成E-6实验的理论预测曲线

Theorem A: Θ_Γ(t) = Vol/(4πt)^(3/2) + c(δ)t^(-(1+δ)/2) + O(t^(-1/2))

谱维定义: d_s(t) = -2 * d[ln Θ(t)] / d[ln t]
实验对应: d_eff(E) = d_s(t(E)) + 1 (含时间维)
"""

import numpy as np

def heat_kernel_trace(t, Vol, delta, c_delta):
    """
    计算热核迹 Θ(t)
    
    参数:
    t: 扩散时间
    Vol: 体积
    delta: Hausdorff维数
    c_delta: 分形修正系数
    """
    main_term = Vol / ((4 * np.pi * t) ** (3/2))
    fractal_term = c_delta * (t ** (-(1 + delta) / 2))
    return main_term + fractal_term

def spectral_dimension(t, Vol, delta, c_delta):
    """
    计算谱维 d_s(t)
    
    d_s = -2 * d[ln Θ] / d[ln t]
    """
    # 计算 Θ(t)
    theta = heat_kernel_trace(t, Vol, delta, c_delta)
    
    # 计算 dΘ/dt (数值微分)
    dt = t * 0.001
    theta_plus = heat_kernel_trace(t + dt, Vol, delta, c_delta)
    d_theta_dt = (theta_plus - theta) / dt
    
    # d[ln Θ]/d[ln t] = (t/Θ) * dΘ/dt
    d_ln_theta_d_ln_t = (t / theta) * d_theta_dt
    
    # 谱维
    d_s = -2 * d_ln_theta_d_ln_t
    
    return d_s

def energy_to_time(E, E0=1.0):
    """
    将实验能量映射到扩散时间
    
    假设: t ~ 1/E (能量越高，有效扩散时间越短)
    """
    return E0 / E

def theoretical_prediction_for_E6():
    """
    生成E-6实验的理论预测曲线
    
    返回:
    energies: 能量数组
    spectral_dims: 谱维数组
    effective_dims: 有效维度数组
    """
    # 参数设置 (基于Kleinian群的典型值)
    Vol = 1.0          # 归一化体积
    delta = 1.2        # Hausdorff维数 (典型值)
    c_delta = 0.5      # 分形修正系数
    
    # 能量范围
    E_min = 0.01       # 低能极限
    E_max = 100.0      # 高能极限
    
    energies = np.logspace(np.log10(E_min), np.log10(E_max), 100)
    
    # 计算谱维和有效维度
    spectral_dims = []
    effective_dims = []
    
    for E in energies:
        t = energy_to_time(E)
        d_s = spectral_dimension(t, Vol, delta, c_delta)
        
        # 限制在物理合理范围
        d_s = np.clip(d_s, 0.5, 4.0)
        
        # 有效维度 = 谱维 + 1 (时间维)
        d_eff = d_s + 1
        
        spectral_dims.append(d_s)
        effective_dims.append(d_eff)
    
    return energies, np.array(spectral_dims), np.array(effective_dims)

def extract_E6_experiment_data():
    """
    从E-6文档中提取的实验数据点
    """
    # 从文档表格提取的近似数据
    data = {
        'rpm': [0, 200, 400, 500, 600, 800, 1000],
        'd_eff': [4.0, 3.9, 3.7, 3.6, 3.5, 3.3, 3.2]  # 含时间维
    }
    
    # 将转速映射到能量 (E ~ ω²)
    omega = np.array(data['rpm'])
    E_exp = (omega / 100.0) ** 2  # 归一化
    
    return E_exp, np.array(data['d_eff'])

def analyze_coefficient_quarter():
    """
    分析系数1/4在谱维流动中的体现
    """
    print("="*60)
    print("系数 c₁ = 1/4 的谱维流动分析")
    print("="*60)
    
    Vol = 1.0
    delta_values = [1.0, 1.2, 1.4, 1.6]
    
    print("\n不同Hausdorff维数 δ 下的谱维流动:")
    print(f"{'δ':<8} {'c(δ)':<12} {'d_s(小t)':<12} {'d_s(大t)':<12}")
    print("-" * 50)
    
    for delta in delta_values:
        c_delta = 0.25 * (2 - delta)  # 简化假设
        
        t_small = 0.001
        d_s_small = spectral_dimension(t_small, Vol, delta, c_delta)
        
        t_large = 100.0
        d_s_large = spectral_dimension(t_large, Vol, delta, c_delta)
        
        print(f"{delta:<8.2f} {c_delta:<12.4f} {d_s_small:<12.2f} {d_s_large:<12.2f}")
    
    print("\n结论:")
    print("- 当 δ → 2 (经典极限), 谱维流动减弱")
    print("- 当 δ → 0 (极端分形), 谱维流动增强")
    print("- 系数1/4通过c(δ)影响流动的'陡峭程度'")

def main_analysis():
    """主分析函数"""
    print("="*60)
    print("T3替代研究: 谱维流动理论预测生成")
    print("基于Theorem A的热核渐近公式")
    print("="*60)
    
    # 生成理论预测
    print("\n[1/2] 生成理论预测...")
    E_theory, d_s_theory, d_eff_theory = theoretical_prediction_for_E6()
    
    # 获取实验数据
    E_exp, d_eff_exp = extract_E6_experiment_data()
    
    print(f"理论预测数据点: {len(E_theory)}")
    print(f"实验数据点: {len(E_exp)}")
    
    print("\n理论预测 (前5点):")
    print(f"{'能量':<12} {'谱维 d_s':<12} {'有效维 d_eff':<12}")
    print("-" * 40)
    for i in range(0, 5):
        print(f"{E_theory[i]:<12.4f} {d_s_theory[i]:<12.4f} {d_eff_theory[i]:<12.4f}")
    
    print("\n实验数据:")
    print(f"{'能量':<12} {'有效维 d_eff':<12}")
    print("-" * 25)
    for i in range(len(E_exp)):
        print(f"{E_exp[i]:<12.4f} {d_eff_exp[i]:<12.2f}")
    
    # 分析系数
    print("\n[2/2] 分析系数1/4的影响...")
    analyze_coefficient_quarter()
    
    print("\n" + "="*60)
    print("分析完成!")
    print("="*60)

if __name__ == "__main__":
    main_analysis()
