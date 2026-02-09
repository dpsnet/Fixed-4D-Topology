#!/usr/bin/env python3
"""
J方向: 随机分形3D可视化
生成3D渗流 cluster 和分形结构
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
from datetime import datetime


def generate_3d_percolation_cluster(size: int = 50, p: float = 0.3) -> np.ndarray:
    """
    生成3D渗流cluster
    
    Args:
        size: 网格大小
        p: 占据概率
    
    Returns:
        3D二进制数组 (1=占据, 0=空)
    """
    np.random.seed(42)
    
    # 随机占据
    grid = np.random.random((size, size, size)) < p
    
    # 找到最大cluster
    from scipy import ndimage
    labeled, n_clusters = ndimage.label(grid)
    
    if n_clusters > 0:
        # 找到最大的cluster
        cluster_sizes = np.bincount(labeled.ravel())[1:]  # 跳过背景
        largest_cluster_id = np.argmax(cluster_sizes) + 1
        largest_cluster = (labeled == largest_cluster_id)
        return largest_cluster
    
    return grid


def estimate_fractal_dimension_3d(cluster: np.ndarray) -> float:
    """
    使用盒计数法估计3D分形维度
    """
    sizes = []
    counts = []
    
    # 不同大小的盒子
    for box_size in [2, 4, 8, 16]:
        count = 0
        for i in range(0, cluster.shape[0], box_size):
            for j in range(0, cluster.shape[1], box_size):
                for k in range(0, cluster.shape[2], box_size):
                    # 检查盒子内是否有占据的格点
                    box = cluster[i:i+box_size, j:j+box_size, k:k+box_size]
                    if np.any(box):
                        count += 1
        
        sizes.append(box_size)
        counts.append(count)
    
    # 线性拟合估计维度
    log_sizes = np.log(sizes)
    log_counts = np.log(counts)
    
    # 简单线性回归
    n = len(log_sizes)
    slope = (n * np.sum(log_sizes * log_counts) - np.sum(log_sizes) * np.sum(log_counts)) / \
            (n * np.sum(log_sizes**2) - np.sum(log_sizes)**2)
    
    return abs(slope)


def plot_3d_cluster(cluster: np.ndarray, title: str, filename: str):
    """绘制3D cluster"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 获取占据的格点坐标
    x, y, z = np.where(cluster)
    
    # 随机采样以改善可视化
    if len(x) > 5000:
        indices = np.random.choice(len(x), 5000, replace=False)
        x, y, z = x[indices], y[indices], z[indices]
    
    # 绘制散点
    ax.scatter(x, y, z, c='blue', marker='o', s=20, alpha=0.6)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()


def generate_sierpinski_3d(n_iterations: int = 4) -> np.ndarray:
    """生成3D Sierpinski海绵"""
    size = 3**n_iterations
    grid = np.ones((size, size, size), dtype=bool)
    
    for i in range(n_iterations):
        step = 3**(n_iterations - i - 1)
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    # Sierpinski规则：如果恰好一个坐标为1（中心），则移除
                    if [x, y, z].count(1) >= 2:
                        grid[x*step:(x+1)*step, 
                             y*step:(y+1)*step, 
                             z*step:(z+1)*step] = False
    
    return grid


def run_j_direction_experiment():
    """运行J方向实验"""
    print("=" * 70)
    print("J方向: 随机分形3D可视化")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'fractals': []
    }
    
    # 实验1: 3D渗流
    print("\n📊 实验1: 3D渗流Cluster")
    for p in [0.25, 0.3, 0.35]:
        print(f"   占据概率 p={p}")
        cluster = generate_3d_percolation_cluster(size=40, p=p)
        dim = estimate_fractal_dimension_3d(cluster)
        n_occupied = np.sum(cluster)
        
        print(f"      占据格点数: {n_occupied}")
        print(f"      估计分形维度: {dim:.2f}")
        
        plot_3d_cluster(cluster, f'3D Percolation (p={p}, d={dim:.2f})', 
                       f'j_percolation_p{p}.png')
        
        results['fractals'].append({
            'type': 'percolation',
            'p': p,
            'dimension': float(dim),
            'n_occupied': int(n_occupied)
        })
    
    # 实验2: Sierpinski海绵
    print("\n📊 实验2: Sierpinski海绵")
    sierpinski = generate_sierpinski_3d(n_iterations=3)
    dim_sierp = estimate_fractal_dimension_3d(sierpinski)
    n_sierp = np.sum(sierpinski)
    
    print(f"   占据格点数: {n_sierp}")
    print(f"   估计分形维度: {dim_sierp:.2f}")
    print(f"   理论维度: ~2.73")
    
    plot_3d_cluster(sierpinski, f'Sierpinski Sponge (d={dim_sierp:.2f})', 
                   'j_sierpinski.png')
    
    results['fractals'].append({
        'type': 'sierpinski',
        'dimension': float(dim_sierp),
        'n_occupied': int(n_sierp),
        'theoretical_dim': 2.73
    })
    
    # 生成汇总图表
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # 渗流p vs 维度
    ax1 = axes[0, 0]
    percolation_data = [(r['p'], r['dimension']) for r in results['fractals'] if r['type'] == 'percolation']
    if percolation_data:
        ps, dims = zip(*percolation_data)
        ax1.plot(ps, dims, 'bo-', linewidth=2, markersize=10)
        ax1.set_xlabel('Occupation Probability p')
        ax1.set_ylabel('Fractal Dimension')
        ax1.set_title('Percolation: p vs Fractal Dimension')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=3.0, color='red', linestyle='--', alpha=0.5, label='d=3 (compact)')
        ax1.legend()
    
    # 对比图
    ax2 = axes[0, 1]
    types = ['Percolation\n(p=0.25)', 'Percolation\n(p=0.3)', 'Percolation\n(p=0.35)', 'Sierpinski']
    dims = [r['dimension'] for r in results['fractals']]
    colors = ['blue', 'blue', 'blue', 'green']
    ax2.bar(types, dims, color=colors, alpha=0.7)
    ax2.set_ylabel('Fractal Dimension')
    ax2.set_title('Fractal Dimension Comparison')
    ax2.axhline(y=3.0, color='red', linestyle='--', alpha=0.5)
    ax2.tick_params(axis='x', rotation=15)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 占据格点数
    ax3 = axes[1, 0]
    occupied = [r['n_occupied'] for r in results['fractals']]
    ax3.bar(types, occupied, color=colors, alpha=0.7)
    ax3.set_ylabel('Number of Occupied Sites')
    ax3.set_title('Cluster Size Comparison')
    ax3.tick_params(axis='x', rotation=15)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 理论vs实验维度
    ax4 = axes[1, 1]
    sierp_data = [r for r in results['fractals'] if r['type'] == 'sierpinski'][0]
    ax4.bar(['Experimental', 'Theoretical'], 
            [sierp_data['dimension'], sierp_data['theoretical_dim']],
            color=['green', 'orange'], alpha=0.7)
    ax4.set_ylabel('Fractal Dimension')
    ax4.set_title('Sierpinski: Experimental vs Theoretical')
    ax4.set_ylim([2.5, 2.8])
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('j_direction_summary.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ 汇总图表已保存: j_direction_summary.png")
    
    # 保存结果
    with open('results_j_fractals.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ 结果已保存: results_j_fractals.json")
    
    return results


if __name__ == '__main__':
    run_j_direction_experiment()
