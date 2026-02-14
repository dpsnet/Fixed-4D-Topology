"""
分析c1提取过程
深入理解为什么提取的c1与理论值0.25有偏差
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
from spectral_flow_fractal import SpectralFlowFractal
from fractal_laplacian import FractalLaplacian


def analyze_extraction_process():
    """详细分析c1提取过程"""
    print("=" * 70)
    print("c1提取过程分析")
    print("=" * 70)
    
    sff = SpectralFlowFractal(dimension=4, c1=0.25)
    
    # 1. 检查理论的谱维度曲线
    print("\n[1] 理论谱维度曲线")
    print("-" * 70)
    
    ell_range = np.logspace(-2, 1, 100)
    d_s_theory = sff.spectral_dimension(ell_range, ell_0=1.0)
    
    print(f"理论c1 = 0.25")
    print(f"d_s(ℓ) = 4 - 0.25/ln(ℓ/ℓ_0)")
    print(f"")
    print(f"关键点:")
    for ell in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        d_s = 4.0 - 0.25 / np.log(ell) if ell != 1.0 else 2.0
        print(f"  ℓ = {ell:6.2f}: d_s = {d_s:.3f}")
    
    # 2. 生成一个大的分层分形样本
    print("\n[2] 生成分层分形样本")
    print("-" * 70)
    
    np.random.seed(42)
    points, ell_vals, d_s_target = sff.generate_layered_fractal(
        n_points=800,
        ell_range=(0.01, 10.0),
        ell_0=1.0
    )
    
    print(f"生成点数: {len(points)}")
    print(f"目标谱维度范围: [{d_s_target.min():.2f}, {d_s_target.max():.2f}]")
    
    # 3. 计算实际谱维度
    print("\n[3] 计算实际谱维度")
    print("-" * 70)
    
    fl = FractalLaplacian(dimension=4)
    
    # 构建拉普拉斯
    L = fl.construct_graph_laplacian(points, epsilon=None)
    print(f"拉普拉斯矩阵: {L.shape}")
    
    # 计算谱维度
    t_vals, d_s_computed = fl.compute_spectral_dimension(
        L, 
        t_range=np.logspace(-1, 1, 50),
        n_eigenvalues=80
    )
    
    print(f"计算的谱维度范围: [{d_s_computed.min():.2f}, {d_s_computed.max():.2f}]")
    print(f"时间尺度范围: [{t_vals.min():.4f}, {t_vals.max():.4f}]")
    
    # 4. 分析提取过程
    print("\n[4] 分析c1提取过程")
    print("-" * 70)
    
    # 长度尺度
    ell_vals = np.sqrt(t_vals)
    log_ell = np.log(ell_vals)
    
    # 选择有效区域
    valid_mask = (np.abs(log_ell) > 0.1) & (d_s_computed > 1.5) & (d_s_computed < 4.5)
    
    print(f"有效数据点: {np.sum(valid_mask)} / {len(log_ell)}")
    
    if np.sum(valid_mask) > 5:
        x = 1.0 / log_ell[valid_mask]
        y = d_s_computed[valid_mask]
        
        # 线性拟合
        A = np.vstack([x, np.ones(len(x))]).T
        c1_fit, d_max_fit = np.linalg.lstsq(A, y, rcond=None)[0]
        c1_fit = -c1_fit
        
        # 计算R^2
        y_pred = d_max_fit - c1_fit * x
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        print(f"")
        print(f"拟合结果:")
        print(f"  提取的c1: {c1_fit:.6f}")
        print(f"  提取的d_max: {d_max_fit:.2f}")
        print(f"  R^2: {r_squared:.4f}")
        print(f"  与理论偏差: {abs(c1_fit - 0.25):.6f}")
    
    # 5. 问题诊断
    print("\n[5] 问题诊断")
    print("-" * 70)
    
    print(f"")
    print(f"可能的误差来源:")
    print(f"  1. 有限样本效应: 点数{len(points)}可能不足以展现完整谱流")
    print(f"  2. 特征值截断: 只计算了部分特征值")
    print(f"  3. 数值噪声: 小t值区域数值不稳定")
    print(f"  4. 分形结构: 生成的分形可能不完全匹配理论谱流")
    
    # 检查不同区域的拟合
    print(f"")
    print(f"分区域分析:")
    
    # 大尺度区域 (d_s ≈ 4)
    large_mask = (d_s_computed > 3.5) & valid_mask
    if np.sum(large_mask) > 3:
        x_large = 1.0 / log_ell[large_mask]
        y_large = d_s_computed[large_mask]
        A_large = np.vstack([x_large, np.ones(len(x_large))]).T
        c1_large, _ = np.linalg.lstsq(A_large, y_large, rcond=None)[0]
        c1_large = -c1_large
        print(f"  大尺度 (d_s > 3.5): c1 ≈ {c1_large:.4f}")
    
    # 过渡区域 (d_s ≈ 3)
    trans_mask = (d_s_computed > 2.5) & (d_s_computed <= 3.5) & valid_mask
    if np.sum(trans_mask) > 3:
        x_trans = 1.0 / log_ell[trans_mask]
        y_trans = d_s_computed[trans_mask]
        A_trans = np.vstack([x_trans, np.ones(len(x_trans))]).T
        c1_trans, _ = np.linalg.lstsq(A_trans, y_trans, rcond=None)[0]
        c1_trans = -c1_trans
        print(f"  过渡区 (2.5 < d_s ≤ 3.5): c1 ≈ {c1_trans:.4f}")
    
    # 小尺度区域 (d_s ≈ 2)
    small_mask = (d_s_computed <= 2.5) & valid_mask
    if np.sum(small_mask) > 3:
        x_small = 1.0 / log_ell[small_mask]
        y_small = d_s_computed[small_mask]
        A_small = np.vstack([x_small, np.ones(len(x_small))]).T
        c1_small, _ = np.linalg.lstsq(A_small, y_small, rcond=None)[0]
        c1_small = -c1_small
        print(f"  小尺度 (d_s ≤ 2.5): c1 ≈ {c1_small:.4f}")
    
    # 6. 建议改进
    print("\n[6] 改进建议")
    print("-" * 70)
    
    print(f"")
    print(f"为提高c1提取精度，建议:")
    print(f"  1. 增加样本点数到2000+")
    print(f"  2. 使用更宽的尺度范围 (ℓ: 0.001 - 100)")
    print(f"  3. 改进分形生成，确保清晰的4→2维度过渡")
    print(f"  4. 使用加权拟合，重视过渡区域数据")
    print(f"  5. 考虑使用多个独立分形样本的平均")
    
    print("\n" + "=" * 70)
    
    return {
        'c1_extracted': c1_fit if 'c1_fit' in locals() else None,
        'd_max_extracted': d_max_fit if 'd_max_fit' in locals() else None,
        'r_squared': r_squared if 'r_squared' in locals() else None,
        'points': points,
        't_vals': t_vals,
        'd_s_computed': d_s_computed
    }


if __name__ == "__main__":
    results = analyze_extraction_process()
