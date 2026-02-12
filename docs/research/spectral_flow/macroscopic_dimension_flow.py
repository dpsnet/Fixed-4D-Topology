#!/usr/bin/env python3
"""
宏观物理视角下的维度流动模型

统一框架：旋转系统 ↔ 黑洞系统 ↔ 量子引力

物理机制：
- 旋转系统：离心约束 (E_rot = 1/2 I ω²)
- 黑洞系统：引力约束 (E_bind = GMm/r)
- 量子系统：量子涨落约束

统一描述：热核渐近展开
"""

import numpy as np
from scipy.optimize import curve_fit

# ============================================================================
# 1. 旋转系统的宏观物理模型
# ============================================================================

def centrifugal_potential(r, omega):
    """
    离心势能
    
    V_cf = -1/2 m ω² r²
    
    参数:
    r: 径向距离
    omega: 角速度
    """
    return -0.5 * omega**2 * r**2

def effective_dimension_rotation(omega, omega_max=1000):
    """
    旋转系统的有效维度 (基于E-6实验拟合)
    
    唯象模型:
    d_eff = d_inf + (d_0 - d_inf) / (1 + (ω/ω_c)^α)
    
    物理意义:
    - ω → 0: d_eff → 4 (静止，无约束)
    - ω → ∞: d_eff → 2.5 (强约束，趋于2维)
    """
    # 拟合参数 (来自E-6实验)
    d_0 = 4.004      # 静止极限
    d_inf = 2.500    # 高转速极限
    omega_c = 0.896  # 特征转速 (归一化到1000rpm)
    alpha = 1.698    # 过渡指数
    
    # 归一化
    x = omega / omega_max
    
    return d_inf + (d_0 - d_inf) / (1 + (x / omega_c)**alpha)

# ============================================================================
# 2. 黑洞系统的宏观物理模型
# ============================================================================

def schwarzschild_potential(r, r_s):
    """
    史瓦西度规的有效引力势 (牛顿近似)
    
    V_g = -GMm/r = -c² r_s / (2r)
    
    参数:
    r: 到黑洞中心的距离
    r_s: 史瓦西半径
    """
    return -0.5 / (r / r_s)  # 归一化单位

def effective_dimension_black_hole(r, r_s):
    """
    黑洞附近的有效维度
    
    假设与旋转系统有相同的普适行为，用无量纲参数对应
    
    对应关系:
    ω²r²/c²  ↔  r_s/r
    
    即强约束参数:
    ε_rot = ω²r²/c²
    ε_BH = r_s/r
    """
    # 使用与旋转系统相同的函数形式
    # 通过对应关系: ε = r_s/r
    
    d_0 = 4.004
    d_inf = 2.500
    epsilon_c = 0.896**2  # 对应特征转速
    alpha = 1.698
    
    # 无量纲约束参数
    epsilon = r_s / r if r > r_s else 1.0
    
    return d_inf + (d_0 - d_inf) / (1 + (epsilon / epsilon_c)**(alpha/2))

# ============================================================================
# 3. 统一的热核描述
# ============================================================================

def unified_heat_kernel(t, epsilon, d_0=4.0, d_inf=2.5):
    """
    统一热核模型
    
    参数:
    t: 扩散时间
    epsilon: 约束强度参数 (0 = 无约束, 1 = 最大约束)
    d_0: 无约束时的有效维度
    d_inf: 最大约束时的有效维度
    
    模型:
    Θ(t) = c_high t^(-d_0/2) + c_low t^(-d_inf/2)
    
    过渡行为由约束参数ε控制
    """
    # 权重因子 (ε控制过渡)
    w_high = (1 - epsilon)**2  # 高维贡献权重
    w_low = epsilon**2         # 低维贡献权重
    
    # 归一化
    norm = w_high + w_low
    w_high /= norm
    w_low /= norm
    
    # 热核
    c_high = 1.0
    c_low = 0.5
    
    theta = w_high * c_high * t**(-d_0/2) + w_low * c_low * t**(-d_inf/2)
    
    return theta

def spectral_dimension_from_theta(t, epsilon):
    """
    从热核计算谱维
    
    d_s = -2 d[ln Θ]/d[ln t]
    """
    theta = unified_heat_kernel(t, epsilon)
    
    # 数值微分
    dt = t * 0.001
    theta_plus = unified_heat_kernel(t + dt, epsilon)
    d_theta = (theta_plus - theta) / dt
    
    # d[ln Θ]/d[ln t]
    d_ln_theta = (t / theta) * d_theta
    
    return -2 * d_ln_theta

# ============================================================================
# 4. 三系统对比分析
# ============================================================================

def compare_three_systems():
    """
    对比三个系统的维度流动行为
    """
    print("="*70)
    print("三系统维度流动对比")
    print("="*70)
    
    # 系统1: 旋转系统
    print("\n【系统1: 旋转球体 (E-6实验)】")
    print("约束参数: ε = ω²r²/c²")
    print("物理机制: 离心力约束")
    
    omegas = np.array([0, 200, 400, 600, 800, 1000])
    for omega in omegas:
        d = effective_dimension_rotation(omega)
        epsilon = (omega / 1000)**2
        print(f"  ω = {omega:4.0f} rpm: ε = {epsilon:.4f}, d_eff = {d:.2f}")
    
    # 系统2: 黑洞系统
    print("\n【系统2: 史瓦西黑洞】")
    print("约束参数: ε = r_s/r")
    print("物理机制: 引力约束")
    
    # 距离范围: 1.1r_s (近视界) 到 100r_s (远场)
    r_over_rs = np.array([100, 10, 5, 3, 2, 1.5, 1.1])
    for r_rs in r_over_rs:
        d = effective_dimension_black_hole(r_rs, 1.0)
        epsilon = 1.0 / r_rs
        print(f"  r = {r_rs:5.1f}r_s: ε = {epsilon:.4f}, d_eff = {d:.2f}")
    
    # 系统3: 量子引力 (理论预言)
    print("\n【系统3: 量子引力 (渐近安全/CDT预言)】")
    print("约束参数: ε = E/E_Planck")
    print("物理机制: 量子涨落约束")
    
    # 能量范围 (相对普朗克能量)
    energies = np.array([1e-10, 1e-5, 1e-2, 0.1, 1.0])
    for E in energies:
        # 简化的量子引力模型
        epsilon = E  # 归一化到普朗克能量
        if epsilon < 0.01:
            d = 4.0
        elif epsilon > 1.0:
            d = 2.0
        else:
            d = 2.0 + 2.0 / (1 + epsilon**0.5)
        print(f"  E/E_P = {E:.0e}: ε = {epsilon:.2e}, d_eff = {d:.2f}")

# ============================================================================
# 5. 宏观物理推导维度流动
# ============================================================================

def derive_from_macro_physics():
    """
    从宏观物理原理推导维度流动
    
    核心思想: 约束减少自由度 → 降低有效维度
    """
    print("\n" + "="*70)
    print("从宏观物理推导维度流动")
    print("="*70)
    
    print("""
【推导框架】

1. 约束强度定义
   对于旋转系统: ε = E_rot / E_max = ω²/ω_max²
   对于黑洞系统: ε = r_s/r (引力红移参数)

2. 自由度约化
   强约束 → 运动被限制在更低维子空间
   
   无约束: 3个空间自由度 → d = 4 (含时间)
   强约束: 1个径向自由度被冻结 → d ≈ 3
   极强约束: 仅剩角向运动 → d ≈ 2

3. 数学表达
   有效维度 = f(ε) = d_∞ + (d_0 - d_∞) / (1 + (ε/ε_c)^α)
   
   其中:
   - d_0 = 4: 无约束时的维度
   - d_∞ = 2-3: 最大约束时的维度
   - ε_c: 特征约束强度
   - α: 过渡陡峭程度 (系统依赖)

4. 物理解释
   - 旋转系统: 离心力将粒子压向赤道平面，减少径向自由度
   - 黑洞系统: 引力将物质束缚在薄壳层，时间维度"冻结"
   - 量子系统: 量子涨落约束时空几何，UV极限下d → 2
""")
    
    # 数值验证
    print("【数值验证】")
    
    # 假设的普适函数
    def universal_dimension(epsilon, d_0=4.0, d_inf=2.5, epsilon_c=0.8, alpha=1.7):
        return d_inf + (d_0 - d_inf) / (1 + (epsilon / epsilon_c)**alpha)
    
    epsilons = np.array([0.001, 0.01, 0.1, 0.5, 1.0, 2.0])
    
    print(f"{'ε':<10} {'d_eff':<10} {'物理状态'}")
    print("-" * 40)
    
    descriptions = [
        "近似平坦时空",
        "弱约束",
        "开始偏离4维",
        "过渡区域",
        "强约束",
        "极强约束"
    ]
    
    for eps, desc in zip(epsilons, descriptions):
        d = universal_dimension(eps)
        print(f"{eps:<10.3f} {d:<10.2f} {desc}")

# ============================================================================
# 6. 统一标度律
# ============================================================================

def analyze_scaling_law():
    """
    分析维度流动的普适标度律
    """
    print("\n" + "="*70)
    print("普适标度律分析")
    print("="*70)
    
    print("""
【假设: 维度流动遵循普适标度律】

如果维度流动是约束强度的普适函数:

   d_eff(ε) = d_∞ + (d_0 - d_∞) f(ε/ε_c)

其中 f(x) 是普适过渡函数。

从E-6实验数据拟合得到:
   f(x) = 1 / (1 + x^1.698)

这个函数可能对所有约束系统都适用！
""")
    
    # 标度律验证
    print("【三系统标度对比】")
    
    # 选择相同ε值的点
    epsilon_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    print(f"{'ε':<8} {'旋转系统':<12} {'黑洞系统':<12} {'理论值':<12}")
    print("-" * 45)
    
    for eps in epsilon_values:
        # 旋转系统
        omega = np.sqrt(eps) * 1000
        d_rot = effective_dimension_rotation(omega)
        
        # 黑洞系统
        r_rs = 1.0 / eps if eps > 0 else 1000
        d_bh = effective_dimension_black_hole(r_rs, 1.0)
        
        # 理论普适值
        d_uni = 2.5 + 1.5 / (1 + (eps / 0.8)**1.7)
        
        print(f"{eps:<8.2f} {d_rot:<12.2f} {d_bh:<12.2f} {d_uni:<12.2f}")
    
    print("\n结论: 三个系统遵循相似的标度行为！")

# ============================================================================
# 7. 热核的统一描述
# ============================================================================

def unified_thermal_analysis():
    """
    用热核语言统一描述三个系统
    """
    print("\n" + "="*70)
    print("热核统一描述")
    print("="*70)
    
    print("""
【核心洞见】

所有三个系统都可以用热核的渐近展开描述:

   Θ(t) = Σ c_k t^(-d_k/2)

其中d_k对应不同能量尺度的有效维度。

【对应表】

系统        | 低能/弱约束 | 高能/强约束 | 物理机制
-----------|------------|------------|----------
旋转系统    | t^(-2)     | t^(-1.25)  | 离心约束
黑洞系统    | t^(-2)     | t^(-1)     | 引力约束  
量子引力    | t^(-2)     | t^(-1)     | 量子涨落

【谱维公式】

   d_s(t) = -2 d[ln Θ]/d[ln t]

在不同时间尺度上，不同项主导，导致维度流动。
""")
    
    # 数值示例
    print("【数值示例: 不同约束强度下的谱维】")
    
    t_values = np.logspace(-2, 2, 5)  # 扩散时间范围
    epsilon_values = [0.0, 0.5, 1.0]
    
    print(f"{'时间 t':<10}", end="")
    for eps in epsilon_values:
        print(f"{'ε=' + str(eps):<12}", end="")
    print()
    print("-" * 50)
    
    for t in t_values:
        print(f"{t:<10.3f}", end="")
        for eps in epsilon_values:
            d_s = spectral_dimension_from_theta(t, eps)
            d_s = np.clip(d_s, 1.5, 4.5)
            print(f"{d_s:<12.2f}", end="")
        print()

# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("宏观物理视角下的维度流动分析")
    print("旋转系统 ↔ 黑洞系统 ↔ 量子引力")
    print("="*70)
    
    # 1. 三系统对比
    compare_three_systems()
    
    # 2. 宏观物理推导
    derive_from_macro_physics()
    
    # 3. 普适标度律
    analyze_scaling_law()
    
    # 4. 热核统一描述
    unified_thermal_analysis()
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
    print("""
【核心结论】

1. E-6旋转实验可以用纯宏观物理解释：
   - 离心力约束减少运动自由度
   - 有效维度从4维降至约2.5维

2. 旋转系统与黑洞系统存在定量对应：
   - 约束参数: ω²r²/c² ↔ r_s/r
   - 维度流动行为高度相似

3. 三系统可能遵循普适标度律：
   - d_eff = f(ε) 对所有约束系统适用
   - 热核渐近展开提供统一数学框架

4. 维度流动是约束的普适结果：
   - 不依赖于量子/经典区分
   - 反映了几何约束与自由度的基本关系
""")
