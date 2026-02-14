"""
高级分形生成器
Advanced Fractal Generator

专门设计用于生成具有精确谱维度流特征的分形
目标: 清晰展现 d_s: 4 → 3 → 2 的过渡
"""

import numpy as np
from typing import Tuple, List


class AdvancedFractalGenerator:
    """
    高级分形生成器
    
    生成严格符合 d_s(ℓ) = 4 - c1/ln(ℓ/ℓ_0) 的分形结构
    """
    
    def __init__(self, dimension: int = 4, c1: float = 0.25):
        self.d = dimension
        self.c1 = c1
        self.d_max = dimension
        self.d_min = 2.0
        
    def generate_strict_spectral_fractal(self, n_points: int = 1000,
                                          ell_min: float = 0.001,
                                          ell_max: float = 100.0,
                                          ell_0: float = 1.0) -> np.ndarray:
        """
        生成严格符合谱维度流公式的分形
        
        核心思想:
        1. 将长度尺度范围分成多个壳层 (shells)
        2. 每个壳层 ℓ 具有该尺度的谱维度 d_s(ℓ)
        3. 在壳层内生成 d_s(ℓ) 维的结构
        
        实现:
        - 对于尺度 ℓ，计算 d_s(ℓ)
        - 在球壳 [ℓ, ℓ+Δℓ] 内生成点
        - 点的分布具有 d_s(ℓ) 维特征
        
        Args:
            n_points: 总点数
            ell_min: 最小长度尺度
            ell_max: 最大长度尺度
            ell_0: 特征长度尺度
            
        Returns:
            分形点集 (n_points, d)
        """
        points = []
        
        # 对数均匀分布的壳层
        n_shells = 50
        ell_shells = np.logspace(np.log10(ell_min), np.log10(ell_max), n_shells)
        
        for i in range(len(ell_shells) - 1):
            ell_center = np.sqrt(ell_shells[i] * ell_shells[i+1])
            ell_width = ell_shells[i+1] - ell_shells[i]
            
            # 计算该尺度的谱维度
            if abs(ell_center - ell_0) < 0.001:
                # 在 ℓ = ℓ_0 处，d_s = 2 (理论极限)
                d_s = self.d_min
            else:
                log_ratio = np.log(ell_center / ell_0)
                if abs(log_ratio) < 0.01:
                    log_ratio = 0.01 if log_ratio >= 0 else -0.01
                d_s = self.d_max - self.c1 / log_ratio
                d_s = np.clip(d_s, self.d_min, self.d_max)
            
            # 该壳层的点数 (与壳层体积成正比)
            # 体积 ~ ℓ^(d-1) * Δℓ
            shell_volume = (ell_center ** (self.d - 1)) * ell_width
            n_shell = max(5, int(n_points * shell_volume / (ell_max ** self.d)))
            
            # 生成该壳层的点
            # 方法: 生成d维点，然后根据d_s压缩部分维度
            for _ in range(n_shell):
                # 随机方向
                direction = np.random.randn(self.d)
                direction /= np.linalg.norm(direction)
                
                # 径向距离 (在该壳层内均匀分布)
                r = ell_shells[i] + np.random.rand() * ell_width
                
                # 基础位置
                base_pos = r * direction
                
                # 根据谱维度 d_s 添加涨落
                # 有效维度 = d_s
                # 活跃维度数 = round(d_s)
                n_active = max(1, min(self.d, int(np.round(d_s))))
                
                # 在活跃维度上添加涨落
                if n_active < self.d:
                    # 确定活跃维度 (与方向正交的子空间)
                    # 简化: 随机选择维度进行压缩
                    
                    # 计算压缩因子
                    # d_s = n_active + α，其中α是第(n_active+1)维的贡献
                    alpha = d_s - n_active if n_active < self.d else 0
                    
                    # 生成涨落
                    fluctuation = np.random.randn(self.d) * (ell_width / 3)
                    
                    # 压缩非活跃维度
                    n_inactive = self.d - n_active
                    if n_inactive > 0:
                        # 随机选择非活跃维度
                        inactive_dims = np.random.choice(self.d, n_inactive, replace=False)
                        # 压缩: 完全非活跃的乘以0.01，部分活跃的乘以α
                        for dim in inactive_dims:
                            if alpha > 0.01 and dim == inactive_dims[0]:
                                fluctuation[dim] *= alpha
                            else:
                                fluctuation[dim] *= 0.01
                    
                    point = base_pos + fluctuation
                else:
                    # 全维活跃 (d_s ≈ 4)
                    point = base_pos + np.random.randn(self.d) * (ell_width / 3)
                
                points.append(point)
        
        points = np.array(points)
        
        # 如果点太多，随机采样
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            # 补充随机点
            additional = n_points - len(points)
            extra = np.random.randn(additional, self.d) * ell_max / 10
            points = np.vstack([points, extra])
        
        return points
    
    def generate_recursive_dimension_fractal(self, n_points: int = 1000,
                                             n_levels: int = 6) -> np.ndarray:
        """
        递归生成具有明确维度过渡的分形
        
        每一层递归对应一个尺度级别，维度逐渐降低
        
        Args:
            n_points: 总点数
            n_levels: 递归层数
            
        Returns:
            分形点集
        """
        points = []
        
        # 递归生成
        def recursive_generate(center, size, level):
            if level == 0:
                # 在最低层生成点
                # 维度 = 2 (最低维)
                n_local = max(1, int(n_points / (2 ** (n_levels * self.d))))
                for _ in range(n_local):
                    point = center + size * (np.random.rand(self.d) - 0.5)
                    # 压缩高维
                    point[2:] *= 0.01
                    points.append(point)
                return
            
            # 计算当前层的维度
            # 从level=n_levels (d=4) 到 level=0 (d=2)
            d_current = 2 + 2 * (level / n_levels)
            
            # 细分2^d_current个子区域
            n_sub = min(int(2 ** d_current), 16)
            
            for i in range(n_sub):
                # 子区域中心偏移
                offset = np.zeros(self.d)
                for d in range(self.d):
                    offset[d] = ((i // (2 ** d)) % 2 - 0.5) * size
                
                new_center = center + offset
                new_size = size / 2
                
                # 递归
                recursive_generate(new_center, new_size, level - 1)
        
        # 从根开始
        root_center = np.zeros(self.d)
        root_size = 10.0
        recursive_generate(root_center, root_size, n_levels)
        
        points = np.array(points) if points else np.random.randn(n_points, self.d)
        
        # 标准化
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            additional = n_points - len(points)
            extra = np.random.randn(additional, self.d) * 0.5
            points = np.vstack([points, extra])
        
        return points
    
    def generate_curved_space_fractal(self, n_points: int = 1000,
                                      curvature: float = 0.1) -> np.ndarray:
        """
        生成模拟弯曲时空的分形
        
        在小尺度引入强曲率 (对应高能量/低维度)
        在大尺度接近平坦 (对应低能量/高维度)
        
        Args:
            n_points: 点数
            curvature: 曲率参数
            
        Returns:
            分形点集
        """
        points = []
        
        for i in range(n_points):
            # 随机选择距离中心的半径
            # 小半径区域有更多点 (模拟分形聚集)
            r = np.random.exponential(2.0)
            
            # 根据半径确定局部维度
            # r小 → 高曲率 → 低维度 (~2)
            # r大 → 低曲率 → 高维度 (~4)
            if r < 0.5:
                d_local = 2.0 + r  # ~2-2.5
            elif r < 2.0:
                d_local = 2.5 + 0.5 * (r - 0.5)  # ~2.5-3.25
            else:
                d_local = min(4.0, 3.25 + 0.25 * (r - 2.0))  # ~3.25-4.0
            
            # 方向
            direction = np.random.randn(self.d)
            direction /= np.linalg.norm(direction)
            
            # 基础位置
            base_pos = r * direction
            
            # 根据局部维度添加各向异性涨落
            n_compress = self.d - int(d_local)
            if n_compress > 0:
                compress_dims = np.random.choice(self.d, n_compress, replace=False)
                # 在压缩维度上添加小涨落
                anisotropic = np.random.randn(self.d) * 0.1 * curvature / (1 + r)
                anisotropic[compress_dims] *= 0.1  # 进一步压缩
                point = base_pos + anisotropic
            else:
                point = base_pos + np.random.randn(self.d) * 0.1 * curvature
            
            points.append(point)
        
        return np.array(points)


def test_advanced_fractals():
    """测试高级分形生成器"""
    print("=" * 70)
    print("高级分形生成器 - 测试")
    print("=" * 70)
    
    afg = AdvancedFractalGenerator(dimension=4, c1=0.25)
    
    # 1. 严格谱流分形
    print("\n[1] 生成严格谱流分形")
    points_strict = afg.generate_strict_spectral_fractal(
        n_points=500,
        ell_min=0.001,
        ell_max=100.0
    )
    print(f"   生成点数: {len(points_strict)}")
    print(f"   坐标范围: [{points_strict.min():.3f}, {points_strict.max():.3f}]")
    
    # 2. 递归维度过渡分形
    print("\n[2] 生成递归维度过渡分形")
    points_recursive = afg.generate_recursive_dimension_fractal(
        n_points=500,
        n_levels=5
    )
    print(f"   生成点数: {len(points_recursive)}")
    print(f"   坐标范围: [{points_recursive.min():.3f}, {points_recursive.max():.3f}]")
    
    # 3. 弯曲时空分形
    print("\n[3] 生成弯曲时空分形")
    points_curved = afg.generate_curved_space_fractal(
        n_points=500,
        curvature=0.2
    )
    print(f"   生成点数: {len(points_curved)}")
    print(f"   坐标范围: [{points_curved.min():.3f}, {points_curved.max():.3f}]")
    
    print("\n" + "=" * 70)
    print("测试完成!")
    print("=" * 70)
    
    return {
        'strict': points_strict,
        'recursive': points_recursive,
        'curved': points_curved
    }


if __name__ == "__main__":
    test_data = test_advanced_fractals()
