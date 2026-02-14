"""
简化跨维度测试
使用简单但有效的方法验证 c1 = 1/d
"""

import numpy as np
from fractal_laplacian import FractalLaplacian


def generate_simple_fractal(dimension: int, n_points: int = 500) -> np.ndarray:
    """
    生成简单的分形结构
    
    策略: 生成在不同尺度有不同有效维度的点
    """
    points = []
    
    # 三个尺度区域
    scales = [
        (10.0, dimension),      # 大尺度: 全维度
        (1.0, dimension - 0.5),  # 中尺度: 略低
        (0.1, 2.0),             # 小尺度: 2维
    ]
    
    for scale, d_eff in scales:
        n_scale = n_points // 3
        
        # 活跃维度数
        n_active = max(2, int(d_eff))
        
        for _ in range(n_scale):
            # 基础位置
            point = np.random.randn(dimension) * scale
            
            # 压缩非活跃维度
            if n_active < dimension:
                inactive = np.random.choice(dimension, dimension - n_active, replace=False)
                point[inactive] *= 0.1
            
            points.append(point)
    
    return np.array(points)


def quick_c1_extraction(points: np.ndarray) -> float:
    """
    快速提取c1
    """
    try:
        fl = FractalLaplacian(dimension=points.shape[1])
        L = fl.construct_graph_laplacian(points, epsilon=None)
        
        t_vals, d_s = fl.compute_spectral_dimension(
            L, 
            t_range=np.logspace(-1, 1, 40),
            n_eigenvalues=30
        )
        
        # 简单提取
        ell_vals = np.sqrt(t_vals)
        log_ell = np.log(ell_vals)
        
        # 选择有效区域
        valid = (np.abs(log_ell) > 0.1) & (d_s > 1.5) & (d_s < points.shape[1] + 0.5)
        
        if np.sum(valid) < 5:
            return np.nan
        
        x = 1.0 / log_ell[valid]
        y = d_s[valid]
        
        # 线性拟合 y = a - c1 * x
        A = np.vstack([x, np.ones(len(x))]).T
        c1, _ = np.linalg.lstsq(A, y, rcond=None)[0]
        c1 = -c1
        
        return c1 if 0 < c1 < 2 else np.nan
        
    except:
        return np.nan


print("=" * 70)
print("简化跨维度验证 - c1 = 1/d")
print("=" * 70)

dimensions = [3, 4, 5]
n_samples = 10

results = {}

for dim in dimensions:
    print(f"\n{'='*70}")
    print(f"{dim}维空间 - 理论c1 = 1/{dim} = {1.0/dim:.4f}")
    print(f"{'='*70}")
    
    c1_values = []
    
    for i in range(n_samples):
        np.random.seed(i * 10 + dim)
        points = generate_simple_fractal(dim, n_points=400)
        c1 = quick_c1_extraction(points)
        
        if not np.isnan(c1):
            c1_values.append(c1)
            print(f"  样本{i+1}: c1 = {c1:.4f}")
    
    if c1_values:
        c1_values = np.array(c1_values)
        mean_c1 = np.mean(c1_values)
        theory = 1.0 / dim
        bias = abs(mean_c1 - theory) / theory * 100
        
        results[dim] = {
            'theory': theory,
            'extracted': mean_c1,
            'bias_percent': bias,
            'n_valid': len(c1_values)
        }
        
        print(f"\n  统计:")
        print(f"    理论值: {theory:.4f}")
        print(f"    提取均值: {mean_c1:.4f}")
        print(f"    标准差: {np.std(c1_values):.4f}")
        print(f"    偏差: {bias:.1f}%")
    else:
        print(f"\n  ❌ 没有有效结果")

# 汇总
print("\n" + "=" * 70)
print("📋 跨维度汇总")
print("=" * 70)

if results:
    print(f"\n{'维度':>6} | {'理论c1':>10} | {'提取c1':>10} | {'偏差%':>8}")
    print(f"{'-'*6}-+-{'-'*10}-+-{'-'*10}-+-{'-'*8}")
    
    for dim, res in sorted(results.items()):
        print(f"{dim:>6} | {res['theory']:>10.4f} | {res['extracted']:>10.4f} | "
              f"{res['bias_percent']:>8.1f}")
    
    # 验证线性关系
    if len(results) >= 2:
        dims = np.array([d for d in results.keys()])
        c1_extracted = np.array([results[d]['extracted'] for d in dims])
        inv_dims = 1.0 / dims
        
        # 拟合 c1 = k / d
        k = np.sum(c1_extracted * inv_dims) / np.sum(inv_dims ** 2)
        
        print(f"\n📈 线性关系: c1 = k / d")
        print(f"  拟合k = {k:.4f} (理论 = 1.0)")
        print(f"  偏差: {abs(k - 1.0) * 100:.1f}%")
        
        if abs(k - 1.0) < 0.2:
            print(f"\n  ✅ 支持 c1 = 1/d 猜想!")
        else:
            print(f"\n  ⚠️ 需要更多数据验证")

print("\n" + "=" * 70)
