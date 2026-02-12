#!/usr/bin/env python3
"""
时空有效维度流动模型 v2: 优化版

物理对应关系:
- 静止状态 (ω=0): d_eff = 4
- 高转速: d_eff → 2

能量-时间关系:
- E ~ ω² (旋转能量)
- t ~ 1/E ~ 1/ω² (扩散时间与能量成反比)

热核模型:
Θ(t) = c_4 t^(-2) + c_2 t^(-1) + 交叉项
"""

import numpy as np
from scipy.optimize import minimize, curve_fit

def dimension_flow_model(omega, d_inf, d_0, omega_c, alpha):
    """
    维度流动唯象模型
    
    d_eff(ω) = d_0 + (d_inf - d_0) * f(ω/ω_c)
    
    其中 f(x) = 1 / (1 + x^α) 是过渡函数
    
    参数:
    - d_inf: ω→∞ 极限 (约等于2)
    - d_0: ω=0 极限 (约等于4)
    - omega_c: 特征转速 (过渡点)
    - alpha: 过渡陡峭程度 (可能与c₁=1/4相关)
    """
    x = omega / omega_c
    f = 1 / (1 + x ** alpha)
    return d_inf + (d_0 - d_inf) * f

def fit_phenomenological_model():
    """
    拟合E-6实验数据使用唯象模型
    """
    # 实验数据
    rpm_data = np.array([0, 200, 400, 500, 600, 800, 1000])
    d_eff_exp = np.array([4.0, 3.9, 3.7, 3.6, 3.5, 3.3, 3.2])
    
    # 角速度 (归一化)
    omega = rpm_data / 1000.0
    
    # 使用curve_fit拟合
    # 初始猜测: d_inf=2, d_0=4, omega_c=0.3, alpha=1
    p0 = [2.0, 4.0, 0.3, 1.0]
    bounds = ([1.5, 3.5, 0.01, 0.1], [2.5, 4.5, 1.0, 5.0])
    
    try:
        popt, pcov = curve_fit(dimension_flow_model, omega, d_eff_exp, p0=p0, bounds=bounds)
        d_inf, d_0, omega_c, alpha = popt
        
        # 计算拟合质量
        d_eff_pred = dimension_flow_model(omega, *popt)
        residuals = d_eff_exp - d_eff_pred
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((d_eff_exp - np.mean(d_eff_exp)) ** 2)
        r2 = 1 - ss_res / ss_tot
        
        print("="*70)
        print("唯象模型拟合结果")
        print("="*70)
        print(f"\n拟合参数:")
        print(f"  d_inf (ω→∞极限) = {d_inf:.4f}")
        print(f"  d_0 (ω=0极限) = {d_0:.4f}")
        print(f"  ω_c (特征转速/1000) = {omega_c:.4f}")
        print(f"  α (过渡指数) = {alpha:.4f}")
        
        print(f"\n拟合质量:")
        print(f"  R² = {r2:.6f}")
        print(f"  均方误差 = {ss_res/len(omega):.6f}")
        
        # 详细对比
        print(f"\n数据对比:")
        print(f"{'ω (x1000)':<12} {'实验值':<12} {'拟合值':<12} {'残差':<12}")
        print("-" * 50)
        for i in range(len(omega)):
            print(f"{omega[i]:<12.4f} {d_eff_exp[i]:<12.2f} {d_eff_pred[i]:<12.2f} {residuals[i]:<12.4f}")
        
        return popt, r2
        
    except Exception as e:
        print(f"拟合失败: {e}")
        return None, None

def test_quarter_hypothesis():
    """
    测试系数1/4假设
    
    如果过渡指数 α = 1/2，则暗示某种普适标度律
    """
    print("\n" + "="*70)
    print("c₁ = 1/4 假设检验")
    print("="*70)
    
    # 使用固定 α = 0.5 (对应 c₁ = 1/4 的某种关联)
    rpm_data = np.array([0, 200, 400, 500, 600, 800, 1000])
    d_eff_exp = np.array([4.0, 3.9, 3.7, 3.6, 3.5, 3.3, 3.2])
    omega = rpm_data / 1000.0
    
    def fixed_alpha_model(omega, d_inf, d_0, omega_c):
        return dimension_flow_model(omega, d_inf, d_0, omega_c, alpha=0.5)
    
    try:
        popt, pcov = curve_fit(fixed_alpha_model, omega, d_eff_exp, p0=[2.0, 4.0, 0.3])
        d_eff_pred = fixed_alpha_model(omega, *popt)
        
        r2 = 1 - np.sum((d_eff_exp - d_eff_pred)**2) / np.sum((d_eff_exp - np.mean(d_eff_exp))**2)
        
        print(f"固定 α = 0.5 的拟合:")
        print(f"  d_inf = {popt[0]:.4f}")
        print(f"  d_0 = {popt[1]:.4f}")
        print(f"  ω_c = {popt[2]:.4f}")
        print(f"  R² = {r2:.6f}")
        
        # 与自由拟合比较
        popt_free, r2_free = fit_phenomenological_model()
        if popt_free is not None:
            print(f"\n自由拟合 α = {popt_free[3]:.4f}, R² = {r2_free:.6f}")
            print(f"固定 α = 0.5, R² = {r2:.6f}")
            print(f"R²差异 = {abs(r2 - r2_free):.6f}")
            
            if abs(r2 - r2_free) < 0.01:
                print("\n✓ α = 0.5 (可能与c₁=1/4相关) 与自由拟合几乎等效!")
            else:
                print(f"\n可能需要其他指数，或数据点不足以确定普适指数")
        
        return r2
        
    except Exception as e:
        print(f"固定α拟合失败: {e}")
        return None

def theoretical_interpretation():
    """
    理论解释与c₁=1/4的可能联系
    """
    print("\n" + "="*70)
    print("理论解释")
    print("="*70)
    
    print("""
【维度流动的物理机制】

1. 静止状态 (ω = 0):
   - 完整4维时空 (3空间 + 1时间)
   - 热核主导项: t^(-2)

2. 中等转速:
   - 离心力开始约束运动
   - 有效维度降低至约3维
   
3. 高转速 (ω → ∞):
   - 强约束下有效维度趋于2维
   - 可能对应1维径向 + 1维时间
   - 热核主导项: t^(-1)

【与c₁=1/4的可能联系】

虽然唯象模型给出 α ≈ 0.75，但这可能与多种因素相关：
- 系统几何 (球体 vs 其他形状)
- 边界条件
- 测量方法

c₁ = 1/4 更可能出现在：
1. 分形维数修正项的系数
2. 过渡函数的普适指数 (在特定条件下)
3. 与解析挠率相关的深层常数

需要更精细的实验和理论分析来确定这一联系。
""")

def generate_prediction_curve():
    """
    生成理论预测曲线
    """
    rpm_data = np.array([0, 200, 400, 500, 600, 800, 1000])
    d_eff_exp = np.array([4.0, 3.9, 3.7, 3.6, 3.5, 3.3, 3.2])
    omega = rpm_data / 1000.0
    
    # 拟合
    popt, _ = curve_fit(dimension_flow_model, omega, d_eff_exp, 
                       p0=[2.0, 4.0, 0.3, 1.0],
                       bounds=([1.5, 3.5, 0.01, 0.1], [2.5, 4.5, 1.0, 5.0]))
    
    # 生成连续曲线
    omega_fine = np.linspace(0, 1.2, 200)
    rpm_fine = omega_fine * 1000
    d_eff_pred = dimension_flow_model(omega_fine, *popt)
    
    # 输出关键点的预测值
    print("\n" + "="*70)
    print("理论预测曲线关键点")
    print("="*70)
    print(f"{'转速(rpm)':<12} {'预测d_eff':<12} {'状态描述'}")
    print("-" * 50)
    
    key_points = [0, 100, 200, 300, 500, 700, 1000, 1200]
    for rpm in key_points:
        omega_pt = rpm / 1000.0
        d_pred = dimension_flow_model(omega_pt, *popt)
        if rpm == 0:
            desc = "4维时空"
        elif rpm < 300:
            desc = "4→3维过渡"
        elif rpm < 700:
            desc = "3维主导"
        elif rpm < 1000:
            desc = "3→2维过渡"
        else:
            desc = "接近2维极限"
        print(f"{rpm:<12} {d_pred:<12.2f} {desc}")
    
    return rpm_fine, d_eff_pred

if __name__ == "__main__":
    print("="*70)
    print("时空维度流动分析 v2")
    print("4维 → 3维 → 2维")
    print("="*70)
    
    # 1. 唯象模型拟合
    popt, r2 = fit_phenomenological_model()
    
    # 2. 1/4假设检验
    r2_fixed = test_quarter_hypothesis()
    
    # 3. 理论解释
    theoretical_interpretation()
    
    # 4. 预测曲线
    rpm_fine, d_pred = generate_prediction_curve()
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
