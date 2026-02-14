"""
调试提取过程
找出"Insufficient data points"的根本原因
"""

import numpy as np
from dimension_specific_fractal import DimensionSpecificFractalGenerator
from fractal_laplacian import FractalLaplacian


def debug_extraction(dimension: int = 4):
    """调试提取过程"""
    print("=" * 70)
    print(f"调试 {dimension} 维提取过程")
    print("=" * 70)
    
    # 生成分形
    gen = DimensionSpecificFractalGenerator(dimension=dimension)
    np.random.seed(42)
    points = gen.generate_dimension_optimized(n_points=400)
    
    print(f"\n1. 生成的点:")
    print(f"   点数: {len(points)}")
    print(f"   维度: {points.shape[1]}")
    print(f"   范围: [{points.min():.3f}, {points.max():.3f}]")
    
    # 构建拉普拉斯
    print(f"\n2. 构建拉普拉斯...")
    fl = FractalLaplacian(dimension=dimension)
    
    from scipy.spatial.distance import pdist
    dists = pdist(points)
    mean_nn = np.mean(np.sort(dists)[:len(points)])
    epsilon = mean_nn
    
    print(f"   mean_nn: {mean_nn:.4f}")
    print(f"   epsilon: {epsilon:.4f}")
    
    L = fl.construct_graph_laplacian(points, epsilon=epsilon)
    print(f"   拉普拉斯: {L.shape}")
    
    # 计算谱维度
    print(f"\n3. 计算谱维度...")
    n_eig = max(20, int(len(points) * 0.2))
    print(f"   n_eigenvalues: {n_eig}")
    
    t_range = np.logspace(-1, 1.5, 50)
    print(f"   t_range: [{t_range.min():.4f}, {t_range.max():.4f}]")
    
    try:
        t_vals, d_s = fl.compute_spectral_dimension(
            L, 
            t_range=t_range,
            n_eigenvalues=n_eig
        )
        
        print(f"   t_vals: [{t_vals.min():.4f}, {t_vals.max():.4f}]")
        print(f"   d_s: [{d_s.min():.2f}, {d_s.max():.2f}]")
        print(f"   d_s 有效值: {np.sum(~np.isnan(d_s))}/{len(d_s)}")
        
        # 转换为长度尺度
        ell_vals = np.sqrt(t_vals)
        print(f"\n4. 长度尺度:")
        print(f"   ell: [{ell_vals.min():.4f}, {ell_vals.max():.4f}]")
        
        # 过滤检查
        print(f"\n5. 过滤检查:")
        valid1 = (ell_vals > 0)
        print(f"   ell > 0: {np.sum(valid1)}/{len(ell_vals)}")
        
        valid2 = (d_s > 1) & (d_s < dimension + 1)
        print(f"   1 < d_s < {dimension+1}: {np.sum(valid2)}/{len(d_s)}")
        
        valid3 = (~np.isnan(ell_vals)) & (~np.isnan(d_s))
        print(f"   非NaN: {np.sum(valid3)}/{len(ell_vals)}")
        
        valid = valid1 & valid2 & valid3
        print(f"   全部有效: {np.sum(valid)}/{len(ell_vals)}")
        
        if np.sum(valid) > 0:
            ell = ell_vals[valid]
            d_s_valid = d_s[valid]
            
            log_ell = np.log(ell)
            print(f"\n6. 对数检查:")
            print(f"   ln(ell): [{log_ell.min():.4f}, {log_ell.max():.4f}]")
            print(f"   |ln(ell)| > 0.001: {np.sum(np.abs(log_ell) > 0.001)}")
            
            # 尝试拟合
            mask = np.abs(log_ell) > 0.001
            if np.sum(mask) >= 4:
                x = 1.0 / log_ell[mask]
                y = d_s_valid[mask]
                
                print(f"\n7. 拟合数据:")
                print(f"   x (1/ln): [{x.min():.4f}, {x.max():.4f}]")
                print(f"   y (d_s): [{y.min():.4f}, {y.max():.4f}]")
                
                A = np.vstack([x, np.ones(len(x))]).T
                c1, d_max = np.linalg.lstsq(A, y, rcond=None)[0]
                c1 = -c1
                
                print(f"\n8. 拟合结果:")
                print(f"   c1 = {c1:.4f} (理论={1.0/dimension:.4f})")
                print(f"   d_max = {d_max:.2f}")
            else:
                print(f"\n❌ 过滤后点数不足: {np.sum(mask)} < 4")
        else:
            print(f"\n❌ 没有有效数据点")
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    for dim in [3, 4, 5]:
        debug_extraction(dim)
        print("\n" + "=" * 70 + "\n")
