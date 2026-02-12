#!/usr/bin/env python3
"""
优化版: 从Theorem A生成E-6实验的理论预测曲线

关键修正:
- 空间维数: 3 (宏观) → 1 (高能极限，因为旋转约束)
- 谱维: d_s = d_eff - 1 (减去时间维)
- 需要更复杂的热核模型来捕捉从高维到低维的转变

Theorem A扩展:
Θ_Γ(t) = c_3 t^(-3/2) + c_2 t^(-1) + c_δ t^(-(1+δ)/2) + O(t^(-1/2))

其中不同能量(时间)尺度主导不同项:
- 低能(大t): c_3 项主导 (d=3空间)
- 中能: c_2 项主导 (d=2空间) 
- 高能(小t): c_δ 项主导 (d=δ分形)
"""

import numpy as np

def heat_kernel_extended(t, c3, c2, cdelta, delta):
    """
    扩展热核迹模型，捕捉多尺度行为
    
    参数:
    t: 扩散时间
    c3: 3维空间系数
    c2: 2维空间系数  
    cdelta: 分形修正系数
    delta: Hausdorff维数
    """
    term_3d = c3 * (t ** (-3/2))      # 3维空间贡献
    term_2d = c2 * (t ** (-1))         # 2维空间贡献
    term_frac = cdelta * (t ** (-(1 + delta)/2))  # 分形贡献
    
    return term_3d + term_2d + term_frac

def spectral_dimension_extended(t, c3, c2, cdelta, delta):
    """
    从扩展热核计算谱维
    """
    theta = heat_kernel_extended(t, c3, c2, cdelta, delta)
    
    # 数值微分
    dt = t * 0.0001
    theta_plus = heat_kernel_extended(t + dt, c3, c2, cdelta, delta)
    d_theta_dt = (theta_plus - theta) / dt
    
    # d[ln Θ]/d[ln t]
    d_ln_theta_d_ln_t = (t / theta) * d_theta_dt
    
    # 谱维
    d_s = -2 * d_ln_theta_d_ln_t
    
    return d_s

def theoretical_model_for_E6():
    """
    为E-6实验优化的理论模型
    
    实验显示: d_eff: 4 → 3 → 2 (含时间维)
    对应谱维: d_s: 3 → 2 → 1
    
    物理图像:
    - 低转速(低能): 3维空间 + 1维时间 = 4维
    - 中转速: 离心力开始约束，有效2维平面 + 1维时间 = 3维
    - 高转速(高能): 极端约束，1维径向 + 1维时间 = 2维
    """
    # 参数校准以匹配实验
    c3 = 1.0        # 3维主导
    c2 = 0.3        # 2维贡献
    cdelta = 0.1    # 分形贡献
    delta = 0.5     # 低维极限的Hausdorff维数
    
    # 能量范围 (对应转速 0-1000 rpm)
    # E ~ ω²，从0.001到100
    E_values = np.logspace(-3, 2, 200)
    
    # 能量到时间的映射
    # 高能 ↔ 小时间 (更短扩散时间)
    t_values = 10.0 / E_values  # 反比关系
    
    results = []
    for t in t_values:
        d_s = spectral_dimension_extended(t, c3, c2, cdelta, delta)
        # 限制在合理范围
        d_s = np.clip(d_s, 0.5, 4.0)
        d_eff = d_s + 1  # 加时间维
        results.append((t, d_s, d_eff))
    
    return E_values, np.array(results)

def compare_with_experiment():
    """
    理论与实验数据对比分析
    """
    # E-6实验数据
    rpm_data = [0, 200, 400, 500, 600, 800, 1000]
    d_eff_exp = [4.0, 3.9, 3.7, 3.6, 3.5, 3.3, 3.2]
    
    # 能量映射 (E ∝ ω²)
    E_exp = np.array([(r/1000)**2 * 100 if r > 0 else 0.001 for r in rpm_data])
    
    # 理论预测
    E_theory, results = theoretical_model_for_E6()
    d_eff_theory = results[:, 2]
    
    print("="*70)
    print("E-6实验与Theorem A扩展模型对比")
    print("="*70)
    
    print("\n实验数据:")
    print(f"{'转速(rpm)':<12} {'能量E':<12} {'d_eff(实验)':<15}")
    print("-" * 40)
    for i in range(len(rpm_data)):
        print(f"{rpm_data[i]:<12} {E_exp[i]:<12.4f} {d_eff_exp[i]:<15.2f}")
    
    print("\n理论预测 (选取匹配点):")
    print(f"{'能量E':<12} {'d_eff(理论)':<15}")
    print("-" * 30)
    for E_t, d_t in zip(E_theory[::25], d_eff_theory[::25]):
        print(f"{E_t:<12.4f} {d_t:<15.2f}")
    
    # 计算匹配误差
    print("\n定量对比:")
    print(f"实验范围: {min(d_eff_exp):.2f} - {max(d_eff_exp):.2f}")
    print(f"理论范围: {min(d_eff_theory):.2f} - {max(d_eff_theory):.2f}")
    
    return E_exp, d_eff_exp, E_theory, d_eff_theory

def coefficient_quarter_analysis():
    """
    分析系数1/4如何影响谱维流动的形状
    """
    print("\n" + "="*70)
    print("系数 c₁ = 1/4 对谱维流动曲线形状的影响")
    print("="*70)
    
    # 测试不同cdelta值 (假设 cdelta ∝ c1)
    cdelta_values = [0.05, 0.1, 0.15, 0.25]  # 0.25 = 1/4
    
    c3 = 1.0
    c2 = 0.3
    delta = 0.5
    
    print("\n不同 c_δ 参数下的维度流动范围:")
    print(f"{'c_δ':<10} {'d_s(低能)':<12} {'d_s(高能)':<12} {'流动幅度':<12}")
    print("-" * 50)
    
    for cdelta in cdelta_values:
        # 低能 (大t)
        t_low = 1000.0
        d_s_low = spectral_dimension_extended(t_low, c3, c2, cdelta, delta)
        
        # 高能 (小t)
        t_high = 0.01
        d_s_high = spectral_dimension_extended(t_high, c3, c2, cdelta, delta)
        
        amplitude = d_s_low - d_s_high
        marker = " <-- 1/4!" if abs(cdelta - 0.25) < 0.01 else ""
        
        print(f"{cdelta:<10.2f} {d_s_low:<12.2f} {d_s_high:<12.2f} {amplitude:<12.2f}{marker}")
    
    print("\n分析结论:")
    print("- c_δ 控制流动的'陡峭程度'")
    print("- c_δ = 1/4 时可能对应某种普适性 (如临界现象)")
    print("- 需要更精细的模型来验证这一假设")

if __name__ == "__main__":
    print("="*70)
    print("T3替代研究: 优化版谱维流动预测")
    print("扩展热核模型匹配E-6实验数据")
    print("="*70)
    
    # 理论与实验对比
    compare_with_experiment()
    
    # 系数分析
    coefficient_quarter_analysis()
    
    print("\n" + "="*70)
    print("下一步: 需要更精确的实验数据来拟合理论参数")
    print("="*70)
