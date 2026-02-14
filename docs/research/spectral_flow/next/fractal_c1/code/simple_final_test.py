"""
简化最终测试
使用最简单的方法验证跨维度c1提取
"""

import numpy as np
from fractal_laplacian import FractalLaplacian


def generate_simple_fractal(dimension: int, n_points: int = 500):
    """生成简单分形"""
    points = []
    
    # 三个尺度层次
    for scale, d_target in [(10.0, dimension), (1.0, (dimension + 2)/2), (0.1, 2.0)]:
        n = n_points // 3
        for _ in range(n):
            point = np.random.randn(dimension) * scale
            # 压缩到目标维度
            n_active = max(2, int(d_target))
            if n_active < dimension:
                dims = np.random.choice(dimension, dimension - n_active, replace=False)
                point[dims] *= 0.1
            points.append(point)
    
    return np.array(points)


def extract_c1_simple(points: np.ndarray, dimension: int):
    """简单提取c1"""
    try:
        fl = FractalLaplacian(dimension=dimension)
        L = fl.construct_graph_laplacian(points, epsilon=None)
        
        # 使用较宽的t范围
        t_range = np.logspace(-2, 2, 50)
        t_vals, d_s = fl.compute_spectral_dimension(L, t_range=t_range, n_eigenvalues=30)
        
        # 转换为长度尺度
        ell_vals = np.sqrt(t_vals)
        
        # 过滤
        valid = (ell_vals > 0) & (d_s > 0.1) & ~np.isnan(d_s) & ~np.isnan(ell_vals)
        
        if np.sum(valid) < 5:
            return None, f"Only {np.sum(valid)} valid points"
        
        ell = ell_vals[valid]
        d_s_valid = d_s[valid]
        
        log_ell = np.log(ell)
        mask = np.abs(log_ell) > 0.01
        
        if np.sum(mask) < 4:
            return None, f"Only {np.sum(mask)} points after log mask"
        
        x = 1.0 / log_ell[mask]
        y = d_s_valid[mask]
        
        # 线性拟合
        A = np.vstack([x, np.ones(len(x))]).T
        c1, d_max = np.linalg.lstsq(A, y, rcond=None)[0]
        c1 = -c1
        
        return {'c1': c1, 'd_max': d_max}, None
        
    except Exception as e:
        return None, str(e)


print("=" * 70)
print("简化跨维度验证")
print("=" * 70)

for dim in [3, 4, 5]:
    print(f"\n{'='*70}")
    print(f"{dim}维空间 - 理论c1 = 1/{dim} = {1.0/dim:.4f}")
    print(f"{'='*70}")
    
    c1_list = []
    
    for i in range(10):
        np.random.seed(i * 20 + dim)
        points = generate_simple_fractal(dim, n_points=500)
        
        result, error = extract_c1_simple(points, dim)
        
        if result:
            c1_list.append(result['c1'])
            theory = 1.0 / dim
            bias = abs(result['c1'] - theory) / theory * 100
            print(f"  样本{i+1}: c1 = {result['c1']:.4f}, d_max = {result['d_max']:.2f}, 偏差 = {bias:.1f}%")
        else:
            print(f"  样本{i+1}: 失败 - {error}")
    
    if c1_list:
        c1_values = np.array(c1_list)
        mean_c1 = np.mean(c1_values)
        theory = 1.0 / dim
        bias_pct = abs(mean_c1 - theory) / theory * 100
        
        print(f"\n  统计:")
        print(f"    理论值: {theory:.4f}")
        print(f"    提取均值: {mean_c1:.4f} ± {np.std(c1_values):.4f}")
        print(f"    偏差: {bias_pct:.1f}%")
        
        if bias_pct < 20:
            print(f"    ✅ 达到目标 (<20%)")
        elif bias_pct < 50:
            print(f"    🟡 接近目标")
        else:
            print(f"    ⚠️ 需要改进")

print("\n" + "=" * 70)
