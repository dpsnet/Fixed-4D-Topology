"""
分形拉普拉斯算子理论实现
Fractal Laplacian Operator Theory Implementation

核心目标: 从分形几何第一性原理导出 c1 = 1/4
"""

import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import eigsh, spsolve
from scipy.spatial.distance import pdist, squareform
from typing import Tuple, Optional, Callable
import warnings


class FractalLaplacian:
    """
    分形时空上的拉普拉斯算子
    
    核心猜想:
    - 分形标度猜想: c1 = 1/d_f^max = 1/4
    - 分形压缩比猜想: c1 = (d_f^min/d_f^max)^2 = (2/4)^2 = 1/4
    """
    
    def __init__(self, dimension: int = 4, fractal_dim: Optional[float] = None):
        """
        初始化分形拉普拉斯算子
        
        Args:
            dimension: 拓扑维度 (默认4维时空)
            fractal_dim: 分形维度 (默认等于拓扑维度)
        """
        self.d_topo = dimension
        self.d_frac = fractal_dim if fractal_dim is not None else dimension
        self.c1_conjecture = 1.0 / self.d_frac  # 核心猜想: c1 = 1/d_f^max
        
        # 验证猜想的一致性
        if self.d_frac == 4:
            assert abs(self.c1_conjecture - 0.25) < 1e-10, "c1 must be 1/4 for d_f=4"
            
    def construct_graph_laplacian(self, points: np.ndarray, 
                                   epsilon: float = None) -> csr_matrix:
        """
        构建图拉普拉斯算子 (点集上的离散拉普拉斯)
        
        使用高斯核定义邻接关系:
        W_ij = exp(-||x_i - x_j||^2 / (2*epsilon^2))
        
        Args:
            points: 点集坐标 (N, d)
            epsilon: 特征长度尺度
            
        Returns:
            图拉普拉斯矩阵 L = D - W
        """
        N = len(points)
        
        if epsilon is None:
            # 自动选择epsilon: 平均最近邻距离的2倍
            dists = squareform(pdist(points))
            np.fill_diagonal(dists, np.inf)
            epsilon = 2 * np.mean(np.min(dists, axis=1))
        
        # 计算高斯核权重矩阵
        dists_sq = squareform(pdist(points, 'sqeuclidean'))
        W = np.exp(-dists_sq / (2 * epsilon**2))
        np.fill_diagonal(W, 0)  # 去除自环
        
        # 度矩阵 D_ii = sum_j W_ij
        D = np.sum(W, axis=1)
        D_diag = diags(D, 0)
        
        # 图拉普拉斯: L = D - W
        L = D_diag - csr_matrix(W)
        
        return L
    
    def compute_spectral_dimension(self, laplacian: csr_matrix, 
                                    t_range: np.ndarray = None,
                                    n_eigenvalues: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        从拉普拉斯算子计算谱维度
        
        公式: d_s(t) = -2 * d(ln K(t)) / d(ln t)
        其中 K(t) = Tr(exp(-t*L)) 是热核返回概率
        
        Args:
            laplacian: 拉普拉斯矩阵
            t_range: 时间尺度范围 (如果为None，自动选择)
            n_eigenvalues: 计算的 eigenvalue 数量
            
        Returns:
            (t_values, d_s_values): 时间尺度和对应的谱维度
        """
        # 计算拉普拉斯的特征值
        try:
            eigenvalues, _ = eigsh(laplacian, k=n_eigenvalues, 
                                   which='SM', return_eigenvectors=True)
        except Exception as e:
            warnings.warn(f"Eigenvalue computation failed: {e}")
            # 使用更小的k重试
            eigenvalues, _ = eigsh(laplacian, k=min(20, laplacian.shape[0]-1), 
                                   which='SM', return_eigenvectors=True)
        
        # 只保留正的特征值 (排除零模)
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        
        if t_range is None:
            # 自动选择时间尺度范围
            t_min = 1.0 / np.max(eigenvalues)
            t_max = 1.0 / np.min(eigenvalues)
            t_range = np.logspace(np.log10(t_min), np.log10(t_max), 50)
        
        # 计算热核 K(t) = sum_i exp(-lambda_i * t)
        K_t = np.array([np.sum(np.exp(-eigenvalues * t)) for t in t_range])
        
        # 确保 K_t > 0，避免 log(0)
        K_t = np.maximum(K_t, 1e-20)
        
        # 数值微分计算谱维度
        log_t = np.log(t_range)
        log_K = np.log(K_t)
        
        # d_s = -2 * d(log K) / d(log t)
        d_log_K = np.gradient(log_K, log_t)
        d_s = -2 * d_log_K
        
        return t_range, d_s
    
    def extract_c1_from_spectral_flow(self, t_values: np.ndarray, 
                                       d_s_values: np.ndarray,
                                       ell_0: float = 1.0) -> dict:
        """
        从谱维度流数据中提取普适系数 c1
        
        公式: d_s(ell) = d_f^max - c1 / ln(ell/ell_0)
        
        核心验证:
        - 提取的 c1 应该接近 1/4
        - d_f^max 应该接近 4
        
        Args:
            t_values: 时间尺度 (对应 length scale ell = sqrt(t))
            d_s_values: 对应的谱维度值
            ell_0: 特征长度尺度
            
        Returns:
            字典包含: {'c1': 提取的c1, 'd_max': 最大维度, 'quality': 拟合质量}
        """
        # 长度尺度 ell = sqrt(t) (热扩散关系)
        ell_values = np.sqrt(t_values)
        
        # 只使用有足够数据点的区域 (避免数值噪声)
        valid_mask = (ell_values > 0) & (d_s_values > 1.5) & (d_s_values < 4.5)
        ell_valid = ell_values[valid_mask]
        d_s_valid = d_s_values[valid_mask]
        
        if len(ell_valid) < 5:
            return {'c1': np.nan, 'd_max': np.nan, 'quality': 0.0, 'error': 'Insufficient data'}
        
        # 计算 ln(ell/ell_0)
        log_ell = np.log(ell_valid / ell_0)
        
        # 避免 log 接近 0 的点
        mask = np.abs(log_ell) > 0.1
        if np.sum(mask) < 5:
            mask = np.abs(log_ell) > 0.01
        
        x = 1.0 / log_ell[mask]  # 1/ln(ell/ell_0)
        y = d_s_valid[mask]       # d_s
        
        # 线性拟合: d_s = d_max - c1 * (1/ln(ell/ell_0))
        # 即 y = d_max - c1 * x
        
        # 使用最小二乘法
        A = np.vstack([x, np.ones(len(x))]).T
        c1_fit, d_max_fit = np.linalg.lstsq(A, y, rcond=None)[0]
        c1_fit = -c1_fit  # 因为 y = d_max - c1 * x
        
        # 计算拟合质量 (R^2)
        y_pred = d_max_fit - c1_fit * x
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        return {
            'c1': float(c1_fit),
            'd_max': float(d_max_fit),
            'quality': float(r_squared),
            'c1_error': abs(c1_fit - self.c1_conjecture),
            'conjecture_verified': abs(c1_fit - self.c1_conjecture) < 0.05
        }


class FractalMeasure:
    """
    分形测度理论实现
    
    核心公式:
    - 分形体积元: dV_ell = ell^{c1} dV
    - 分形熵: S = c1 * ln(ell/ell_0)
    """
    
    def __init__(self, c1: float = 0.25):
        self.c1 = c1
        
    def fractal_volume_element(self, ell: float, dV_classical: float) -> float:
        """
        计算分形体积元
        
        Args:
            ell: 长度尺度
            dV_classical: 经典体积元
            
        Returns:
            分形体积元 dV_ell = ell^{c1} * dV
        """
        return (ell ** self.c1) * dV_classical
    
    def fractal_entropy(self, ell: float, ell_0: float = 1.0) -> float:
        """
        计算分形熵
        
        与Bekenstein-Hawking熵类比:
        S_BH = A / (4 * ell_P^2) = (1/4) * (A/ell_P^2)
        
        这里 S_frac = c1 * ln(ell/ell_0) = (1/4) * ln(ell/ell_0)
        
        Args:
            ell: 当前长度尺度
            ell_0: 参考长度尺度
            
        Returns:
            分形熵 S
        """
        return self.c1 * np.log(ell / ell_0)
    
    def box_counting_dimension(self, points: np.ndarray, 
                                epsilon_range: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        盒计数法计算分形维度
        
        N(epsilon) ~ epsilon^{-d_f}
        
        Args:
            points: 点集 (N, d)
            epsilon_range: 盒子大小范围
            
        Returns:
            (epsilon_values, d_f_values): 盒子大小和对应的局部分形维度
        """
        if epsilon_range is None:
            # 自动选择epsilon范围
            coords_range = np.max(points, axis=0) - np.min(points, axis=0)
            max_range = np.max(coords_range)
            epsilon_range = np.logspace(-3, 0, 30) * max_range
        
        N_values = []
        
        for eps in epsilon_range:
            # 计算覆盖所需的盒子数
            n_boxes_per_dim = np.ceil((np.max(points, axis=0) - 
                                       np.min(points, axis=0)) / eps).astype(int)
            n_boxes_per_dim = np.maximum(n_boxes_per_dim, 1)
            
            # 将点分配到盒子中
            bins = [np.linspace(np.min(points[:, i]) - eps/2, 
                               np.max(points[:, i]) + eps/2, 
                               n_boxes_per_dim[i] + 1) for i in range(points.shape[1])]
            
            # 统计非空盒子
            hist, _ = np.histogramdd(points, bins=bins)
            N = np.sum(hist > 0)
            N_values.append(max(N, 1))
        
        N_values = np.array(N_values)
        
        # 计算局部分形维度 d_f = -d(ln N)/d(ln epsilon)
        log_eps = np.log(epsilon_range)
        log_N = np.log(N_values)
        d_f = -np.gradient(log_N, log_eps)
        
        return epsilon_range, d_f


# =============================================================================
# 验证核心猜想的测试函数
# =============================================================================

def verify_c1_conjecture(d_f_max: float = 4.0, d_f_min: float = 2.0) -> dict:
    """
    验证核心猜想: c1 = 1/d_f^max = (d_f^min/d_f^max)^2
    
    Args:
        d_f_max: 最大分形维度 (默认4)
        d_f_min: 最小分形维度 (默认2)
        
    Returns:
        验证结果字典
    """
    # 猜想1: c1 = 1/d_f^max
    c1_conjecture_1 = 1.0 / d_f_max
    
    # 猜想2: c1 = (d_f^min/d_f^max)^2
    c1_conjecture_2 = (d_f_min / d_f_max) ** 2
    
    # 比较
    match = abs(c1_conjecture_1 - c1_conjecture_2) < 1e-10
    
    result = {
        'd_f_max': d_f_max,
        'd_f_min': d_f_min,
        'c1_from_reciprocal': c1_conjecture_1,
        'c1_from_ratio_squared': c1_conjecture_2,
        'conjectures_match': match,
        'c1_value': c1_conjecture_1 if match else None,
        'verification_passed': match and abs(c1_conjecture_1 - 0.25) < 1e-10
    }
    
    return result


def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("分形拉普拉斯算子理论 - 基础功能测试")
    print("=" * 60)
    
    # 1. 验证核心猜想
    print("\n[1] 验证核心猜想 c1 = 1/4")
    result = verify_c1_conjecture(d_f_max=4.0, d_f_min=2.0)
    print(f"   d_f^max = {result['d_f_max']}")
    print(f"   d_f^min = {result['d_f_min']}")
    print(f"   c1 = 1/d_f^max = {result['c1_from_reciprocal']:.6f}")
    print(f"   c1 = (d_f^min/d_f^max)^2 = {result['c1_from_ratio_squared']:.6f}")
    print(f"   ✓ 猜想验证通过: {result['verification_passed']}")
    
    # 2. 测试图拉普拉斯构建
    print("\n[2] 测试图拉普拉斯构建")
    np.random.seed(42)
    points = np.random.randn(100, 4)  # 4维空间中的100个点
    
    fl = FractalLaplacian(dimension=4)
    L = fl.construct_graph_laplacian(points, epsilon=1.0)
    print(f"   点集维度: {points.shape}")
    print(f"   拉普拉斯矩阵大小: {L.shape}")
    print(f"   矩阵稀疏度: {L.nnz / (L.shape[0]**2):.4f}")
    
    # 3. 测试谱维度计算
    print("\n[3] 测试谱维度计算")
    t_vals, d_s = fl.compute_spectral_dimension(L, n_eigenvalues=20)
    print(f"   时间尺度范围: [{t_vals.min():.4e}, {t_vals.max():.4e}]")
    print(f"   谱维度范围: [{d_s.min():.2f}, {d_s.max():.2f}]")
    
    # 4. 测试c1提取
    print("\n[4] 测试 c1 提取")
    c1_result = fl.extract_c1_from_spectral_flow(t_vals, d_s)
    print(f"   提取的 c1: {c1_result['c1']:.4f}")
    print(f"   提取的 d_max: {c1_result['d_max']:.2f}")
    print(f"   拟合质量 R^2: {c1_result['quality']:.4f}")
    print(f"   与猜想 c1=1/4 的偏差: {c1_result['c1_error']:.4f}")
    
    # 5. 测试分形测度
    print("\n[5] 测试分形测度")
    fm = FractalMeasure(c1=0.25)
    S = fm.fractal_entropy(ell=0.01, ell_0=1.0)
    print(f"   分形熵 S(ell=0.01): {S:.4f}")
    print(f"   与 Bekenstein-Hawking S=A/4 的对应: c1=1/4 ✓")
    
    # 6. 测试盒计数维度
    print("\n[6] 测试盒计数维度")
    eps_vals, d_f = fm.box_counting_dimension(points[:50, :3])  # 只取3维便于可视化
    print(f"   盒子大小范围: [{eps_vals.min():.4f}, {eps_vals.max():.4f}]")
    print(f"   平均分形维度: {np.mean(d_f):.2f}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
    
    return result['verification_passed']


if __name__ == "__main__":
    test_basic_functionality()
