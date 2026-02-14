"""
简化验证
使用经过验证的工作流程
"""

import numpy as np
from optimized_fractal_generator import OptimizedFractalGenerator
from fractal_laplacian import FractalLaplacian
from robust_c1_extractor import RobustC1Extractor


print("=" * 70)
print("简化验证 - c1 = 1/4")
print("=" * 70)

ofg = OptimizedFractalGenerator(dimension=4, c1=0.25)
fl = FractalLaplacian(dimension=4)
extractor = RobustC1Extractor(true_c1=0.25)

# 测试单个样本
print("\n测试单个样本...")

np.random.seed(42)
points = ofg.generate_dimension_cascade(n_points=600)

print(f"生成点数: {len(points)}")
print(f"坐标范围: [{points.min():.3f}, {points.max():.3f}]")

# 构建拉普拉斯
print("\n构建拉普拉斯...")
L = fl.construct_graph_laplacian(points, epsilon=None)
print(f"拉普拉斯: {L.shape}")

# 计算谱维度
print("\n计算谱维度...")
t_vals, d_s = fl.compute_spectral_dimension(
    L, 
    t_range=np.logspace(-1.5, 1.5, 60),
    n_eigenvalues=40
)

print(f"时间尺度: [{t_vals.min():.4f}, {t_vals.max():.4f}]")
print(f"谱维度: [{d_s.min():.2f}, {d_s.max():.2f}]")

# 转换为长度尺度
ell_vals = np.sqrt(t_vals)

# 提取c1 - 使用稳健提取器
print("\n提取c1...")

print("\n1. 加权拟合:")
r1 = extractor.extract_weighted_fit(ell_vals, d_s)
if 'c1' in r1:
    print(f"   c1 = {r1['c1']:.4f} ± {r1.get('c1_error', 0):.4f}")
    print(f"   d_max = {r1.get('d_max', 0):.2f}")
    print(f"   R^2 = {r1.get('quality', 0):.4f}")

print("\n2. 非线性拟合:")
r2 = extractor.extract_nonlinear_fit(ell_vals, d_s)
if 'c1' in r2:
    print(f"   c1 = {r2['c1']:.4f} ± {r2.get('c1_error', 0):.4f}")
    print(f"   d_max = {r2.get('d_max', 0):.2f}")
    print(f"   R^2 = {r2.get('quality', 0):.4f}")

print("\n3. 综合结果:")
r_combined = extractor.extract_robust(ell_vals, d_s, combine_methods=True)
if 'c1' in r_combined:
    print(f"   c1 = {r_combined['c1']:.4f}")
    print(f"   标准差: {r_combined.get('c1_std', 0):.4f}")
    print(f"   方法数: {r_combined.get('n_methods', 0)}")
    
    # 评估
    bias = abs(r_combined['c1'] - 0.25)
    print(f"\n   偏差: {bias:.4f}")
    if bias < 0.005:
        print("   ✅ 达到目标精度 (±0.005)")
    elif bias < 0.01:
        print("   🟡 接近目标精度")
    else:
        print("   ⚠️ 需要改进")

print("\n" + "=" * 70)

# 批量测试
print("\n批量测试 (10样本)...")

c1_values = []

for i in range(10):
    np.random.seed(i)
    
    points = ofg.generate_dimension_cascade(n_points=500)
    
    try:
        L = fl.construct_graph_laplacian(points, epsilon=None)
        t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=35)
        ell_vals = np.sqrt(t_vals)
        
        result = extractor.extract_weighted_fit(ell_vals, d_s)
        
        if 'c1' in result and 0 < result['c1'] < 1:
            c1_values.append(result['c1'])
            print(f"  样本{i+1}: c1 = {result['c1']:.4f}, R^2 = {result.get('quality', 0):.3f}")
    except Exception as e:
        print(f"  样本{i+1}: 失败 - {e}")

if c1_values:
    c1_values = np.array(c1_values)
    print(f"\n统计:")
    print(f"  均值: {np.mean(c1_values):.4f}")
    print(f"  中位数: {np.median(c1_values):.4f}")
    print(f"  标准差: {np.std(c1_values):.4f}")
    print(f"  偏差: {abs(np.mean(c1_values) - 0.25):.4f}")

print("\n" + "=" * 70)
