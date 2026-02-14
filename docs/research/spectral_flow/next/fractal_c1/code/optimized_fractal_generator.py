"""
优化的分形生成器
Optimized Fractal Generator

专门设计用于精确展现 4 → 3 → 2 维度过渡
确保c1 = 1/4的准确提取
"""

import numpy as np
from typing import Tuple, List


class OptimizedFractalGenerator:
    """
    优化的分形生成器
    
    核心改进:
    1. 更宽的尺度范围 (0.0001 to 1000)
    2. 明确的4→3→2维度过渡
    3. 更好的统计采样
    4. 针对谱维度流优化的结构
    """
    
    def __init__(self, dimension: int = 4, c1: float = 0.25):
        self.d = dimension
        self.c1 = c1
        self.d_max = dimension
        self.d_min = 2.0
        
    def generate_dimension_cascade(self, n_points: int = 2000,
                                    ell_min: float = 0.0001,
                                    ell_max: float = 1000.0,
                                    ell_0: float = 1.0) -> np.ndarray:
        """
        生成维度级联分形 - 明确展现4→3→2过渡
        
        算法:
        1. 将尺度空间分成三个明确区域:
           - 大尺度 (ℓ > 10): d_s ≈ 4
           - 过渡区 (0.1 < ℓ < 10): d_s = 4 - 0.25/ln(ℓ)
           - 小尺度 (ℓ < 0.1): d_s ≈ 2
        2. 在每个区域生成对应维度的点
        3. 确保过渡平滑
        
        Args:
            n_points: 总点数 (推荐2000+)
            ell_min: 最小尺度
            ell_max: 最大尺度
            ell_0: 特征尺度
            
        Returns:
            分形点集
        """
        points = []
        
        # 定义三个区域
        regions = [
            # (ell_min, ell_max, target_d_s, n_fraction)
            (10.0, ell_max, 4.0, 0.25),      # 高维区: d_s ≈ 4
            (0.1, 10.0, None, 0.50),          # 过渡区: 公式计算
            (ell_min, 0.1, 2.0, 0.25),        # 低维区: d_s ≈ 2
        ]
        
        for ell_a, ell_b, target_d, frac in regions:
            n_region = int(n_points * frac)
            
            # 在该区域内对数均匀采样
            ell_values = np.logspace(np.log10(ell_a), np.log10(ell_b), 
                                     max(10, n_region // 10))
            
            for ell in ell_values:
                # 确定该尺度的谱维度
                if target_d is not None:
                    d_s = target_d
                else:
                    # 过渡区: 使用公式
                    log_ratio = np.log(ell / ell_0)
                    if abs(log_ratio) < 0.01:
                        log_ratio = 0.01
                    d_s = self.d_max - self.c1 / log_ratio
                    d_s = np.clip(d_s, self.d_min, self.d_max)
                
                # 该尺度的点数
                n_at_scale = max(3, n_region // len(ell_values))
                
                # 生成具有d_s维特征的点
                points_at_scale = self._generate_points_at_dimension(
                    n_at_scale, ell, d_s
                )
                points.append(points_at_scale)
        
        points = np.vstack(points)
        
        # 标准化到目标数量
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            additional = n_points - len(points)
            extra = np.random.randn(additional, self.d) * 0.1
            points = np.vstack([points, extra])
        
        return points
    
    def _generate_points_at_dimension(self, n: int, scale: float, 
                                      d_s: float) -> np.ndarray:
        """
        生成具有特定谱维度的点
        
        Args:
            n: 点数
            scale: 长度尺度
            d_s: 目标谱维度
            
        Returns:
            点集 (n, d)
        """
        # 活跃维度数
        n_active = max(1, min(self.d, int(np.floor(d_s))))
        fractional = d_s - n_active  # 小数部分
        
        points = np.zeros((n, self.d))
        
        # 活跃维度
        active_dims = list(range(n_active))
        if fractional > 0.01 and n_active < self.d:
            # 部分激活下一个维度
            active_dims.append(n_active)
        
        # 生成点
        for i in range(n):
            # 活跃维度
            for dim in active_dims[:n_active]:
                points[i, dim] = np.random.randn() * scale
            
            # 部分激活维度 (如果有)
            if len(active_dims) > n_active and fractional > 0.01:
                dim = active_dims[n_active]
                points[i, dim] = np.random.randn() * scale * np.sqrt(fractional)
            
            # 非活跃维度: 小涨落
            inactive = [d for d in range(self.d) if d not in active_dims]
            for dim in inactive:
                points[i, dim] = np.random.randn() * scale * 0.05
        
        return points
    
    def generate_hierarchical_fractal(self, n_points: int = 2000,
                                       n_levels: int = 8) -> np.ndarray:
        """
        生成层次化分形
        
        每一层对应一个尺度级别，从顶层(4D)到底层(2D)
        
        Args:
            n_points: 总点数
            n_levels: 层次数 (越多过渡越平滑)
            
        Returns:
            分形点集
        """
        points = []
        
        # 从顶层(4D)到底层(2D)
        for level in range(n_levels, -1, -1):
            # 该层的维度
            d_progress = level / n_levels  # 0到1
            d_s = self.d_min + (self.d_max - self.d_min) * d_progress
            
            # 该层的点数
            n_level = max(50, int(n_points / (n_levels + 1)))
            
            # 该层的尺度 (大尺度->小尺度)
            scale = 10.0 * (0.5 ** (n_levels - level))
            
            # 生成该层的点
            points_level = self._generate_points_at_dimension(n_level, scale, d_s)
            
            # 添加位置偏移 (分离不同层)
            offset = np.array([level * 5.0] + [0.0] * (self.d - 1))
            points_level += offset
            
            points.append(points_level)
        
        return np.vstack(points)
    
    def generate_anisotropic_fractal(self, n_points: int = 2000) -> np.ndarray:
        """
        生成各向异性分形
        
        不同方向有不同的维度特征，整体展现维度过渡
        
        Args:
            n_points: 点数
            
        Returns:
            分形点集
        """
        points = []
        
        # 分成不同方向的簇
        n_clusters = 20
        
        for i in range(n_clusters):
            # 该簇的维度 (从4到2渐变)
            progress = i / (n_clusters - 1)
            d_s = self.d_max - (self.d_max - self.d_min) * progress
            
            # 点数
            n_cluster = n_points // n_clusters
            
            # 尺度
            scale = 1.0 / (1 + i * 0.5)
            
            # 生成簇
            cluster = self._generate_points_at_dimension(n_cluster, scale, d_s)
            
            # 随机偏移
            offset = np.random.randn(self.d) * 10.0
            cluster += offset
            
            points.append(cluster)
        
        return np.vstack(points)
    
    def generate_shell_structure(self, n_points: int = 2000,
                                  n_shells: int = 50) -> np.ndarray:
        """
        生成壳层结构分形
        
        类似洋葱结构，每层壳有不同的有效维度
        
        Args:
            n_points: 总点数
            n_shells: 壳层数
            
        Returns:
            分形点集
        """
        points = []
        
        # 径向距离范围
        r_min, r_max = 0.01, 100.0
        
        for i in range(n_shells):
            # 壳层半径
            r_inner = r_min * (r_max / r_min) ** (i / n_shells)
            r_outer = r_min * (r_max / r_min) ** ((i + 1) / n_shells)
            r_center = np.sqrt(r_inner * r_outer)
            
            # 该壳层的维度
            # 大半径 -> 高维度 (~4)
            # 小半径 -> 低维度 (~2)
            log_ratio = np.log(r_center)
            if abs(log_ratio) < 0.01:
                d_s = (self.d_max + self.d_min) / 2
            else:
                d_s = self.d_max - self.c1 / log_ratio
                d_s = np.clip(d_s, self.d_min, self.d_max)
            
            # 壳层内的点数 (与表面积成正比)
            surface_area = r_center ** (d_s - 1)
            n_shell = max(10, int(n_points * surface_area / (r_max ** self.d)))
            
            # 生成壳层点
            for _ in range(n_shell):
                # 随机方向
                direction = np.random.randn(self.d)
                direction /= np.linalg.norm(direction)
                
                # 径向距离 (在壳层内)
                r = r_inner + np.random.rand() * (r_outer - r_inner)
                
                # 基础位置
                base = r * direction
                
                # 添加具有d_s维特征的涨落
                n_active = max(1, min(self.d, int(np.round(d_s))))
                fluctuation = np.random.randn(self.d) * (r_outer - r_inner) / 3
                
                # 压缩非活跃维度
                if n_active < self.d:
                    inactive = np.random.choice(self.d, self.d - n_active, replace=False)
                    fluctuation[inactive] *= 0.1
                
                point = base + fluctuation
                points.append(point)
        
        return np.array(points)


def test_optimized_fractals():
    """测试优化的分形生成器"""
    print("=" * 70)
    print("优化的分形生成器 - 测试")
    print("=" * 70)
    
    ofg = OptimizedFractalGenerator(dimension=4, c1=0.25)
    
    methods = {
        'dimension_cascade': lambda: ofg.generate_dimension_cascade(500),
        'hierarchical': lambda: ofg.generate_hierarchical_fractal(500, 6),
        'anisotropic': lambda: ofg.generate_anisotropic_fractal(500),
        'shell_structure': lambda: ofg.generate_shell_structure(500, 20)
    }
    
    for name, generator in methods.items():
        print(f"\n[ {name} ]")
        np.random.seed(42)
        points = generator()
        print(f"  点数: {len(points)}")
        print(f"  范围: [{points.min():.3f}, {points.max():.3f}]")
        print(f"  标准差: {np.std(points):.3f}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_optimized_fractals()
