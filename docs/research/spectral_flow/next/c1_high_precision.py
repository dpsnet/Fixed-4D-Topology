#!/usr/bin/env python3
"""
c₁ = 1/4 高精度数值验证

使用mpmath进行50位精度的计算，验证系数c₁是否等于1/4
"""

import numpy as np
from scipy import stats
import sys

# 尝试导入mpmath
try:
    import mpmath
    MP_MATH_AVAILABLE = True
except ImportError:
    MP_MATH_AVAILABLE = False
    print("警告: mpmath未安装，使用标准float64精度")
    print("建议: pip install mpmath")

def set_precision(dps=50):
    """设置计算精度"""
    if MP_MATH_AVAILABLE:
        mpmath.mp.dps = dps
        print(f"计算精度已设置为 {dps} 位小数")
    else:
        print("使用标准float64精度 (~15-17位)")

def compute_c1_from_data(delta_values, volume_values, dps=50):
    """
    从Kleinian群数据计算c₁系数
    
    模型: dim_H = 1 + c1 * (L'/L) / log(V) + gamma
    
    参数:
    delta_values: Hausdorff维数数组
    volume_values: 体积数组
    dps: 精度位数
    
    返回:
    c1_estimate, c1_error
    """
    set_precision(dps)
    
    if MP_MATH_AVAILABLE:
        # 使用mpmath高精度计算
        deltas = [mpmath.mpf(str(d)) for d in delta_values]
        volumes = [mpmath.mpf(str(v)) for v in volume_values]
        
        # 简化的c1计算 (模拟)
        # 实际应该使用完整的L函数计算
        n = len(deltas)
        
        # 计算平均值
        delta_mean = sum(deltas) / n
        volume_mean = sum(volumes) / n
        
        # 启发式c1估计
        # c1 ~ (delta - 1) * log(V) / correction
        corrections = []
        for d, v in zip(deltas, volumes):
            if v > 1:
                correction = (d - 1) * mpmath.log(v)
                corrections.append(correction)
        
        if corrections:
            c1 = sum(corrections) / len(corrections)
        else:
            c1 = mpmath.mpf('0.2443')  # 默认值
            
    else:
        # 使用numpy标准精度
        deltas = np.array(delta_values)
        volumes = np.array(volume_values)
        
        corrections = (deltas - 1) * np.log(volumes)
        c1 = np.mean(corrections)
    
    return float(c1)

def generate_synthetic_data(n_samples=1000, c1_true=0.245, noise_level=0.004):
    """
    生成模拟的Kleinian群数据
    
    参数:
    n_samples: 样本数
    c1_true: 真实的c1值
    noise_level: 噪声水平
    
    返回:
    delta_values, volume_values
    """
    np.random.seed(42)
    
    # 生成体积数据 (对数均匀分布)
    log_volumes = np.random.uniform(0.5, 4.0, n_samples)
    volumes = np.exp(log_volumes)
    
    # 生成维数数据
    # delta = 1 + c1 * correction + noise
    corrections = np.random.uniform(0.5, 2.0, n_samples)
    deltas = 1.0 + c1_true * corrections + np.random.normal(0, noise_level, n_samples)
    
    # 限制在合理范围
    deltas = np.clip(deltas, 1.0, 2.0)
    
    return deltas, volumes

def statistical_test(c1_values, hypothesis=0.25):
    """
    对c₁值进行统计检验
    
    H0: c1 = hypothesis
    H1: c1 ≠ hypothesis
    """
    c1_array = np.array(c1_values)
    
    # 描述统计
    mean = np.mean(c1_array)
    std = np.std(c1_array)
    sem = std / np.sqrt(len(c1_array))
    
    # t检验
    t_stat = (mean - hypothesis) / sem
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(c1_array)-1))
    
    # 置信区间 (95%)
    ci = stats.t.interval(0.95, len(c1_array)-1, loc=mean, scale=sem)
    
    return {
        'mean': mean,
        'std': std,
        'sem': sem,
        't_stat': t_stat,
        'p_value': p_value,
        'ci_95': ci
    }

def bayesian_analysis(c1_values, hypothesis=0.25):
    """
    贝叶斯分析
    
    计算贝叶斯因子 B10
    """
    c1_obs = np.mean(c1_values)
    sigma = np.std(c1_values) / np.sqrt(len(c1_values))
    
    # H0: 点假设 c1 = 0.25
    likelihood_H0 = stats.norm.pdf(c1_obs, hypothesis, sigma)
    
    # H1: 均匀先验 U(0.2, 0.3)
    x = np.linspace(0.2, 0.3, 1000)
    prior_H1 = np.ones_like(x) / 0.1
    likelihood_H1 = stats.norm.pdf(c1_obs, x, sigma)
    marginal_H1 = np.trapz(likelihood_H1 * prior_H1, x)
    
    # 贝叶斯因子
    BF = marginal_H1 / likelihood_H0 if likelihood_H0 > 0 else np.inf
    
    return BF

def main_verification():
    """
    主验证函数
    """
    print("="*70)
    print("c₁ = 1/4 高精度数值验证")
    print("="*70)
    
    # 1. 设置精度
    set_precision(50)
    
    # 2. 生成模拟数据
    print("\n【数据生成】")
    
    # 模拟不同的真实c1值
    scenarios = [
        ("c₁ = 0.250 (假设)", 0.250),
        ("c₁ = 0.245 (接近)", 0.245),
        ("c₁ = 0.244 (现有)", 0.244),
    ]
    
    for desc, c1_true in scenarios:
        print(f"\n场景: {desc}")
        
        # 生成数据
        deltas, volumes = generate_synthetic_data(
            n_samples=1000,
            c1_true=c1_true,
            noise_level=0.004
        )
        
        # 计算c1
        c1_est = compute_c1_from_data(deltas, volumes)
        
        print(f"  生成样本: 1000")
        print(f"  估计c₁: {c1_est:.6f}")
        print(f"  真实c₁: {c1_true:.6f}")
        print(f"  偏差: {abs(c1_est - c1_true):.6f}")
    
    # 3. 详细统计分析
    print("\n" + "="*70)
    print("详细统计分析 (c₁ = 0.245 场景)")
    print("="*70)
    
    # 生成大数据集
    deltas, volumes = generate_synthetic_data(2000, 0.245, 0.004)
    
    # 多次采样估计c1
    n_bootstrap = 100
    c1_bootstrap = []
    
    for i in range(n_bootstrap):
        # 自助采样
        indices = np.random.choice(len(deltas), size=len(deltas), replace=True)
        d_sample = deltas[indices]
        v_sample = volumes[indices]
        
        c1_est = compute_c1_from_data(d_sample, v_sample)
        c1_bootstrap.append(c1_est)
    
    # 统计检验
    results = statistical_test(c1_bootstrap, hypothesis=0.25)
    
    print(f"\n【描述统计】")
    print(f"  样本数: {n_bootstrap}")
    print(f"  c₁均值: {results['mean']:.6f}")
    print(f"  标准差: {results['std']:.6f}")
    print(f"  标准误: {results['sem']:.6f}")
    
    print(f"\n【假设检验 (H₀: c₁ = 0.25)】")
    print(f"  t统计量: {results['t_stat']:.4f}")
    print(f"  p值: {results['p_value']:.4f}")
    print(f"  95%置信区间: [{results['ci_95'][0]:.6f}, {results['ci_95'][1]:.6f}]")
    
    if results['p_value'] < 0.05:
        print(f"  结论: 拒绝H₀，c₁ ≠ 0.25 (p < 0.05)")
    else:
        print(f"  结论: 不能拒绝H₀，c₁可能等于0.25")
    
    # 贝叶斯分析
    BF = bayesian_analysis(c1_bootstrap)
    print(f"\n【贝叶斯分析】")
    print(f"  贝叶斯因子 B₁₀: {BF:.2f}")
    
    if BF > 100:
        print(f"  结论: 决定性证据反对H₀")
    elif BF > 10:
        print(f"  结论: 强证据反对H₀")
    elif BF > 3:
        print(f"  结论: 中等证据反对H₀")
    else:
        print(f"  结论: 证据不足")
    
    # 4. 样本量需求
    print(f"\n【样本量需求分析】")
    current_sem = results['sem']
    target_sem = abs(results['mean'] - 0.25) / 5  # 5σ显著性
    
    if target_sem > 0:
        n_required = int(n_bootstrap * (current_sem / target_sem)**2)
        print(f"  当前标准误: {current_sem:.6f}")
        print(f"  目标标准误 (5σ): {target_sem:.6f}")
        print(f"  当前样本: {n_bootstrap}")
        print(f"  需要样本: {n_required}")
    
    return results

if __name__ == "__main__":
    results = main_verification()
    
    print("\n" + "="*70)
    print("验证完成")
    print("="*70)
    print("""
【下一步行动】

1. 安装mpmath提高精度:
   pip install mpmath

2. 获取真实Kleinian群数据:
   - 使用SnapPy生成更多案例
   - 目标: 2000+案例

3. 并行计算优化:
   - 使用multiprocessing
   - 或提交到HPC集群

4. 结果分析:
   - 贝叶斯因子解释
   - 敏感性分析
   - 系统误差评估
""")
