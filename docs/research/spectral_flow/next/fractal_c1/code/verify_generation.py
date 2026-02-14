"""
验证分形生成
检查生成的分形是否真的有正确的谱维度
"""

import numpy as np
from revamped_fractal_generator import RevampedFractalGenerator
from fractal_laplacian import FractalLaplacian


def verify_generation(dimension: int = 4):
    """验证分形生成"""
    print("=" * 70)
    print(f"验证 {dimension} 维分形生成")
    print("=" * 70)
    
    gen = RevampedFractalGenerator(dimension=dimension)
    
    # 生成明确过渡分形
    points, info = gen.generate_explicit_transition(n_points=600)
    
    print(f"\n生成信息:")
    print(f"  总点数: {len(points)}")
    for region in info['regions']:
        print(f"  {region['name']}: {region['n_points']}点, 目标d_s={region['mean_d_s']:.2f}")
    
    # 计算整体的谱维度
    print(f"\n计算整体谱维度...")
    fl = FractalLaplacian(dimension=dimension)
    L = fl.construct_graph_laplacian(points, epsilon=None)
    
    # 使用自动t范围
    t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=50)
    
    print(f"  t范围: [{t_vals.min():.4f}, {t_vals.max():.4f}]")
    print(f"  d_s范围: [{d_s.min():.2f}, {d_s.max():.2f}]")
    print(f"  d_s均值: {np.mean(d_s):.2f}")
    
    # 检查每个区域的贡献
    # 按径向距离分组
    print(f"\n按径向距离分析:")
    
    r = np.linalg.norm(points, axis=1)
    
    # 三个区域
    regions_r = [
        (0, 0.3, "low_dim"),
        (0.3, 3.0, "transition"),
        (3.0, 1000.0, "high_dim")
    ]
    
    for r_min, r_max, name in regions_r:
        mask = (r > r_min) & (r < r_max)
        n_in_region = np.sum(mask)
        if n_in_region > 10:
            print(f"  {name} (r={r_min}-{r_max}): {n_in_region}点, 平均r={np.mean(r[mask]):.3f}")
    
    # 关键检查: 生成的点的d_s理论值 vs 计算值
    print(f"\n理论vs实际:")
    print(f"  理论d_max: {dimension}")
    print(f"  理论d_min: 2.0")
    print(f"  计算d_s范围: [{d_s.min():.2f}, {d_s.max():.2f}]")
    
    if d_s.max() > dimension - 0.5 and d_s.min() < 2.5:
        print(f"  ✅ 覆盖理论范围")
    else:
        print(f"  ⚠️ 未覆盖理论范围")
        print(f"     需要: [{2.0}, {dimension}]")


if __name__ == "__main__":
    for dim in [3, 4, 5]:
        verify_generation(dim)
        print("\n" + "=" * 70 + "\n")
