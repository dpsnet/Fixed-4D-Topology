"""
调试谱维度计算
"""

import numpy as np
from scipy.sparse.linalg import eigsh
from fractal_laplacian import FractalLaplacian
from dimension_specific_fractal import DimensionSpecificFractalGenerator


# 生成简单测试数据
print("生成测试数据...")
gen = DimensionSpecificFractalGenerator(dimension=4)
np.random.seed(42)
points = gen.generate_dimension_optimized(n_points=300)

print(f"点数: {len(points)}")
print(f"坐标范围: [{points.min():.3f}, {points.max():.3f}]")

# 构建拉普拉斯
fl = FractalLaplacian(dimension=4)
L = fl.construct_graph_laplacian(points, epsilon=None)

print(f"\n拉普拉斯矩阵: {L.shape}")
print(f"非零元素: {L.nnz}")

# 计算特征值
print("\n计算特征值...")
n_eig = 50
eigenvalues, _ = eigsh(L, k=n_eig, which='SM', return_eigenvectors=True)

print(f"特征值范围: [{eigenvalues.min():.6f}, {eigenvalues.max():.6f}]")
print(f"正特征值数量: {np.sum(eigenvalues > 1e-10)}")

# 只保留正特征值
eigenvalues = eigenvalues[eigenvalues > 1e-10]
print(f"保留后特征值数量: {len(eigenvalues)}")
print(f"保留后范围: [{eigenvalues.min():.6f}, {eigenvalues.max():.6f}]")

# 选择t范围
t_min = 1.0 / np.max(eigenvalues)
t_max = 1.0 / np.min(eigenvalues)
print(f"\nt范围: [{t_min:.6f}, {t_max:.6f}]")

t_range = np.logspace(np.log10(t_min), np.log10(t_max), 30)
print(f"t_range: [{t_range.min():.6f}, {t_range.max():.6f}]")

# 计算热核
print("\n计算热核...")
K_t = []
for t in t_range[:5]:  # 只看前5个
    k = np.sum(np.exp(-eigenvalues * t))
    K_t.append(k)
    print(f"  t={t:.6f}: K(t)={k:.6e}")

K_t = np.array([np.sum(np.exp(-eigenvalues * t)) for t in t_range])
print(f"\nK_t范围: [{K_t.min():.6e}, {K_t.max():.6e}]")

# 计算log
K_t_safe = np.maximum(K_t, 1e-20)
log_t = np.log(t_range)
log_K = np.log(K_t_safe)

print(f"\nlog_t范围: [{log_t.min():.4f}, {log_t.max():.4f}]")
print(f"log_K范围: [{log_K.min():.4f}, {log_K.max():.4f}]")

# 计算梯度
d_log_K = np.gradient(log_K, log_t)
print(f"\nd_log_K范围: [{d_log_K.min():.4f}, {d_log_K.max():.4f}]")

# 计算谱维度
d_s = -2 * d_log_K
print(f"\nd_s范围: [{d_s.min():.4f}, {d_s.max():.4f}]")
print(f"d_s前5个值: {d_s[:5]}")
print(f"d_s有效值(>1): {np.sum(d_s > 1)}/{len(d_s)}")
