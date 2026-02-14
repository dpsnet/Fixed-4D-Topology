"""
谱维度流分形生成器
Spectral Dimension Flow Fractal Generator

核心目标: 生成分形维度明确从 4 → 3 → 2 过渡的分形结构
用于验证 c1 = 1/4 猜想
"""

import numpy as np
from typing import Tuple, List, Callable
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SpectralFlowFractal:
    """
    谱维度流分形生成器
    
    生成具有特定谱维度流特征的分形:
    d_s(ℓ) = 4 - 0.25/ln(ℓ/ℓ_0)
    
    即:
    - 大尺度 (ℓ >> ℓ_0): d_s ≈ 4
    - 中尺度: d_s ≈ 3
    - 小尺度 (ℓ → ℓ_0): d_s → 2
    """
    
    def __init__(self, dimension: int = 4, c1: float = 0.25):
        self.d = dimension
        self.c1 = c1
        self.d_max = dimension
        self.d_min = 2.0
        
    def spectral_dimension(self, ell: np.ndarray, ell_0: float = 1.0) -> np.ndarray:
        """
        计算给定尺度的谱维度
        
        d_s(ℓ) = 4 - c1/ln(ℓ/ℓ_0)
        
        Args:
            ell: 长度尺度数组
            ell_0: 特征长度尺度
            
        Returns:
            谱维度数组
        """
        log_ratio = np.log(ell / ell_0)
        # 避免 log 接近 0
        log_ratio = np.where(np.abs(log_ratio) < 0.01, 0.01, log_ratio)
        
        d_s = self.d_max - self.c1 / log_ratio
        
        # 限制在合理范围
        d_s = np.clip(d_s, self.d_min, self.d_max)
        
        return d_s
    
    def generate_layered_fractal(self, n_points: int = 1000,
                                  ell_range: Tuple[float, float] = (0.01, 10.0),
                                  ell_0: float = 1.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        生成具有分层维度过渡的分形
        
        算法:
        1. 将长度尺度范围分成多个层
        2. 每层生成具有该尺度谱维度的点
        3. 组合所有层的点
        
        Args:
            n_points: 总点数
            ell_range: 长度尺度范围 (ell_min, ell_max)
            ell_0: 特征长度尺度
            
        Returns:
            (points, ell_values, d_s_values): 点集、对应的尺度、谱维度
        """
        ell_min, ell_max = ell_range
        n_layers = 20  # 分层数
        
        # 对数均匀分布的尺度
        ell_values = np.logspace(np.log10(ell_min), np.log10(ell_max), n_layers)
        d_s_values = self.spectral_dimension(ell_values, ell_0)
        
        points_list = []
        ell_list = []
        d_s_list = []
        
        for i, (ell, d_s) in enumerate(zip(ell_values, d_s_values)):
            # 该层的点数 (与尺度相关)
            n_at_layer = max(10, int(n_points / n_layers * (ell / ell_max)))
            
            # 生成具有谱维度 d_s 的点
            # 方法: 在 d 维空间中生成点，但沿某些维度压缩
            # 有效维度 = d_s
            
            # 确定活跃维度数
            n_active = max(1, min(self.d, int(np.round(d_s))))
            
            # 生成点
            points_layer = np.random.randn(n_at_layer, self.d) * ell
            
            # 压缩非活跃维度
            if n_active < self.d:
                # 随机选择活跃维度
                active_dims = np.random.choice(self.d, n_active, replace=False)
                mask = np.ones(self.d, dtype=bool)
                mask[active_dims] = False
                # 压缩非活跃维度
                points_layer[:, mask] *= (0.1 * ell / ell_max)
            
            points_list.append(points_layer)
            ell_list.extend([ell] * n_at_layer)
            d_s_list.extend([d_s] * n_at_layer)
        
        points = np.vstack(points_list)
        ell_array = np.array(ell_list)
        d_s_array = np.array(d_s_list)
        
        # 如果点太多，随机采样
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
            ell_array = ell_array[indices]
            d_s_array = d_s_array[indices]
        
        return points, ell_array, d_s_array
    
    def generate_ifs_fractal(self, n_points: int = 1000,
                              n_iterations: int = 10000,
                              contraction_ratios: List[float] = None) -> np.ndarray:
        """
        使用迭代函数系统 (IFS) 生成分形
        
        IFS通过仿射变换的迭代生成分形
        变换的收缩比控制分形维度
        
        Args:
            n_points: 生成的点数
            n_iterations: 迭代次数
            contraction_ratios: 收缩比列表 (控制不同尺度的维度)
            
        Returns:
            分形点集
        """
        if contraction_ratios is None:
            # 默认收缩比: 从大尺度(小收缩)到小尺度(大收缩)
            # 对应维度从4到2的过渡
            contraction_ratios = [0.9, 0.7, 0.5, 0.3]
        
        n_transforms = len(contraction_ratios)
        
        # 初始化点
        point = np.zeros(self.d)
        points = []
        
        # 丢弃前1000个点 (达到稳定状态)
        for _ in range(1000):
            # 随机选择变换
            idx = np.random.randint(n_transforms)
            ratio = contraction_ratios[idx]
            
            # 应用仿射变换
            # x' = ratio * x + translation
            translation = (1 - ratio) * (np.random.rand(self.d) - 0.5)
            point = ratio * point + translation
        
        # 收集点
        for _ in range(n_iterations):
            idx = np.random.randint(n_transforms)
            ratio = contraction_ratios[idx]
            translation = (1 - ratio) * (np.random.rand(self.d) - 0.5)
            point = ratio * point + translation
            
            if len(points) < n_points:
                points.append(point.copy())
        
        return np.array(points)
    
    def generate_dimension_transition_fractal(self, n_points: int = 1000,
                                               transition_type: str = 'smooth') -> np.ndarray:
        """
        生成维度平滑过渡的分形
        
        明确展现 4 → 3 → 2 的维度过渡
        
        Args:
            n_points: 总点数
            transition_type: 'smooth'(平滑) 或 'stepwise'(阶梯)
            
        Returns:
            分形点集
        """
        if transition_type == 'stepwise':
            # 阶梯式过渡: 4维 → 3维 → 2维
            n_per_dim = n_points // 3
            
            # 4维区域 (高维结构)
            points_4d = np.random.randn(n_per_dim, self.d)
            
            # 3维区域 (3维子空间)
            points_3d = np.random.randn(n_per_dim, self.d)
            points_3d[:, 3] *= 0.01  # 压缩第4维
            points_3d[:, 3] += 2.0   # 平移分离
            
            # 2维区域 (2维平面)
            points_2d = np.random.randn(n_per_dim, self.d)
            points_2d[:, 2:] *= 0.01  # 压缩第3、4维
            points_2d[:, 2:] += 4.0   # 平移分离
            
            points = np.vstack([points_4d, points_3d, points_2d])
            
        else:  # smooth
            # 平滑过渡: 使用径向维度过渡
            points = []
            
            for i in range(n_points):
                # 径向距离决定维度
                r = np.random.exponential(1.0)
                
                # 根据距离确定有效维度
                # r小 → 高维 (4D)
                # r大 → 低维 (2D)
                if r < 0.5:
                    d_eff = 4.0
                elif r < 1.5:
                    # 过渡区: 4 → 3
                    d_eff = 4.0 - (r - 0.5) / 1.0
                elif r < 2.5:
                    # 过渡区: 3 → 2
                    d_eff = 3.0 - (r - 1.5) / 1.0
                else:
                    d_eff = 2.0
                
                # 生成点
                point = np.random.randn(self.d) * r
                
                # 根据有效维度压缩
                n_compress = self.d - int(d_eff)
                if n_compress > 0:
                    compress_dims = np.random.choice(self.d, n_compress, replace=False)
                    point[compress_dims] *= 0.1
                
                points.append(point)
            
            points = np.array(points)
        
        return points
    
    def generate_quantum_spacetime_fractal(self, n_points: int = 1000,
                                           fluctuation_strength: float = 0.1) -> np.ndarray:
        """
        模拟量子引力度子化时空的分形结构
        
        特征:
        - 小尺度: 高度涨落 (分形维度 ~2)
        - 大尺度: 平滑 (维度 ~4)
        - 过渡区: 对数标度
        
        Args:
            n_points: 点数
            fluctuation_strength: 涨落强度
            
        Returns:
            分形点集
        """
        points = []
        
        # 中心点
        center = np.zeros(self.d)
        
        for i in range(n_points):
            # 随机选择距离中心的位置
            r = np.random.exponential(1.0)
            
            # 量子涨落: 小尺度涨落大，大尺度涨落小
            # 涨落强度 ~ 1/r (逆距离)
            local_fluctuation = fluctuation_strength / (1 + r)
            
            # 基础位置
            base_pos = np.random.randn(self.d) * r
            
            # 添加分形涨落
            # 分形维度 = 4 - c1/ln(r/r_0)
            if r > 0.01:
                d_s = min(4.0, max(2.0, 4.0 - self.c1 / np.log(r + 1)))
                
                # 根据谱维度调整涨落
                # d_s小 → 涨落各向异性强 → 维度低
                anisotropy = (4.0 - d_s) / 2.0  # 0到1之间
                
                # 在某个方向增强涨落 (模拟维度降低)
                direction = np.random.randn(self.d)
                direction /= np.linalg.norm(direction)
                
                fluctuation = local_fluctuation * (
                    np.random.randn(self.d) + 
                    anisotropy * direction * np.random.randn()
                )
            else:
                fluctuation = local_fluctuation * np.random.randn(self.d)
            
            point = base_pos + fluctuation
            points.append(point)
        
        return np.array(points)


def test_spectral_flow_fractals():
    """测试谱维度流分形生成器"""
    print("=" * 70)
    print("谱维度流分形生成器 - 测试")
    print("=" * 70)
    
    sff = SpectralFlowFractal(dimension=4, c1=0.25)
    
    # 1. 测试谱维度函数
    print("\n[1] 谱维度函数 d_s(ℓ) = 4 - 0.25/ln(ℓ/ℓ_0)")
    ell_test = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 10.0])
    d_s_test = sff.spectral_dimension(ell_test, ell_0=1.0)
    
    print(f"   {'ℓ':>8} | {'d_s(ℓ)':>10} | 维度区域")
    print(f"   {'-'*8}-+-{'-'*10}-+-----------")
    for ell, d_s in zip(ell_test, d_s_test):
        region = "高能/2D" if d_s < 2.5 else ("过渡" if d_s < 3.5 else "低能/4D")
        print(f"   {ell:8.2f} | {d_s:10.3f} | {region}")
    
    # 2. 分层分形
    print("\n[2] 生成分层维度过渡分形")
    points_layered, ell_vals, d_s_vals = sff.generate_layered_fractal(
        n_points=500, ell_range=(0.01, 10.0)
    )
    print(f"   生成点数: {len(points_layered)}")
    print(f"   谱维度范围: [{d_s_vals.min():.2f}, {d_s_vals.max():.2f}]")
    print(f"   平均谱维度: {d_s_vals.mean():.2f}")
    
    # 3. IFS分形
    print("\n[3] 生成IFS分形")
    points_ifs = sff.generate_ifs_fractal(n_points=500, n_iterations=5000)
    print(f"   生成点数: {len(points_ifs)}")
    print(f"   坐标范围: [{points_ifs.min():.3f}, {points_ifs.max():.3f}]")
    
    # 4. 维度过渡分形
    print("\n[4] 生成平滑维度过渡分形")
    points_smooth = sff.generate_dimension_transition_fractal(
        n_points=500, transition_type='smooth'
    )
    print(f"   生成点数: {len(points_smooth)}")
    
    points_step = sff.generate_dimension_transition_fractal(
        n_points=500, transition_type='stepwise'
    )
    print(f"   阶梯过渡点数: {len(points_step)}")
    
    # 5. 量子时空分形
    print("\n[5] 生成量子时空分形")
    points_quantum = sff.generate_quantum_spacetime_fractal(
        n_points=500, fluctuation_strength=0.2
    )
    print(f"   生成点数: {len(points_quantum)}")
    print(f"   坐标范围: [{points_quantum.min():.3f}, {points_quantum.max():.3f}]")
    
    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)
    
    return {
        'layered': points_layered,
        'ifs': points_ifs,
        'smooth': points_smooth,
        'stepwise': points_step,
        'quantum': points_quantum
    }


if __name__ == "__main__":
    test_data = test_spectral_flow_fractals()
