#!/usr/bin/env python3
"""
Kerr旋转黑洞中的维度流动数值计算

计算不同旋转参数 chi = a/(r_s/2) 和位置下的有效维度
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无显示环境使用

# ============================================================================
# 1. Kerr度规工具函数
# ============================================================================

def rho_squared(r, theta, a):
    """
    Kerr度规函数 ρ² = r² + a²cos²θ
    
    参数:
    r: 径向坐标
    theta: 极角
    a: 单位质量角动量
    """
    return r**2 + a**2 * np.cos(theta)**2

def Delta(r, r_s, a):
    """
    Kerr度规函数 Δ = r² - r_s*r + a²
    """
    return r**2 - r_s*r + a**2

def Sigma(r, theta, r_s, a):
    """
    Kerr度规函数 Σ = (r² + a²)² - Δ*a²*sin²θ
    """
    delta = Delta(r, r_s, a)
    return (r**2 + a**2)**2 - delta * a**2 * np.sin(theta)**2

# ============================================================================
# 2. Kerr度规分量
# ============================================================================

def kerr_metric_components(r, theta, r_s, a):
    """
    计算Kerr度规的分量
    
    返回: (g_tt, g_rr, g_theta, g_phi, g_tphi)
    """
    rho2 = rho_squared(r, theta, a)
    delta = Delta(r, r_s, a)
    sigma = Sigma(r, theta, r_s, a)
    
    # 度规分量
    g_tt = -(1 - r_s * r / rho2)
    g_rr = rho2 / delta
    g_theta = rho2
    g_phi = sigma * np.sin(theta)**2 / rho2
    g_tphi = -r_s * r * a * np.sin(theta)**2 / rho2
    
    return g_tt, g_rr, g_theta, g_phi, g_tphi

def horizon_radius(r_s, a):
    """
    Kerr事件视界半径
    
    r_+ = r_s/2 + sqrt((r_s/2)² - a²)
    """
    M = r_s / 2  # 质量参数
    if a > M:
        return None  # 裸奇点
    return M + np.sqrt(M**2 - a**2)

def ergosphere_radius(r_s, a, theta):
    """
    能层边界 (静态极限)
    
    r_ergo = r_s/2 + sqrt((r_s/2)² - a²cos²θ)
    """
    M = r_s / 2
    inside_sqrt = M**2 - a**2 * np.cos(theta)**2
    if inside_sqrt < 0:
        return M  # 全空间都在能层内
    return M + np.sqrt(inside_sqrt)

def horizon_angular_velocity(r_s, a):
    """
    视界角速度
    
    Ω_H = a / (r_+² + a²)
    """
    r_p = horizon_radius(r_s, a)
    if r_p is None:
        return None
    return a / (r_p**2 + a**2)

# ============================================================================
# 3. 维度流动计算
# ============================================================================

def effective_dimension_Kerr(r_over_rs, chi, theta, r_s=1.0):
    """
    计算Kerr黑洞中特定位置的有效维度
    
    使用唯象模型:
    d_eff = d_inf(chi) + (d_0 - d_inf(chi)) / (1 + (epsilon/epsilon_c)^alpha)
    
    参数:
    r_over_rs: 距离/史瓦西半径
    chi: 无量纲旋转参数 chi = a/(r_s/2) ∈ [0, 1]
    theta: 极角 (0=北极, π/2=赤道)
    """
    a = chi * r_s / 2  # 角动量参数
    r = r_over_rs * r_s
    
    # 检查是否在视界内
    r_horizon = horizon_radius(r_s, a)
    if r_horizon and r <= r_horizon:
        return 2.0  # 视界内设为2维
    
    # 基础参数 (来自史瓦西)
    d_0 = 4.0
    epsilon_c = 0.8
    alpha = 1.7
    
    # 角动量依赖的极限维度
    # 假设: d_inf(chi) = 2.5 - 0.5 * chi
    d_inf = 2.5 - 0.5 * chi
    
    # 角度依赖的修正
    # 赤道(theta=π/2)效应最强, 极区(theta=0)效应最弱
    theta_factor = np.sin(theta)**2  # 0到1
    
    # 修正d_inf
    d_inf_eff = d_inf - 0.3 * chi * theta_factor
    
    # 约束参数 (包含角度依赖)
    epsilon = r_s / r
    
    # 能层增强效应
    r_ergo = ergosphere_radius(r_s, a, theta)
    if r_ergo and r < r_ergo:
        # 在能层内, 增强维度流动
        ergo_factor = 1.0 + 0.2 * (1.0 - r / r_ergo) * chi
        epsilon *= ergo_factor
    
    # 计算维度
    d_eff = d_inf_eff + (d_0 - d_inf_eff) / (1 + (epsilon / epsilon_c)**alpha)
    
    return max(2.0, min(4.0, d_eff))

def compare_Schwarzschild_vs_Kerr():
    """
    对比史瓦西和Kerr黑洞的维度流动
    """
    print("="*70)
    print("史瓦西 vs Kerr 维度流动对比")
    print("="*70)
    
    # 参数设置
    r_over_rs_values = np.array([100, 10, 5, 3, 2, 1.5, 1.2])
    chi_values = np.array([0.0, 0.3, 0.5, 0.7, 0.9, 0.99])
    theta_equator = np.pi / 2  # 赤道
    
    print("\n【赤道平面 (θ = π/2) 的维度流动】")
    print(f"{'r/r_s':<10}", end="")
    for chi in chi_values:
        print(f"χ={chi:<5.2f}", end="")
    print()
    print("-" * 70)
    
    for r_over_rs in r_over_rs_values:
        print(f"{r_over_rs:<10.1f}", end="")
        for chi in chi_values:
            d = effective_dimension_Kerr(r_over_rs, chi, theta_equator)
            print(f"{d:<8.2f}", end="")
        print()
    
    # 角度依赖
    print("\n【角度依赖 (χ = 0.9, r/r_s = 2.0)】")
    theta_values = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
    print(f"{'θ (deg)':<12} {'d_eff':<10} {'sin²θ':<10}")
    print("-" * 35)
    
    r_test = 2.0
    chi_test = 0.9
    for theta in theta_values:
        d = effective_dimension_Kerr(r_test, chi_test, theta)
        theta_deg = theta * 180 / np.pi
        sin2_theta = np.sin(theta)**2
        print(f"{theta_deg:<12.0f} {d:<10.2f} {sin2_theta:<10.3f}")

# ============================================================================
# 4. 旋转参数依赖分析
# ============================================================================

def analyze_spin_dependence():
    """
    分析维度流动对旋转参数的依赖
    """
    print("\n" + "="*70)
    print("旋转参数依赖分析")
    print("="*70)
    
    # 固定位置, 变化旋转参数
    r_over_rs = 2.0
    chi_values = np.linspace(0, 0.99, 20)
    theta = np.pi / 2
    
    print(f"\n固定位置: r/r_s = {r_over_rs}")
    print(f"{'χ':<10} {'a/M':<10} {'d_eff':<10} {'Δd':<10}")
    print("-" * 40)
    
    d_schwarzschild = effective_dimension_Kerr(r_over_rs, 0.0, theta)
    
    for chi in chi_values[::4]:  # 采样
        a_over_M = chi
        d = effective_dimension_Kerr(r_over_rs, chi, theta)
        delta_d = d - d_schwarzschild
        print(f"{chi:<10.2f} {a_over_M:<10.2f} {d:<10.2f} {delta_d:<10.2f}")
    
    # 极限行为
    print(f"\n极限分析:")
    print(f"  史瓦西极限 (χ=0): d_eff = {d_schwarzschild:.2f}")
    d_extreme = effective_dimension_Kerr(r_over_rs, 0.99, theta)
    print(f"  极端Kerr (χ=0.99): d_eff = {d_extreme:.2f}")
    print(f"  维度降低: {d_schwarzschild - d_extreme:.2f}")

# ============================================================================
# 5. 能层效应分析
# ============================================================================

def analyze_ergosphere():
    """
    分析能层内的维度流动
    """
    print("\n" + "="*70)
    print("能层效应分析")
    print("="*70)
    
    r_s = 1.0
    chi = 0.9
    a = chi * r_s / 2
    
    print(f"旋转参数: χ = {chi}")
    print(f"角动量: a = {a:.3f}M")
    
    # 视界和能层边界
    r_horizon = horizon_radius(r_s, a)
    r_ergo_equator = ergosphere_radius(r_s, a, np.pi/2)
    r_ergo_pole = ergosphere_radius(r_s, a, 0)
    
    print(f"\n边界位置:")
    print(f"  视界半径: r_+/r_s = {r_horizon/r_s:.3f}")
    print(f"  能层边界 (赤道): r_ergo/r_s = {r_ergo_equator/r_s:.3f}")
    print(f"  能层边界 (极区): r_ergo/r_s = {r_ergo_pole/r_s:.3f}")
    
    # 能层内的维度流动
    print(f"\n能层内的维度流动 (赤道):")
    r_values = np.linspace(r_horizon*1.01, r_ergo_equator*1.1, 10)
    print(f"{'r/r_s':<10} {'区域':<15} {'d_eff':<10}")
    print("-" * 40)
    
    for r in r_values:
        r_over_rs = r / r_s
        d = effective_dimension_Kerr(r_over_rs, chi, np.pi/2)
        
        if r < r_ergo_equator:
            region = "能层内"
        else:
            region = "能层外"
        
        print(f"{r_over_rs:<10.3f} {region:<15} {d:<10.2f}")

# ============================================================================
# 6. 与E-6旋转系统的深化对应
# ============================================================================

def E6_Kerr_correspondence():
    """
    E-6实验与Kerr黑洞的深化对应
    """
    print("\n" + "="*70)
    print("E-6实验 ↔ Kerr黑洞 深化对应")
    print("="*70)
    
    print("""
对应关系:
  E-6实验          Kerr黑洞
  ─────────────────────────────
  转速 ω          视界角速度 Ω_H
  离心约束        引力+旋转约束
  赤道效应最强    赤道效应最强
  维度: 4→2.5    维度: 4→2.0
""")
    
    # 定量对应
    print("定量对应示例:")
    
    # E-6参数
    omega_max = 1000  # rpm
    omega_values = np.array([0, 200, 400, 600, 800, 1000])
    
    # 对应的Kerr参数 (近似)
    chi_equiv = 0.9  # 高旋转
    r_s_equiv = 1.0
    
    print(f"{'ω (rpm)':<12} {'ε_E6':<10} {'对应 r/r_s':<12} {'d_E6':<8} {'d_Kerr':<8}")
    print("-" * 55)
    
    for omega in omega_values:
        epsilon_E6 = (omega / omega_max)**2
        
        # 近似对应
        if epsilon_E6 > 0:
            r_over_rs_equiv = 1.0 / epsilon_E6
        else:
            r_over_rs_equiv = float('inf')
        
        # 计算维度
        d_E6 = 2.5 + 1.5 / (1 + (epsilon_E6 / 0.8)**1.7) if epsilon_E6 > 0 else 4.0
        
        if r_over_rs_equiv < 100:
            d_Kerr = effective_dimension_Kerr(r_over_rs_equiv, chi_equiv, np.pi/2)
        else:
            d_Kerr = 4.0
        
        r_str = f"{r_over_rs_equiv:.1f}" if r_over_rs_equiv < 100 else "∞"
        print(f"{omega:<12.0f} {epsilon_E6:<10.4f} {r_str:<12} {d_E6:<8.2f} {d_Kerr:<8.2f}")

# ============================================================================
# 7. 黑洞阴影预测
# ============================================================================

def shadow_size_prediction():
    """
    预测Kerr黑洞阴影的大小
    """
    print("\n" + "="*70)
    print("黑洞阴影大小预测")
    print("="*70)
    
    print("""
维度流动对黑洞阴影的影响:

  标准预测: R_shadow ≈ 5.2 GM/c² (史瓦西)
  
  维度流动修正:
    R_shadow ≈ R_shadow^Schw × (1 - α × χ²)
    
  其中 α 是维度流动相关的参数
""")
    
    chi_values = np.array([0.0, 0.3, 0.5, 0.7, 0.9, 0.99])
    
    print(f"{'χ':<10} {'R_shadow/R_s':<15} {'修正因子':<12}")
    print("-" * 40)
    
    for chi in chi_values:
        # 简化的阴影大小公式
        # R ∝ 1/√(d_eff - 2) 的启发式关系
        r_test = 2.5  # 特征位置
        d_eff = effective_dimension_Kerr(r_test, chi, np.pi/2)
        
        # 启发式阴影大小
        R_shadow = 5.2 * np.sqrt(2.0 / (d_eff - 1.9))  # 启发式
        correction = R_shadow / 5.2
        
        print(f"{chi:<10.2f} {R_shadow:<15.3f} {correction:<12.3f}")

# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Kerr旋转黑洞中的维度流动数值分析")
    print("="*70)
    
    # 1. 史瓦西 vs Kerr 对比
    compare_Schwarzschild_vs_Kerr()
    
    # 2. 旋转参数依赖
    analyze_spin_dependence()
    
    # 3. 能层效应
    analyze_ergosphere()
    
    # 4. E-6对应
    E6_Kerr_correspondence()
    
    # 5. 阴影预测
    shadow_size_prediction()
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
    print("""
【主要结论】

1. 旋转降低有效维度:
   - 史瓦西 (χ=0): d_eff → 2.5
   - 极端Kerr (χ=0.99): d_eff → 2.0

2. 角度依赖:
   - 赤道效应最强
   - 极区接近史瓦西值

3. 能层增强效应:
   - 能层内维度流动更显著
   - d_eff 可低至2.0

4. 与E-6实验对应:
   - 旋转系统对应中等旋转黑洞
   - 维度流动行为一致

【下一步】
- 高精度谱计算
- EHT观测对比
- 引力波模板
""")
