#!/usr/bin/env python3
"""
Bilby + 维度流动 使用示例

分析GW150914-like信号
"""

import numpy as np
import bilby
from bilby_dimflow_plugin import DimFlowAnalysis, dimflow_binary_black_hole

# 注入参数 (真实值)
injection_parameters = dict(
    mass_1=36.0,
    mass_2=29.0,
    a_1=0.0,
    a_2=0.0,
    tilt_1=0.0,
    tilt_2=0.0,
    phi_12=0.0,
    phi_jl=0.0,
    theta_jn=0.4,
    luminosity_distance=410.0,
    phase=0.0,
    geocent_time=1126259642.413,
    ra=1.95,
    dec=-1.27,
    psi=0.53,
    d_eff_param=3.5,  # 维度流动参数 (真实值)
)

# 波形参数
waveform_arguments = dict(
    waveform_approximant='IMRPhenomD',
    reference_frequency=50.0,
)

# 创建分析器
analysis = DimFlowAnalysis(label='GW150914_dimflow')

# 设置注入
analysis.setup_injection(injection_parameters)

# 设置先验 (包含维度流动)
priors = analysis.setup_priors(include_dimflow=True)

print("准备运行分析...")
print("注: 完整分析需要GWOSC数据和较长时间")
print("这里仅展示框架")

# 模拟结果
print("\n模拟分析结果:")
print("标准模型 vs 维度流动模型")
print("贝叶斯因子 B_21 ~ 2-5 (预期)")
print("需要真实数据验证")
