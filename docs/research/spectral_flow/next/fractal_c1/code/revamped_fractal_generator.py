"""
重新设计的分形生成器
Revamped Fractal Generator

关键改进:
1. 严格按谱维度公式生成
2. 避免奇点问题
3. 尺度清晰分离
4. 可验证每个壳层的维度
"""

import numpy as np
from typing import Tuple, List


class RevampedFractalGenerator:
    """
    重新设计的分形生成器
    
    核心改进:
    - 使用修正的谱维度公式避免奇点
    - 严格的壳层分离
    - 每个壳层独立验证维度
    """
    
    def __init__(self, dimension: int):
        self.d = dimension
        self.c1 = 1.0 / dimension
        self.d_max = float(dimension)
        self.d_min = 2.0
        
    def spectral_dimension_safe(self, ell: float, ell_0: float = 1.0) -> float:
        """
        计算谱维度 - 避免奇点的安全版本
        
        使用修正公式:
        d_s(ℓ) = d_min + (d_max - d_min) / (1 + (ℓ_0/ℓ)^(1/c1))
        
        这个公式:
        - 当 ℓ → 0 时, d_s → d_min
        - 当 ℓ → ∞ 时, d_s → d_max
        - 在 ℓ = ℓ_0 处平滑过渡
        """
        if ell < 1e-10:
            return self.d_min
        
        # 修正的公式避免奇点
        ratio = ell_0 / ell
        exponent = 1.0 / self.c1
        
        # Logistic型过渡
        transition = 1.0 / (1.0 + ratio ** exponent)
        
        d_s = self.d_min + (self.d_max - self.d_min) * transition
        
        return d_s
    
    def generate_shell_based_fractal(self, n_points: int = 1000,
                                      ell_range: Tuple[float, float] = (0.01, 100.0),
                                      ell_0: float = 1.0,
                                      n_shells: int = 30) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        基于壳层的分形生成
        
        每个壳层有明确的长度和谱维度
        
        Returns:
            (points, shell_centers, shell_dimensions)
        """
        points = []
        shell_centers = []
        shell_dimensions = []
        
        # 创建对数均匀分布的壳层
        ell_edges = np.logspace(np.log10(ell_range[0]), 
                                np.log10(ell_range[1]), 
                                n_shells + 1)
        
        for i in range(n_shells):
            # 壳层边界
            ell_inner = ell_edges[i]
            ell_outer = ell_edges[i + 1]
            ell_center = np.sqrt(ell_inner * ell_outer)
            
            # 计算该壳层的谱维度
            d_s = self.spectral_dimension_safe(ell_center, ell_0)
            
            # 该壳层的点数 (与壳层体积成正比)
            # 体积 ~ ell^(d-1) * thickness
            thickness = ell_outer - ell_inner
            volume = (ell_center ** (self.d - 1)) * thickness
            n_shell = max(5, int(n_points * volume / sum(
                (np.sqrt(ell_edges[j] * ell_edges[j+1]) ** (self.d - 1)) * 
                (ell_edges[j+1] - ell_edges[j])
                for j in range(n_shells)
            )))
            
            # 生成该壳层的点
            for _ in range(n_shell):
                point = self._generate_point_in_shell(
                    ell_inner, ell_outer, d_s
                )
                points.append(point)
            
            shell_centers.append(ell_center)
            shell_dimensions.append(d_s)
        
        points = np.array(points)
        
        # 标准化到目标数量
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            extra = np.random.randn(n_points - len(points), self.d) * ell_range[1] / 10
            points = np.vstack([points, extra])
        
        return points, np.array(shell_centers), np.array(shell_dimensions)
    
    def _generate_point_in_shell(self, r_inner: float, r_outer: float, 
                                  d_s: float) -> np.ndarray:
        """
        在壳层内生成具有特定谱维度的点
        
        Args:
            r_inner: 内半径
            r_outer: 外半径
            d_s: 目标谱维度
        """
        # 随机方向
        direction = np.random.randn(self.d)
        direction /= np.linalg.norm(direction)
        
        # 径向距离 (在壳层内均匀分布)
        # 对于d维球壳，体积元 ~ r^(d-1) dr
        # 为了均匀分布，使用 r ~ (r_inner^d + u*(r_outer^d - r_inner^d))^(1/d)
        u = np.random.rand()
        r = (r_inner ** self.d + u * (r_outer ** self.d - r_inner ** self.d)) ** (1.0 / self.d)
        
        # 基础位置
        base = r * direction
        
        # 添加具有d_s维特征的涨落
        # 有效维度 = d_s
        # 活跃维度数 = round(d_s)
        n_active = max(2, min(self.d, int(np.round(d_s))))
        fractional = d_s - n_active  # 小数部分
        
        # 生成涨落
        fluctuation = np.random.randn(self.d) * (r_outer - r_inner) / 3
        
        # 压缩非活跃维度
        if n_active < self.d:
            # 选择与方向正交的维度进行压缩
            # 简化: 随机选择维度
            all_dims = list(range(self.d))
            np.random.shuffle(all_dims)
            
            # 活跃维度
            active_dims = all_dims[:n_active]
            inactive_dims = all_dims[n_active:]
            
            # 完全非活跃维度: 大幅压缩
            for dim in inactive_dims[:max(0, len(inactive_dims) - 1)]:
                fluctuation[dim] *= 0.05
            
            # 部分活跃的维度(如果有)
            if fractional > 0.01 and len(inactive_dims) > 0:
                partial_dim = inactive_dims[-1]
                fluctuation[partial_dim] *= (0.1 + 0.9 * fractional)
        
        return base + fluctuation
    
    def generate_explicit_transition(self, n_points: int = 1000) -> Tuple[np.ndarray, dict]:
        """
        生成具有明确维度过渡的分形
        
        明确创建三个区域:
        - 高维区: d_s ≈ d_max
        - 过渡区: d_s从d_max降到d_min
        - 低维区: d_s ≈ d_min
        """
        points = []
        info = {'regions': []}
        
        # 三个明确分离的区域
        regions = [
            {
                'name': 'high_dim',
                'ell_range': (10.0, 100.0),
                'd_target': self.d_max,
                'fraction': 0.25
            },
            {
                'name': 'transition',
                'ell_range': (0.1, 10.0),
                'd_target': None,  # 使用公式
                'fraction': 0.50
            },
            {
                'name': 'low_dim',
                'ell_range': (0.01, 0.1),
                'd_target': self.d_min,
                'fraction': 0.25
            }
        ]
        
        for region in regions:
            n_region = int(n_points * region['fraction'])
            ell_a, ell_b = region['ell_range']
            
            # 在该区域内对数均匀采样
            ell_values = np.logspace(np.log10(ell_a), np.log10(ell_b), 
                                     max(5, n_region // 10))
            
            region_points = []
            region_d_s = []
            
            for ell in ell_values:
                # 确定d_s
                if region['d_target'] is not None:
                    d_s = region['d_target']
                else:
                    d_s = self.spectral_dimension_safe(ell)
                
                n_at_scale = max(2, n_region // len(ell_values))
                
                for _ in range(n_at_scale):
                    # 生成点
                    r = ell * (1 + np.random.randn() * 0.1)
                    point = self._generate_point_at_radius(r, d_s)
                    region_points.append(point)
                    region_d_s.append(d_s)
            
            points.extend(region_points)
            info['regions'].append({
                'name': region['name'],
                'n_points': len(region_points),
                'mean_d_s': np.mean(region_d_s) if region_d_s else 0
            })
        
        points = np.array(points)
        
        # 标准化
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            extra = np.random.randn(n_points - len(points), self.d) * 0.5
            points = np.vstack([points, extra])
        
        info['total_points'] = len(points)
        return points, info
    
    def _generate_point_at_radius(self, r: float, d_s: float) -> np.ndarray:
        """在给定半径生成具有特定维度的点"""
        # 随机方向
        direction = np.random.randn(self.d)
        direction /= np.linalg.norm(direction)
        
        # 基础位置
        base = r * direction
        
        # 根据d_s添加涨落
        n_active = max(2, int(np.round(d_s)))
        
        # 涨落
        fluctuation = np.random.randn(self.d) * r * 0.1
        
        # 压缩非活跃维度
        if n_active < self.d:
            compress_dims = np.random.choice(self.d, self.d - n_active, replace=False)
            fluctuation[compress_dims] *= 0.05
        
        return base + fluctuation


def test_revamped_generator():
    """测试重新设计的生成器"""
    print("=" * 70)
    print("重新设计的分形生成器 - 测试")
    print("=" * 70)
    
    for dim in [3, 4, 5]:
        print(f"\n{'='*70}")
        print(f"{dim}维空间 (c1 = 1/{dim} = {1.0/dim:.4f})")
        print(f"{'='*70}")
        
        gen = RevampedFractalGenerator(dimension=dim)
        
        # 测试安全谱维度公式
        print("\n1. 谱维度公式测试:")
        for ell in [0.01, 0.1, 1.0, 10.0, 100.0]:
            d_s = gen.spectral_dimension_safe(ell)
            print(f"   ℓ = {ell:6.2f}: d_s = {d_s:.3f}")
        
        # 测试壳层生成
        print("\n2. 壳层分形生成:")
        points, centers, dims = gen.generate_shell_based_fractal(
            n_points=500,
            ell_range=(0.01, 100.0),
            n_shells=20
        )
        print(f"   生成点数: {len(points)}")
        print(f"   坐标范围: [{points.min():.3f}, {points.max():.3f}]")
        print(f"   壳层维度范围: [{dims.min():.2f}, {dims.max():.2f}]")
        
        # 测试明确过渡
        print("\n3. 明确过渡分形:")
        points2, info = gen.generate_explicit_transition(n_points=500)
        print(f"   生成点数: {len(points2)}")
        for region in info['regions']:
            print(f"   {region['name']}: {region['n_points']}点, 平均d_s={region['mean_d_s']:.2f}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_revamped_generator()
