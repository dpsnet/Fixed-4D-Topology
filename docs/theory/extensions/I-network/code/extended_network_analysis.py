#!/usr/bin/env python3
"""
I方向: 扩展网络数据集分析
分析更多网络类型并验证维度层次结构
"""
import numpy as np
import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def generate_social_network(n_nodes: int, n_communities: int = 5) -> np.ndarray:
    """生成具有社区结构的社交网络"""
    np.random.seed(42)
    adj = np.zeros((n_nodes, n_nodes))
    
    nodes_per_comm = n_nodes // n_communities
    
    for c in range(n_communities):
        start = c * nodes_per_comm
        end = min((c + 1) * nodes_per_comm, n_nodes)
        
        # 社区内部高密度连接
        for i in range(start, end):
            for j in range(i + 1, end):
                if np.random.random() < 0.3:  # 30%社区内部连接概率
                    adj[i, j] = adj[j, i] = 1
        
        # 社区间低密度连接
        if c < n_communities - 1:
            next_start = (c + 1) * nodes_per_comm
            next_end = min((c + 2) * nodes_per_comm, n_nodes)
            for i in range(start, end):
                for j in range(next_start, next_end):
                    if np.random.random() < 0.05:  # 5%跨社区连接概率
                        adj[i, j] = adj[j, i] = 1
    
    return adj


def generate_biological_network(n_nodes: int) -> np.ndarray:
    """生成生物网络(PPI-like)"""
    np.random.seed(43)
    adj = np.zeros((n_nodes, n_nodes))
    
    # 少数高度连接的枢纽节点
    n_hubs = max(1, n_nodes // 20)
    hubs = np.random.choice(n_nodes, n_hubs, replace=False)
    
    for hub in hubs:
        # 枢纽节点连接到许多其他节点
        n_connections = int(n_nodes * 0.15)
        targets = np.random.choice(n_nodes, n_connections, replace=False)
        for t in targets:
            if t != hub:
                adj[hub, t] = adj[t, hub] = 1
    
    # 普通节点间稀疏连接
    for i in range(n_nodes):
        if i not in hubs:
            for j in range(i + 1, n_nodes):
                if j not in hubs and np.random.random() < 0.02:
                    adj[i, j] = adj[j, i] = 1
    
    return adj


def generate_infrastructure_network(n_nodes: int) -> np.ndarray:
    """生成基础设施网络(电网-like, 空间约束)"""
    np.random.seed(44)
    adj = np.zeros((n_nodes, n_nodes))
    
    # 将节点放在2D网格上
    grid_size = int(np.sqrt(n_nodes)) + 1
    positions = []
    for i in range(n_nodes):
        x = i % grid_size
        y = i // grid_size
        positions.append((x, y))
    
    # 主要连接最近邻
    for i in range(n_nodes):
        xi, yi = positions[i]
        for j in range(i + 1, n_nodes):
            xj, yj = positions[j]
            dist = np.sqrt((xi - xj)**2 + (yi - yj)**2)
            
            # 连接概率随距离衰减
            prob = np.exp(-dist / 2.0)
            if np.random.random() < prob:
                adj[i, j] = adj[j, i] = 1
    
    return adj


def box_counting_dimension(adj: np.ndarray, max_box_size: int = None) -> float:
    """使用盒计数法估计网络维度"""
    n = adj.shape[0]
    if max_box_size is None:
        max_box_size = n // 2
    
    box_sizes = []
    counts = []
    
    for r in range(1, min(max_box_size, 50)):
        # 简化：使用随机采样估计
        n_samples = min(100, n)
        sample_nodes = np.random.choice(n, n_samples, replace=False)
        
        covered = set()
        for node in sample_nodes:
            # BFS半径r
            visited = {node}
            frontier = {node}
            for _ in range(r):
                new_frontier = set()
                for f in frontier:
                    neighbors = np.where(adj[f] > 0)[0]
                    new_frontier.update(neighbors)
                visited.update(new_frontier)
                frontier = new_frontier
            covered.update(visited)
        
        # 估计需要多少盒子
        n_covered = len(covered)
        n_boxes = max(1, n / n_covered)
        
        box_sizes.append(r)
        counts.append(n_boxes)
    
    # 线性拟合估计维度
    if len(box_sizes) > 1:
        log_sizes = np.log(box_sizes)
        log_counts = np.log(counts)
        
        # 简单线性回归
        n = len(log_sizes)
        slope = (n * np.sum(log_sizes * log_counts) - np.sum(log_sizes) * np.sum(log_counts)) / \
                (n * np.sum(log_sizes**2) - np.sum(log_sizes)**2)
        
        return abs(slope)
    
    return 2.0


def run_i_direction_experiment():
    """运行I方向实验"""
    print("=" * 70)
    print("I方向: 扩展网络数据集分析")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'networks': []
    }
    
    configs = [
        {'name': 'Social-500', 'type': 'social', 'n_nodes': 500},
        {'name': 'Social-1000', 'type': 'social', 'n_nodes': 1000},
        {'name': 'Biological-500', 'type': 'biological', 'n_nodes': 500},
        {'name': 'Biological-1000', 'type': 'biological', 'n_nodes': 1000},
        {'name': 'Infrastructure-500', 'type': 'infrastructure', 'n_nodes': 500},
        {'name': 'Infrastructure-1000', 'type': 'infrastructure', 'n_nodes': 1000},
    ]
    
    dimensions = []
    network_names = []
    
    for cfg in configs:
        print(f"\n📊 网络: {cfg['name']}")
        
        # 生成网络
        if cfg['type'] == 'social':
            adj = generate_social_network(cfg['n_nodes'])
        elif cfg['type'] == 'biological':
            adj = generate_biological_network(cfg['n_nodes'])
        else:
            adj = generate_infrastructure_network(cfg['n_nodes'])
        
        # 计算统计
        n_edges = np.sum(adj) / 2
        avg_degree = 2 * n_edges / cfg['n_nodes']
        
        # 计算维度
        dim = box_counting_dimension(adj)
        
        network_result = {
            'name': cfg['name'],
            'type': cfg['type'],
            'n_nodes': cfg['n_nodes'],
            'n_edges': int(n_edges),
            'avg_degree': float(avg_degree),
            'dimension': float(dim)
        }
        
        results['networks'].append(network_result)
        dimensions.append(dim)
        network_names.append(cfg['name'])
        
        print(f"   节点数: {cfg['n_nodes']}, 边数: {int(n_edges)}")
        print(f"   平均度: {avg_degree:.2f}")
        print(f"   估计维度: {dim:.2f}")
    
    # 生成图表
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 图1: 维度对比
    ax1 = axes[0]
    colors = ['blue' if 'Social' in n else 'green' if 'Biological' in n else 'orange' 
              for n in network_names]
    ax1.barh(network_names, dimensions, color=colors, alpha=0.7)
    ax1.set_xlabel('Estimated Dimension')
    ax1.set_title('Network Dimensions by Type')
    ax1.axvline(x=2.0, color='red', linestyle='--', label='d=2 (spatial)')
    ax1.axvline(x=3.0, color='purple', linestyle='--', label='d=3 (social)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 图2: 规模vs维度
    ax2 = axes[1]
    social_dims = [d for n, d in zip(network_names, dimensions) if 'Social' in n]
    social_sizes = [c['n_nodes'] for c in configs if c['type'] == 'social']
    bio_dims = [d for n, d in zip(network_names, dimensions) if 'Biological' in n]
    bio_sizes = [c['n_nodes'] for c in configs if c['type'] == 'biological']
    infra_dims = [d for n, d in zip(network_names, dimensions) if 'Infrastructure' in n]
    infra_sizes = [c['n_nodes'] for c in configs if c['type'] == 'infrastructure']
    
    ax2.plot(social_sizes, social_dims, 'bo-', label='Social', linewidth=2, markersize=8)
    ax2.plot(bio_sizes, bio_dims, 'go-', label='Biological', linewidth=2, markersize=8)
    ax2.plot(infra_sizes, infra_dims, 'o-', color='orange', label='Infrastructure', linewidth=2, markersize=8)
    ax2.set_xlabel('Network Size (nodes)')
    ax2.set_ylabel('Estimated Dimension')
    ax2.set_title('Dimension vs Network Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig('i_direction_network_analysis.png', dpi=150, bbox_inches='tight')
    print(f"\n✓ 图表已保存: i_direction_network_analysis.png")
    
    # 保存结果
    with open('results_i_network_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ 结果已保存: results_i_network_analysis.json")
    
    return results


if __name__ == '__main__':
    run_i_direction_experiment()