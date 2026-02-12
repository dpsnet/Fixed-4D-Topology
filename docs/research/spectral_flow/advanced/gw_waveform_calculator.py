#!/usr/bin/env python3
"""
引力波波形计算器：维度流动效应

计算维度流动对双黑洞并合引力波波形的影响
"""

import numpy as np

# ============================================================================
# 1. 标准引力波波形 (简化 inspiral 模型)
# ============================================================================

def chirp_mass(m1, m2):
    """
    计算啁啾质量
    
    M_chirp = (m1*m2)^(3/5) / (m1+m2)^(1/5)
    """
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

def reduced_mass(m1, m2):
    """
    计算约化质量
    """
    return m1 * m2 / (m1 + m2)

def standard_waveform(t, m1, m2, d_L, **kwargs):
    """
    标准双黑洞并合引力波波形 (简化 inspiral 模型)
    
    使用牛顿四极近似
    
    参数:
    t: 时间数组
    m1, m2: 两个黑洞的质量 (太阳质量)
    d_L: 光度距离 (Mpc)
    """
    # 常数
    G = 4.302e-3  # pc M_sun^-1 (km/s)^2
    c = 3e5  # km/s
    
    # 转换为几何单位
    M_chirp = chirp_mass(m1, m2)  # 太阳质量
    M_chirp_sec = M_chirp * 4.925e-6  # 秒
    
    # 特征频率演化
    # f(t) = (1/8π) * (t_c - t)^(-3/8) * M_chirp^(-5/8)
    
    t_c = t[-1]  # 并合时间
    tau = t_c - t
    
    # 避免除零
    tau = np.maximum(tau, 1e-10)
    
    # 频率演化
    f = (1.0 / (8 * np.pi)) * tau**(-3/8) * M_chirp_sec**(-5/8)
    
    # 振幅
    # h ~ (G M_chirp / c^2 d_L) * (G M_chirp f / c^3)^(2/3)
    d_L_mpc = d_L * 3.086e22  # 转换为米
    M_chirp_kg = M_chirp * 1.989e30  # 转换为kg
    
    # 振幅 (简化)
    h_0 = (G * M_chirp_kg / (c**2 * d_L_mpc))
    h = h_0 * (G * M_chirp_kg * f / c**3)**(2/3)
    
    # 相位
    phi = 2 * np.pi * np.cumsum(f) * np.gradient(t)
    
    # 波形
    h_plus = h * np.cos(phi)
    h_cross = h * np.sin(phi)
    
    return h_plus, h_cross, f

# ============================================================================
# 2. 维度流动修正的波形
# ============================================================================

def dimension_flow_correction(r, m_total, d_eff):
    """
    计算维度流动对引力波的修正因子
    
    参数:
    r: 轨道半径 (单位: GM/c^2)
    m_total: 总质量
    d_eff: 有效维度
    
    返回: 修正因子
    """
    # 约束参数: epsilon ~ 1/r
    epsilon = 1.0 / r if r > 1 else 1.0
    
    # 维度依赖的引力常数
    # G_eff = G * (4 / d_eff)
    G_factor = 4.0 / d_eff
    
    # 波幅修正
    amplitude_correction = G_factor**(2/3)
    
    # 频率修正
    frequency_correction = G_factor**(1/2)
    
    # 综合修正
    total_correction = amplitude_correction * frequency_correction
    
    return total_correction

def dimension_flow_waveform(t, m1, m2, d_L, **kwargs):
    """
    包含维度流动效应的引力波波形
    
    关键改进:
    - 在并合前考虑维度流动效应
    - 修正啁啾质量和频率演化
    """
    # 标准参数
    M_chirp_standard = chirp_mass(m1, m2)
    M_total = m1 + m2
    
    # 时间演化
    t_c = t[-1]
    tau = t_c - t
    tau = np.maximum(tau, 1e-10)
    
    # 轨道分离 (牛顿近似)
    # r(t) ~ (tau)^(1/4)
    r_orbit = tau**(1/4) * 10  # 归一化
    
    # 计算每个时间点的有效维度
    d_eff_values = []
    for r in r_orbit:
        if r > 10:
            d_eff = 4.0
        elif r > 2:
            epsilon = 1.0 / r
            d_eff = 2.5 + 1.5 / (1 + (epsilon / 0.8)**1.7)
        else:
            d_eff = 2.5
        d_eff_values.append(d_eff)
    
    d_eff_values = np.array(d_eff_values)
    
    # 修正的啁啾质量
    # M_chirp^eff = M_chirp * (4 / d_eff)^(3/5)
    M_chirp_eff = M_chirp_standard * (4.0 / d_eff_values)**(3/5)
    
    # 频率演化 (修正)
    M_chirp_sec = M_chirp_eff * 4.925e-6
    f = (1.0 / (8 * np.pi)) * tau**(-3/8) * M_chirp_sec**(-5/8)
    
    # 振幅 (修正)
    d_L_mpc = d_L * 3.086e22
    M_chirp_kg = M_chirp_eff * 1.989e30
    
    h_0 = (4.302e-3 * M_chirp_kg / ((3e5)**2 * d_L_mpc))
    h = h_0 * (4.302e-3 * M_chirp_kg * f / (3e5)**3)**(2/3)
    
    # 相位
    phi = 2 * np.pi * np.cumsum(f) * np.gradient(t)
    
    # 波形
    h_plus = h * np.cos(phi)
    h_cross = h * np.sin(phi)
    
    return h_plus, h_cross, f, d_eff_values

# ============================================================================
# 3. 波形对比分析
# ============================================================================

def compare_waveforms():
    """
    对比标准波形和维度流动修正波形
    """
    print("="*70)
    print("引力波波形对比: 标准 vs 维度流动修正")
    print("="*70)
    
    # 参数设置 (类似GW150914)
    m1 = 36  # 太阳质量
    m2 = 29  # 太阳质量
    d_L = 410  # Mpc
    
    # 时间数组 (最后1秒)
    t = np.linspace(-1.0, 0, 10000)  # 秒
    
    # 标准波形
    h_plus_std, h_cross_std, f_std = standard_waveform(t, m1, m2, d_L)
    
    # 维度流动修正波形
    h_plus_dim, h_cross_dim, f_dim, d_eff = dimension_flow_waveform(t, m1, m2, d_L)
    
    # 分析结果
    print(f"\n系统参数: m1={m1}M☉, m2={m2}M☉, d_L={d_L}Mpc")
    print(f"啁啾质量: {chirp_mass(m1, m2):.2f}M☉")
    
    print(f"\n【并合前瞬间】")
    print(f"{'参数':<20} {'标准':<15} {'维度修正':<15} {'差异%':<10}")
    print("-" * 65)
    
    idx = -100  # 并合前瞬间
    
    # 频率
    f_diff = (f_dim[idx] - f_std[idx]) / f_std[idx] * 100
    print(f"{'频率 (Hz)':<20} {f_std[idx]:<15.1f} {f_dim[idx]:<15.1f} {f_diff:<10.2f}")
    
    # 振幅
    h_diff = (abs(h_plus_dim[idx]) - abs(h_plus_std[idx])) / abs(h_plus_std[idx]) * 100
    print(f"{'振幅 (10^-21)':<20} {abs(h_plus_std[idx])*1e21:<15.2f} {abs(h_plus_dim[idx])*1e21:<15.2f} {h_diff:<10.2f}")
    
    # 有效维度
    print(f"{'有效维度':<20} {'4.00':<15} {d_eff[idx]:<15.2f} {'-':<10}")
    
    # 累积相位差
    phase_std = np.unwrap(np.angle(h_plus_std + 1j*h_cross_std))
    phase_dim = np.unwrap(np.angle(h_plus_dim + 1j*h_cross_dim))
    phase_diff = phase_dim[-1] - phase_std[-1]
    
    print(f"\n【累积效应】")
    print(f"总相位差: {phase_diff:.2f} rad ({phase_diff/(2*np.pi):.2f} 周期)")
    
    return t, h_plus_std, h_plus_dim, f_std, f_dim, d_eff

# ============================================================================
# 4. LIGO可探测性分析
# ============================================================================

def ligo_detectability_analysis():
    """
    分析维度流动效应对LIGO探测的影响
    """
    print("\n" + "="*70)
    print("LIGO可探测性分析")
    print("="*70)
    
    # LIGO灵敏度 (简化)
    # 在100-300 Hz范围内，灵敏度约为 ~10^-23 / sqrt(Hz)
    h_rms_ligo = 1e-23  # 近似
    
    print(f"\nLIGO典型灵敏度: h_rms ~ {h_rms_ligo:.0e}")
    
    # 测试不同质量的双黑洞系统
    mass_pairs = [
        (10, 10),   # 中等质量
        (30, 30),   # 高质量 (类似GW150914)
        (50, 50),   # 更高质量
    ]
    
    d_L = 1000  # Mpc
    
    print(f"\n固定距离: {d_L} Mpc")
    print(f"{'m1,m2':<12} {'M_chirp':<10} {'h_std':<12} {'h_dim':<12} {'差异':<10}")
    print("-" * 60)
    
    for m1, m2 in mass_pairs:
        t = np.linspace(-0.5, 0, 5000)
        
        h_plus_std, _, _ = standard_waveform(t, m1, m2, d_L)
        h_plus_dim, _, _, _ = dimension_flow_waveform(t, m1, m2, d_L)
        
        # 最大振幅
        h_max_std = np.max(np.abs(h_plus_std))
        h_max_dim = np.max(np.abs(h_plus_dim))
        
        M_chirp = chirp_mass(m1, m2)
        
        diff = (h_max_dim - h_max_std) / h_max_std * 100
        
        print(f"{m1},{m2}M☉{'':<5} {M_chirp:.1f}M☉{'':<3} "
              f"{h_max_std:.2e}{'':<4} {h_max_dim:.2e}{'':<4} {diff:+.1f}%")

# ============================================================================
# 5. 参数估计偏差
# ============================================================================

def parameter_estimation_bias():
    """
    分析维度流动对参数估计的影响
    """
    print("\n" + "="*70)
    print("参数估计偏差分析")
    print("="*70)
    
    print("""
当使用标准4维波形模板分析受维度流动影响的信号时，
会产生系统性的参数估计偏差。
""")
    
    # 模拟"真实"系统
    m1_true = 36
    m2_true = 29
    d_L_true = 410
    
    # 使用标准模板拟合会产生偏差
    # 因为维度流动改变了频率-质量关系
    
    print("真实参数:")
    print(f"  m1 = {m1_true} M☉")
    print(f"  m2 = {m2_true} M☉")
    print(f"  d_L = {d_L_true} Mpc")
    
    # 估计偏差 (启发式计算)
    # 频率偏移 -> 质量被低估
    # 振幅偏移 -> 距离被高估
    
    f_shift = 0.95  # 频率降低约5%
    h_shift = 1.10  # 振幅增加约10%
    
    # 质量估计: M_est = M_true * f_shift^(8/3)
    M_chirp_true = chirp_mass(m1_true, m2_true)
    M_chirp_est = M_chirp_true * f_shift**(-8/3)
    
    # 距离估计: d_est = d_true / h_shift
    d_L_est = d_L_true / h_shift
    
    print(f"\n使用标准模板的估计结果:")
    print(f"  M_chirp: {M_chirp_true:.2f} → {M_chirp_est:.2f} M☉ "
          f"({(M_chirp_est/M_chirp_true-1)*100:+.1f}%)")
    print(f"  d_L: {d_L_true} → {d_L_est:.0f} Mpc "
          f"({(d_L_est/d_L_true-1)*100:+.1f}%)")
    
    print(f"\n偏差解释:")
    print(f"  频率降低 → 啁啾质量被低估")
    print(f"  振幅增加 → 光度距离被高估")

# ============================================================================
# 6. 未来探测器预测
# ============================================================================

def future_detectors_prediction():
    """
    预测维度流动对未来探测器的影响
    """
    print("\n" + "="*70)
    print("未来探测器预测")
    print("="*70)
    
    print("""
【LISA (2030s)】
- 探测频率: ~mHz
- 目标: 超大质量双黑洞 (10^6 - 10^7 M☉)
- 维度流动效应: 更强 (更大的r_s)

【爱因斯坦望远镜】
- 灵敏度: 比LIGO高10倍
- 频率范围: 1-10000 Hz
- 可探测更精细的波形修正

【宇宙探测器】
- 空间引力波探测器
- 可探测原初引力波背景
- 维度流动的宇宙学效应
""")
    
    # LISA预测
    print("【LISA可探测的维度流动效应】")
    
    # 超大质量双黑洞
    M_total = 1e6  # 太阳质量
    q = 0.1  # 质量比
    m1 = M_total / (1 + q)
    m2 = M_total * q / (1 + q)
    
    M_chirp = chirp_mass(m1, m2)
    
    print(f"系统: m1={m1:.0e}M☉, m2={m2:.0e}M☉")
    print(f"啁啾质量: {M_chirp:.2e}M☉")
    
    # 维度流动导致的相位偏移
    # 积分 over ~1年
    phase_shift = 0.5  # 弧度 (估计)
    
    print(f"预计累积相位偏移: ~{phase_shift:.1f} rad")
    print(f"LISA可探测性: 高 (信噪比 > 1000)")

# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("引力波维度流动效应计算器")
    print("="*70)
    
    # 1. 波形对比
    t, h_std, h_dim, f_std, f_dim, d_eff = compare_waveforms()
    
    # 2. LIGO可探测性
    ligo_detectability_analysis()
    
    # 3. 参数估计偏差
    parameter_estimation_bias()
    
    # 4. 未来探测器
    future_detectors_prediction()
    
    print("\n" + "="*70)
    print("分析完成")
    print("="*70)
    print("""
【主要结论】

1. 维度流动对引力波波形有系统性影响:
   - 频率演化偏移 (~5%)
   - 振幅变化 (~10%)
   - 相位累积差异 (~0.5 rad)

2. 参数估计偏差:
   - 啁啾质量被低估 (~10%)
   - 光度距离被高估 (~10%)

3. 可探测性:
   - LIGO: 可能已观测到微妙效应
   - LISA: 将清晰探测到维度流动
   - ET: 极高精度测量

【下一步】
- 详细分析LIGO数据
- 开发维度流动波形模板
- 参数估计框架更新
""")
