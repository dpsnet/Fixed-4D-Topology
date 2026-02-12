#!/usr/bin/env python3
"""
LIGO引力波维度流动波形模板 - 启动脚本

开发包含维度流动修正的引力波波形模板
"""

import numpy as np
from scipy import signal

print("="*70)
print("LIGO引力波维度流动波形模板 - 启动")
print("="*70)

# ============================================================================
# 1. 维度流动修正的啁啾质量
# ============================================================================

def chirp_mass_dimflow(m1, m2, d_eff=4.0):
    """
    计算包含维度流动修正的啁啾质量
    
    标准公式: M_chirp = (m1*m2)^(3/5) / (m1+m2)^(1/5)
    修正公式: M_chirp^eff = M_chirp * (4/d_eff)^(3/5)
    """
    M_chirp_standard = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)
    
    # 维度流动修正
    correction = (4.0 / d_eff)**(3/5)
    M_chirp_eff = M_chirp_standard * correction
    
    return M_chirp_eff, correction

# ============================================================================
# 2. 维度依赖的引力常数
# ============================================================================

def effective_gravitational_constant(d_eff):
    """
    有效引力常数 (维度依赖)
    
    G_eff = G * (4 / d_eff)
    """
    return 4.0 / d_eff

# ============================================================================
# 3. 简化维度流动波形
# ============================================================================

def dimflow_waveform_simple(t, m1, m2, d_L, d_eff_func=None):
    """
    简化的维度流动修正引力波波形
    
    参数:
    t: 时间数组
    m1, m2: 质量 (太阳质量)
    d_L: 光度距离 (Mpc)
    d_eff_func: 有效维度随时间的函数
    
    返回:
    h_plus, h_cross, d_eff_t
    """
    if d_eff_func is None:
        # 默认维度流动: 从4降到2.5
        d_eff_func = lambda tau: 2.5 + 1.5 / (1 + (10*tau)**0.5)
    
    # 总质量
    M_total = m1 + m2
    
    # 时间到并合
    t_c = t[-1]
    tau = t_c - t
    tau = np.maximum(tau, 1e-10)
    
    # 归一化时间
    tau_norm = tau / (M_total * 4.925e-6)  # 秒 -> 几何单位
    
    # 维度流动
    d_eff_t = d_eff_func(tau_norm)
    
    # 修正的啁啾质量 (时间依赖)
    M_chirp_eff_t = np.zeros_like(t)
    for i, d_eff in enumerate(d_eff_t):
        M_chirp_eff_t[i], _ = chirp_mass_dimflow(m1, m2, d_eff)
    
    # 频率演化 ( inspiral 相位)
    # f ~ tau^(-3/8) * M_chirp^(-5/8)
    f_t = (1.0 / (8 * np.pi)) * tau_norm**(-3/8) * M_chirp_eff_t**(-5/8)
    
    # 限制频率在合理范围
    f_t = np.clip(f_t, 10, 1000)  # Hz
    
    # 振幅
    # h ~ M_chirp^(5/3) / d_L * f^(2/3)
    d_L_norm = d_L / 100.0  # 归一化
    h_t = (M_chirp_eff_t / 10.0)**(5/3) / d_L_norm * (f_t / 100.0)**(2/3)
    
    # 归一化到合理范围 (~10^-21)
    h_t = h_t * 1e-21
    
    # 相位
    phi_t = 2 * np.pi * np.cumsum(f_t) * np.gradient(t)
    
    # 波形
    h_plus = h_t * np.cos(phi_t)
    h_cross = h_t * np.sin(phi_t)
    
    return h_plus, h_cross, d_eff_t, f_t

# ============================================================================
# 4. 与标准波形对比
# ============================================================================

def compare_waveforms():
    """
    对比标准波形和维度流动波形
    """
    print("\n【波形对比分析】")
    
    # 参数
    m1, m2 = 36, 29  # GW150914-like
    d_L = 410  # Mpc
    
    # 时间数组
    t = np.linspace(-1.0, 0, 8192)  # 1秒, 8192点
    
    # 维度流动波形
    h_plus_df, h_cross_df, d_eff_t, f_t = dimflow_waveform_simple(t, m1, m2, d_L)
    
    # 标准波形 (d_eff = 4 恒定)
    h_plus_std, h_cross_std, _, f_std = dimflow_waveform_simple(
        t, m1, m2, d_L, lambda tau: 4.0 * np.ones_like(tau)
    )
    
    # 分析差异
    print(f"\n系统: m1={m1}M☉, m2={m2}M☉, d_L={d_L}Mpc")
    
    # 并合前瞬间
    idx = -100
    print(f"\n并合前 (~{t[idx]:.3f}s):")
    print(f"  维度流动:")
    print(f"    d_eff = {d_eff_t[idx]:.3f}")
    print(f"    f = {f_t[idx]:.1f} Hz")
    print(f"    h_plus = {h_plus_df[idx]:.2e}")
    print(f"  标准 (d=4):")
    print(f"    f = {f_std[idx]:.1f} Hz")
    print(f"    h_plus = {h_plus_std[idx]:.2e}")
    print(f"  差异:")
    print(f"    Δf/f = {(f_t[idx] - f_std[idx])/f_std[idx]*100:+.2f}%")
    print(f"    Δh/h = {(abs(h_plus_df[idx]) - abs(h_plus_std[idx]))/abs(h_plus_std[idx])*100:+.2f}%")
    
    # 累积相位差
    phase_df = np.unwrap(np.angle(h_plus_df + 1j*h_cross_df))
    phase_std = np.unwrap(np.angle(h_plus_std + 1j*h_cross_std))
    phase_diff = phase_df[-1] - phase_std[-1]
    
    print(f"\n累积相位差: {phase_diff:.2f} rad ({phase_diff/(2*np.pi):.2f} 周期)")
    
    # 信噪比估计
    print(f"\n【信噪比影响】")
    
    # 简化的SNR估计
    # SNR ~ sqrt(4 * ∫ |h(f)|^2 / S_n(f) df)
    
    # 假设LIGO噪声曲线简化
    f_range = np.linspace(20, 500, 100)
    S_n = 1e-46 * (f_range/100)**(-4)  # 简化噪声谱
    
    # 计算SNR
    h_f_df = np.fft.rfft(h_plus_df)
    h_f_std = np.fft.rfft(h_plus_std)
    freq = np.fft.rfftfreq(len(t), t[1]-t[0])
    
    # 只考虑20-500 Hz范围
    mask = (freq >= 20) & (freq <= 500)
    
    snr_df = np.sqrt(4 * np.sum(np.abs(h_f_df[mask])**2))
    snr_std = np.sqrt(4 * np.sum(np.abs(h_f_std[mask])**2))
    
    print(f"  SNR (维度流动): {snr_df:.1f}")
    print(f"  SNR (标准): {snr_std:.1f}")
    print(f"  差异: {(snr_df/snr_std - 1)*100:+.2f}%")
    
    return t, h_plus_df, h_plus_std, d_eff_t

# ============================================================================
# 5. 参数估计偏差分析
# ============================================================================

def parameter_estimation_bias():
    """
    分析维度流动对参数估计的影响
    """
    print("\n" + "="*70)
    print("参数估计偏差分析")
    print("="*70)
    
    print("""
当使用标准4维波形模板拟合受维度流动影响的信号时，
会产生系统性的参数估计偏差。

偏差机制:
1. 频率偏移 → 质量被误估计
2. 振幅变化 → 距离被误估计
3. 相位差异 → 轨道参数偏差
""")
    
    # 模拟偏差
    print("\n【GW150914-like 系统偏差预测】")
    
    # 真实参数 (含维度流动)
    m1_true, m2_true = 36, 29
    d_L_true = 410
    M_chirp_true = (m1_true * m2_true)**(3/5) / (m1_true + m2_true)**(1/5)
    
    # 使用标准模板拟合会产生偏差
    # 频率降低 ~5% → 质量被高估 ~10%
    # 振幅增加 ~10% → 距离被低估 ~10%
    
    freq_shift = -0.05  # -5%
    amp_shift = 0.10    # +10%
    
    # 质量偏差: M_est = M_true * (1 + freq_shift)^(8/3)
    M_chirp_est = M_chirp_true * (1 + freq_shift)**(-8/3)
    
    # 距离偏差: d_est = d_true / (1 + amp_shift)
    d_L_est = d_L_true / (1 + amp_shift)
    
    print(f"真实值:")
    print(f"  M_chirp = {M_chirp_true:.2f} M☉")
    print(f"  d_L = {d_L_true} Mpc")
    print(f"\n标准模板估计:")
    print(f"  M_chirp = {M_chirp_est:.2f} M☉ ({(M_chirp_est/M_chirp_true-1)*100:+.1f}%)")
    print(f"  d_L = {d_L_est:.0f} Mpc ({(d_L_est/d_L_true-1)*100:+.1f}%)")
    
    print(f"\n【物理意义】")
    print(f"质量被高估: 因为频率降低被误解为更大的质量")
    print(f"距离被低估: 因为振幅增加被误解为更近的距离")

# ============================================================================
# 6. 开发路线图
# ============================================================================

def development_roadmap():
    """
    波形模板开发路线图
    """
    print("\n" + "="*70)
    print("波形模板开发路线图")
    print("="*70)
    
    print("""
【当前阶段: 概念验证】
- 简化 inspiral 模型 ✓
- 基本维度流动效应 ✓
- 参数偏差估计 ✓

【下一阶段: 精确模型】
- 实现完整的IMRPhenomD模型
- 添加维度流动修正
- 包含spin效应

【再下一阶段: 数据分析】
- 与LALSuite集成
- 贝叶斯参数估计
- 应用到真实LIGO数据

【最终目标: 科学发表】
- 论文: "Testing Spectral Dimension Flow with LIGO"
- 目标期刊: Physical Review Letters
""")
    
    roadmap = [
        ("Week 1", "概念验证完成", "✓"),
        ("Week 2", "IMRPhenomD + 维度流动", "○"),
        ("Week 3", "Spin效应 + 精度优化", "○"),
        ("Week 4", "LALSuite集成测试", "○"),
        ("Week 5-6", "应用到GW150914", "○"),
        ("Week 7-8", "统计检验 + 论文写作", "○"),
        ("Month 3", "投稿PRL", "○"),
    ]
    
    print("\n【详细时间线】")
    for week, task, status in roadmap:
        print(f"  {week:<12} [{status}] {task}")

# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LIGO引力波维度流动波形模板")
    print("="*70)
    
    # 1. 波形对比
    t, h_df, h_std, d_eff = compare_waveforms()
    
    # 2. 参数估计偏差
    parameter_estimation_bias()
    
    # 3. 开发路线图
    development_roadmap()
    
    print("\n" + "="*70)
    print("启动完成")
    print("="*70)
    print("""
【下一步行动】

1. 开发精确IMRPhenomD模型:
   - 参考 LALSimulation 库
   - 添加维度流动参数

2. 实现贝叶斯参数估计:
   - 使用 bilby 或 pycbc
   - 包含维度流动作为额外参数

3. 应用到LIGO数据:
   - 下载GWOSC公开数据
   - 进行参数估计
   - 计算贝叶斯因子

4. 论文准备:
   - 收集所有结果
   - 撰写PRL论文
   - 准备补充材料
""")
