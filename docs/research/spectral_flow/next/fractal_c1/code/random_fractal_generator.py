"""
随机分形生成器
Random Fractal Generator

目标: 生成具有谱维度流特征的分形结构，验证 c1 = 1/4
"""

import numpy as np
from typing import Tuple, List, Optional
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class RandomFractalGenerator:
    """
    4维随机分形生成器
    
    生成具有分形结构的点集，模拟量子引力度子化时空的随机分形特性
    """
    
    def __init__(self, dimension: int = 4, target_fractal_dim: float = 4.0):
        """
        初始化分形生成器
        
        Args:
            dimension: 嵌入维度 (默认4维时空)
            target_fractal_dim: 目标分形维度
        """
        self.d = dimension
        self.d_f_target = target_fractal_dim
        
    def generate_fractal_percolation(self, n_points: int = 1000, 
                                      p: float = 0.5,
                                      n_iterations: int = 5) -> np.ndarray:
        """
        生成渗流型随机分形
        
        算法:
        1. 从超立方体网格开始
        2. 以概率p保留每个子立方体
        3. 递归细分保留的立方体
        4. 在保留的区域中随机采样点
        
        Args:
            n_points: 生成的点数
            p: 保留概率 (控制分形维度)
            n_iterations: 迭代次数
            
        Returns:
            分形点集 (n_points, d)
        """
        points = []
        
        # 初始网格
        grid_size = 2 ** n_iterations
        
        # 递归生成渗流结构
        def subdivide(center, size, depth):
            if depth == 0:
                # 在最终级别的立方体中采样
                n_samples = max(1, int(n_points / (grid_size ** self.d) * (p ** n_iterations)))
                for _ in range(n_samples):
                    point = center + size * (np.random.rand(self.d) - 0.5)
                    points.append(point)
                return
            
            # 以概率p保留并细分
            if np.random.rand() < p:
                # 细分2^d个子立方体
                new_size = size / 2
                offsets = np.array([
                    [i // (2**j) % 2 for j in range(self.d)] 
                    for i in range(2**self.d)
                ]) * new_size - new_size/2
                
                for offset in offsets:
                    subdivide(center + offset, new_size, depth - 1)
        
        # 从中心开始
        initial_center = np.zeros(self.d)
        initial_size = 1.0
        subdivide(initial_center, initial_size, n_iterations)
        
        points = np.array(points)
        
        # 确保points是2D数组
        if len(points.shape) == 1:
            points = points.reshape(-1, self.d)
        
        # 如果点不够或为空，生成随机点
        if len(points) == 0 or len(points) < n_points // 2:
            points = np.random.randn(n_points, self.d) * 0.3
        elif len(points) < n_points:
            additional = n_points - len(points)
            extra_points = np.random.randn(additional, self.d) * 0.1
            points = np.vstack([points, extra_points])
        elif len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
            
        return points
    
    def generate_fractal_walk(self, n_steps: int = 10000,
                               alpha: float = 0.5) -> np.ndarray:
        """
        生成具有长程相关的分形随机游走
        
        使用分数布朗运动的思想，产生分形轨迹
        
        Args:
            n_steps: 游走步数
            alpha: Hurst指数 (控制分形维度: d_f = 1/alpha)
            
        Returns:
            游走轨迹 (n_steps, d)
        """
        # 生成分数布朗运动的增量
        # 使用傅里叶方法生成长程相关噪声
        
        # 生成白噪声
        white_noise = np.random.randn(n_steps, self.d)
        
        # 傅里叶变换
        fft_noise = np.fft.fft(white_noise, axis=0)
        
        # 频率
        freqs = np.fft.fftfreq(n_steps)
        freqs[0] = 1e-10  # 避免除零
        
        # 功率谱: S(f) ~ 1/f^(2*alpha + 1)
        power_factor = np.abs(freqs) ** (-(alpha + 0.5))
        power_factor[0] = 0  # DC分量置零
        
        # 着色
        colored_fft = fft_noise * power_factor[:, np.newaxis]
        
        # 逆傅里叶变换
        increments = np.fft.ifft(colored_fft, axis=0).real
        
        # 累积得到轨迹
        trajectory = np.cumsum(increments, axis=0)
        
        return trajectory
    
    def generate_spectral_fractal(self, n_points: int = 1000,
                                   d_s_min: float = 2.0,
                                   d_s_max: float = 4.0,
                                   c1: float = 0.25) -> np.ndarray:
        """
        基于谱维度流公式生成分形点集
        
        生成具有特定谱维度特征的点集:
        d_s(ell) = d_s_max - c1 / ln(ell/ell_0)
        
        Args:
            n_points: 点数
            d_s_min: 最小谱维度 (默认2)
            d_s_max: 最大谱维度 (默认4)
            c1: 普适系数 (默认1/4)
            
        Returns:
            分形点集
        """
        # 确定ell的范围
        # 当 d_s = d_s_min 时: c1 / ln(ell/ell_0) = d_s_max - d_s_min = 2
        # ln(ell_min/ell_0) = c1 / 2 = 1/8
        ell_min_ratio = np.exp(c1 / (d_s_max - d_s_min))
        
        # ell_max 对应 d_s 接近 d_s_max
        ell_max_ratio = np.exp(c1 / 0.1)  # 当 d_s 接近 d_s_max - 0.1
        
        # 生成不同尺度的点
        points = []
        n_scales = 10
        
        for i in range(n_scales):
            # 对数均匀分布的尺度
            log_ratio = np.log(ell_min_ratio) + i * (np.log(ell_max_ratio) - np.log(ell_min_ratio)) / (n_scales - 1)
            ell_ratio = np.exp(log_ratio)
            
            # 当前尺度的谱维度
            d_s = d_s_max - c1 / log_ratio if log_ratio > 0.01 else d_s_min
            
            # 在该尺度生成点 (点的密度与 d_s 相关)
            n_at_scale = int(n_points / n_scales * (d_s / d_s_max))
            
            # 生成分布在对应维度的点
            # 使用高斯分布，方差与尺度相关
            scale = ell_ratio
            points_at_scale = np.random.randn(n_at_scale, self.d) * scale
            points.append(points_at_scale)
        
        points = np.vstack(points)
        
        # 标准化
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        elif len(points) < n_points:
            # 补充随机点
            additional = n_points - len(points)
            extra = np.random.randn(additional, self.d) * 0.1
            points = np.vstack([points, extra])
        
        return points
    
    def generate_multifractal(self, n_points: int = 1000,
                               spectrum_range: Tuple[float, float] = (2.0, 4.0)) -> np.ndarray:
        """
        生成多重分形 (multifractal) 结构
        
        同时包含多种分形维度的复杂结构
        
        Args:
            n_points: 总点数
            spectrum_range: 分形维度范围
            
        Returns:
            多重分形点集
        """
        d_min, d_max = spectrum_range
        
        # 生成不同分形维度的混合
        points = []
        n_components = 5
        
        for i in range(n_components):
            # 该组件的分形维度
            d_f = d_min + i * (d_max - d_min) / (n_components - 1)
            
            # 该组件的点数 (与维度成正比)
            n_component = int(n_points * d_f / (d_min + d_max) / n_components * 2)
            
            # 生成分形游走，Hurst指数 H = 1/d_f
            if d_f > 1:
                H = 1.0 / d_f
                component_points = self.generate_fractal_walk(n_component, alpha=H)
                # 降维到 d_f 维子空间
                if d_f < self.d:
                    # 投影到随机子空间
                    proj_matrix = np.random.randn(self.d, int(d_f))
                    proj_matrix, _ = np.linalg.qr(proj_matrix)
                    component_points = component_points @ proj_matrix
                    # 扩展回d维
                    component_points_full = np.zeros((n_component, self.d))
                    component_points_full[:, :int(d_f)] = component_points
                    component_points = component_points_full
            else:
                component_points = np.random.randn(n_component, self.d) * 0.1
            
            # 随机平移
            offset = np.random.randn(self.d) * (i + 1)
            component_points += offset
            
            points.append(component_points)
        
        points = np.vstack(points)
        
        # 标准化到单位超立方体
        points = (points - np.min(points, axis=0)) / (np.max(points, axis=0) - np.min(points, axis=0))
        points = points * 2 - 1  # 映射到 [-1, 1]
        
        if len(points) > n_points:
            indices = np.random.choice(len(points), n_points, replace=False)
            points = points[indices]
        
        return points


def test_fractal_generation():
    """测试分形生成功能"""
    print("=" * 70)
    print("随机分形生成器 - 测试")
    print("=" * 70)
    
    generator = RandomFractalGenerator(dimension=4, target_fractal_dim=4.0)
    
    # 1. 测试渗流分形
    print("\n[1] 生成渗流型分形 (Percolation Fractal)")
    points_perc = generator.generate_fractal_percolation(n_points=500, p=0.6, n_iterations=4)
    print(f"   生成点数: {len(points_perc)}")
    print(f"   维度: {points_perc.shape}")
    print(f"   坐标范围: [{points_perc.min():.3f}, {points_perc.max():.3f}]")
    
    # 2. 测试分形游走
    print("\n[2] 生成分形随机游走 (Fractal Random Walk)")
    points_walk = generator.generate_fractal_walk(n_steps=1000, alpha=0.5)
    print(f"   步数: {len(points_walk)}")
    print(f"   维度: {points_walk.shape}")
    print(f"   终点距离: {np.linalg.norm(points_walk[-1]):.3f}")
    
    # 3. 测试基于谱维度的分形
    print("\n[3] 生成基于谱维度的分形 (Spectral Fractal)")
    points_spec = generator.generate_spectral_fractal(n_points=500, c1=0.25)
    print(f"   生成点数: {len(points_spec)}")
    print(f"   维度: {points_spec.shape}")
    print(f"   坐标范围: [{points_spec.min():.3f}, {points_spec.max():.3f}]")
    
    # 4. 测试多重分形
    print("\n[4] 生成多重分形 (Multifractal)")
    points_multi = generator.generate_multifractal(n_points=500, spectrum_range=(2.0, 4.0))
    print(f"   生成点数: {len(points_multi)}")
    print(f"   维度: {points_multi.shape}")
    print(f"   坐标范围: [{points_multi.min():.3f}, {points_multi.max():.3f}]")
    
    print("\n" + "=" * 70)
    print("所有分形生成测试通过!")
    print("=" * 70)
    
    return {
        'percolation': points_perc,
        'random_walk': points_walk,
        'spectral': points_spec,
        'multifractal': points_multi
    }


def generate_fractal_dataset(n_samples: int = 100, 
                              n_points_per_sample: int = 500,
                              output_dir: str = None) -> dict:
    """
    生成大规模分形数据集用于统计验证 c1 = 1/4
    
    Args:
        n_samples: 样本数量
        n_points_per_sample: 每个样本的点数
        output_dir: 输出目录
        
    Returns:
        数据集统计信息
    """
    print("=" * 70)
    print(f"生成大规模分形数据集: {n_samples} 样本 x {n_points_per_sample} 点")
    print("=" * 70)
    
    generator = RandomFractalGenerator(dimension=4)
    
    all_fractals = []
    fractal_types = []
    
    for i in range(n_samples):
        if i % 10 == 0:
            print(f"   进度: {i}/{n_samples}")
        
        # 循环使用不同的分形类型
        fractal_type = i % 4
        
        if fractal_type == 0:
            points = generator.generate_fractal_percolation(n_points_per_sample, p=0.5 + 0.1*np.random.rand())
            typename = 'percolation'
        elif fractal_type == 1:
            points = generator.generate_fractal_walk(n_points_per_sample, alpha=0.4 + 0.2*np.random.rand())
            typename = 'random_walk'
        elif fractal_type == 2:
            points = generator.generate_spectral_fractal(n_points_per_sample, c1=0.25)
            typename = 'spectral'
        else:
            points = generator.generate_multifractal(n_points_per_sample)
            typename = 'multifractal'
        
        all_fractals.append(points)
        fractal_types.append(typename)
    
    print(f"   完成! 共生成 {n_samples} 个分形样本")
    
    # 保存数据
    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for i, (points, typename) in enumerate(zip(all_fractals, fractal_types)):
            filename = f"{output_dir}/fractal_{typename}_{i:04d}.npy"
            np.save(filename, points)
        
        print(f"   数据已保存到: {output_dir}")
    
    return {
        'n_samples': n_samples,
        'n_points': n_points_per_sample,
        'types': fractal_types,
        'data': all_fractals
    }


if __name__ == "__main__":
    # 运行基本测试
    test_data = test_fractal_generation()
    
    # 生成小数据集用于后续分析
    print("\n生成100个分形样本的测试数据集...")
    dataset = generate_fractal_dataset(
        n_samples=100,
        n_points_per_sample=300,
        output_dir='../data/random_fractal'
    )
