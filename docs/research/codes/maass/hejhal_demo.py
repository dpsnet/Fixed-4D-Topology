#!/usr/bin/env python3
"""
Hejhal算法演示版本 - 概念验证

这个版本使用更少的点和较低精度，但能够演示算法工作原理。
"""

import numpy as np
from scipy.linalg import svdvals
import mpmath
mpmath.mp.dps = 15  # 降低精度以提高速度


# 已知特征值
KNOWN_EVEN_R = 13.779751351890
KNOWN_ODD_R = 9.533695261349


def k_bessel(t, x):
    """计算 K_{it}(x)"""
    if x <= 0:
        return 0.0
    try:
        val = mpmath.besselk(1j * t, x)
        return float(val.real)
    except:
        return 0.0


def build_simple_matrix(t, M=8, parity='even'):
    """
    构建简化的配点矩阵
    
    参数:
        t: 谱参数
        M: 矩阵大小
        parity: 'even' 或 'odd'
    """
    A = np.zeros((M, M))
    
    # 简单的配点选择
    for j in range(M):
        y = 0.9 + 0.3 * j / M
        x = -0.4 + 0.8 * j / M
        
        for n in range(1, M + 1):
            # 原始点
            arg1 = 2 * np.pi * n * y
            k1 = k_bessel(t, arg1)
            b1 = np.sqrt(y) * k1
            
            if parity == 'even':
                term1 = b1 * np.cos(2 * np.pi * n * x)
            else:
                term1 = b1 * np.sin(2 * np.pi * n * x)
            
            # 变换点
            denom = x*x + y*y
            if denom > 1e-10:
                x_s = -x / denom
                y_s = y / denom
                
                arg2 = 2 * np.pi * n * y_s
                k2 = k_bessel(t, arg2)
                b2 = np.sqrt(y_s) * k2
                
                if parity == 'even':
                    term2 = b2 * np.cos(2 * np.pi * n * x_s)
                else:
                    term2 = b2 * np.sin(2 * np.pi * n * x_s)
                
                A[j, n-1] = term1 - term2
            else:
                A[j, n-1] = term1
    
    return A


def find_eigenvalue_simple(t_center, half_width=0.3, M=8, parity='even'):
    """简化的特征值搜索"""
    t_vals = np.linspace(t_center - half_width, t_center + half_width, 30)
    ratios = []
    
    for t in t_vals:
        A = build_simple_matrix(t, M, parity)
        try:
            s = svdvals(A)
            if s[0] > 0:
                ratios.append(s[-1] / s[0])
            else:
                ratios.append(1.0)
        except:
            ratios.append(1.0)
    
    ratios = np.array(ratios)
    min_idx = np.argmin(ratios)
    
    return t_vals[min_idx], ratios[min_idx]


def main():
    print("=" * 70)
    print("Hejhal算法演示 - Maass形式特征值计算")
    print("=" * 70)
    print("\n这是一个概念验证实现，展示Hejhal算法的基本原理")
    print("完整版本需要更高精度和更多计算时间\n")
    
    # 测试第一个偶形式
    print("【测试】第一个偶形式 (文献值 R ≈ 13.78)")
    print("-" * 70)
    
    t, ratio = find_eigenvalue_simple(13.8, half_width=0.5, M=8, parity='even')
    error = abs(t - KNOWN_EVEN_R)
    
    print(f"找到: R = {t:.6f}")
    print(f"文献值: R = {KNOWN_EVEN_R:.6f}")
    print(f"误差: {error:.4f}")
    print(f"条件数比值: {ratio:.4f}")
    
    # 测试第一个奇形式
    print("\n【测试】第一个奇形式 (文献值 R ≈ 9.53)")
    print("-" * 70)
    
    t, ratio = find_eigenvalue_simple(9.5, half_width=0.5, M=8, parity='odd')
    error = abs(t - KNOWN_ODD_R)
    
    print(f"找到: R = {t:.6f}")
    print(f"文献值: R = {KNOWN_ODD_R:.6f}")
    print(f"误差: {error:.4f}")
    print(f"条件数比值: {ratio:.4f}")
    
    print("\n" + "=" * 70)
    print("说明:")
    print("  - 本演示使用了简化的配点选择和较低精度")
    print("  - 完整实现需要 M=20-30 和 mpmath dps=30")
    print("  - 精度随 M 增加而提高，具有指数收敛性")
    print("=" * 70)


if __name__ == '__main__':
    main()
