"""
维度特定分形生成器
Dimension-Specific Fractal Generator

针对3维、4维、5维分别优化的分形生成器
"""

import numpy as np
from typing import Tuple


class DimensionSpecificFractalGenerator:
    """
    维度特定分形生成器
    
    针对每个维度优化的参数:
    - 3维: c1 = 1/3 ≈ 0.333, d_min = 2, d_max = 3
    - 4维: c1 = 1/4 = 0.250, d_min = 2, d_max = 4
    - 5维: c1 = 1/5 = 0.200, d_min = 2, d_max = 5
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.c1 = 1.0 / dimension  # c1 = 1/d
        self.d_max = float(dimension)
        self.d_min = 2.0
        
        # 维度特定参数
        self.params = self._get_dimension_params()
    
    def _get_dimension_params(self) -> dict:
        """获取维度特定参数"""
        params = {
            3: {
                'ell_range': (0.001, 100.0),
                'ell_0': 1.0,
                'n_shells': 40,
                'scale_factor': 1.5,
                'transition_width': 0.8,
            },
            4: {
                'ell_range': (0.0001, 1000.0),
                'ell_0': 1.0,
                'n_shells': 50,
                'scale_factor': 2.0,
                'transition_width': 1.0,
            },
            5: {
                'ell_range': (0.0001, 500.0),
                'ell_0': 1.0,
                'n_shells': 45,
                'scale_factor': 1.8,
                'transition_width': 0.9,
            }
        }
        return params.get(self.d, params[4])
    
    def generate_dimension_optimized(self, n_points: int = 800) -> np.ndarray:
        """
        生成维度优化的分形
        
        严格按照 d_s(ℓ) = d_max - c1/ln(ℓ/ℓ_0) 生成
        """
        p = self.params
        ell_min, ell_max = p['ell_range']
        ell_0 = p['ell_0']
        n_shells = p['n_shells']
        
        points = []
        
        # 创建壳层
        ell_shells = np.logspace(np.log10(ell_min), np.log10(ell_max), n_shells)
        
        for i in range(len(ell_shells) - 1):
            ell_center = np.sqrt(ell_shells[i] * ell_shells[i+1])
            ell_width = ell_shells[i+1] - ell_shells[i]
            
            # 计算该尺度的谱维度
            if abs(ell_center - ell_0) < 0.001:
                d_s = self.d_min
            else:
                log_ratio = np.log(ell_center / ell_0)
                if abs(log_ratio) < 0.01:
                    log_ratio = 0.01 if log_ratio > 0 else -0.01
                d_s = self.d_max - self.c1 / log_ratio
                d_s = np.clip(d_s, self.d_min, self.d_max)
            
            # 该壳层的点数
            shell_importance = self._get_shell_importance(ell_center, d_s)
            n_shell = max(5, int(n_points * shell_importance / n_shells))
            
            # 生成点
            for _ in range(n_shell):
                point = self._generate_point_at_scale(ell_center, ell_width, d_s)
                points.append(point)
        
        points = np.array(points)
        
        # 标准化到目标数量
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            additional = n_points - len(points)
            extra = np.random.randn(additional, self.d) * ell_max / 10
            points = np.vstack([points, extra])
        
        return points
    
    def _get_shell_importance(self, ell: float, d_s: float) -> float:
        """
        计算壳层重要性权重
        
        过渡区域赋予更高权重
        """
        # 过渡区域: d_s 在 (d_min + 0.5) 和 (d_max - 0.5) 之间
        transition_center = (self.d_min + self.d_max) / 2
        distance_from_transition = abs(d_s - transition_center)
        max_distance = (self.d_max - self.d_min) / 2
        
        # 过渡区重要性高
        importance = 1.0 + 2.0 * (1 - distance_from_transition / max_distance)
        
        return max(0.5, importance)
    
    def _generate_point_at_scale(self, scale: float, width: float, 
                                  d_s: float) -> np.ndarray:
        """
        在特定尺度生成具有特定谱维度的点
        """
        # 活跃维度数
        n_active = max(2, int(np.floor(d_s)))
        fractional = d_s - n_active
        
        # 基础方向
        direction = np.random.randn(self.d)
        direction /= np.linalg.norm(direction)
        
        # 径向距离 (在尺度范围内)
        r = scale + np.random.randn() * width / 3
        
        # 基础位置
        base = r * direction
        
        # 添加涨落 - 活跃维度大，非活跃维度小
        fluctuation = np.random.randn(self.d) * width / 4
        
        # 确定活跃维度
        if n_active < self.d:
            # 部分维度压缩
            compress_dims = np.random.choice(self.d, self.d - n_active, replace=False)
            
            # 完全非活跃维度压缩
            fluctuation[compress_dims] *= 0.05
            
            # 部分激活的维度(如果有)
            if fractional > 0.01 and n_active < self.d:
                partial_dim = compress_dims[0] if len(compress_dims) > 0 else 0
                fluctuation[partial_dim] *= np.sqrt(fractional)
        
        # 非活跃维度的基础位置也压缩
        if n_active < self.d:
            inactive_dims = list(set(range(self.d)) - 
                                set(range(n_active)) - 
                                set([partial_dim] if fractional > 0.01 and n_active < self.d else []))
            for dim in inactive_dims[:max(0, self.d - n_active - 1)]:
                base[dim] *= 0.1
        
        return base + fluctuation
    
    def generate_three_region_fractal(self, n_points: int = 800) -> np.ndarray:
        """
        三区结构分形
        
        明确的高维区、过渡区、低维区
        """
        points = []
        
        # 三个明确区域
        regions = [
            # (ell范围, 目标d_s, 点数比例)
            (10.0, self.params['ell_range'][1], self.d_max, 0.3),      # 高维区
            (0.1, 10.0, None, 0.4),                                    # 过渡区
            (self.params['ell_range'][0], 0.1, self.d_min, 0.3),       # 低维区
        ]
        
        for ell_a, ell_b, target_d, frac in regions:
            n_region = int(n_points * frac)
            
            # 对数均匀采样
            ell_values = np.logspace(np.log10(max(ell_a, 0.0001)), 
                                     np.log10(ell_b), 
                                     max(5, n_region // 10))
            
            for ell in ell_values:
                # 确定d_s
                if target_d is not None:
                    d_s = target_d
                else:
                    # 过渡区: 使用公式
                    log_ratio = np.log(ell / self.params['ell_0'])
                    if abs(log_ratio) < 0.01:
                        log_ratio = 0.01
                    d_s = self.d_max - self.c1 / log_ratio
                    d_s = np.clip(d_s, self.d_min, self.d_max)
                
                n_at_scale = max(2, n_region // len(ell_values))
                
                for _ in range(n_at_scale):
                    point = self._generate_point_at_scale(ell, ell * 0.1, d_s)
                    points.append(point)
        
        points = np.array(points) if points else np.random.randn(n_points, self.d)
        
        # 标准化
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            extra = np.random.randn(n_points - len(points), self.d) * 0.5
            points = np.vstack([points, extra])
        
        return points


def test_dimension_specific():
    """测试维度特定生成器"""
    print("=" * 70)
    print("维度特定分形生成器 - 测试")
    print("=" * 70)
    
    for dim in [3, 4, 5]:
        print(f"\n{'='*70}")
        print(f"{dim}维空间 - 理论c1 = 1/{dim} = {1.0/dim:.6f}")
        print(f"{'='*70}")
        
        gen = DimensionSpecificFractalGenerator(dimension=dim)
        
        # 测试方法1
        print("\n方法1: 维度优化分形")
        np.random.seed(42)
        points1 = gen.generate_dimension_optimized(n_points=500)
        print(f"  生成点数: {len(points1)}")
        print(f"  坐标范围: [{points1.min():.3f}, {points1.max():.3f}]")
        
        # 测试方法2
        print("\n方法2: 三区结构分形")
        np.random.seed(42)
        points2 = gen.generate_three_region_fractal(n_points=500)
        print(f"  生成点数: {len(points2)}")
        print(f"  坐标范围: [{points2.min():.3f}, {points2.max():.3f}]")
        
        # 打印参数
        print(f"\n  参数:")
        print(f"    ell范围: {gen.params['ell_range']}")
        print(f"    壳层数: {gen.params['n_shells']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_dimension_specific()
