"""
快速c1测试
减少计算量，快速验证新方法
"""

import numpy as np
from advanced_fractal_generator import AdvancedFractalGenerator
from fractal_laplacian import FractalLaplacian


print("=" * 70)
print("快速c1测试")
print("=" * 70)

afg = AdvancedFractalGenerator(dimension=4, c1=0.25)
fl = FractalLaplacian(dimension=4)

# 测试严格谱流分形
print("\n[1] 严格谱流分形")
for n_points in [300, 500, 800]:
    print(f"\n  n_points = {n_points}")
    np.random.seed(42)
    points = afg.generate_strict_spectral_fractal(n_points, 0.001, 100.0)
    
    L = fl.construct_graph_laplacian(points, epsilon=None)
    t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=30)
    
    result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
    
    if 'c1' in result:
        print(f"    c1 = {result['c1']:.4f}, d_max = {result.get('d_max', 0):.2f}, "
              f"R^2 = {result.get('quality', 0):.3f}")
        print(f"    d_s range: [{d_s.min():.2f}, {d_s.max():.2f}]")

# 测试递归分形
print("\n[2] 递归维度过渡分形")
for n_points in [300, 500]:
    print(f"\n  n_points = {n_points}")
    np.random.seed(42)
    points = afg.generate_recursive_dimension_fractal(n_points, 5)
    
    L = fl.construct_graph_laplacian(points, epsilon=None)
    t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=30)
    
    result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
    
    if 'c1' in result:
        print(f"    c1 = {result['c1']:.4f}, d_max = {result.get('d_max', 0):.2f}, "
              f"R^2 = {result.get('quality', 0):.3f}")
        print(f"    d_s range: [{d_s.min():.2f}, {d_s.max():.2f}]")

print("\n" + "=" * 70)
