"""
Large Real Network Analyzer
==========================

Analyzes very large real networks (like AS-Skitter) with sampling.
Optimized for pure Python without numpy.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import random
import math
from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class NetworkStats:
    """Network statistics summary."""
    name: str
    num_nodes: int
    num_edges: int
    avg_degree: float
    max_degree: int
    sample_size: int
    

def load_large_network_sample(filepath: str, sample_ratio: float = 0.1, 
                              max_edges: int = 100000) -> Dict[int, Set[int]]:
    """
    Load a large network with sampling for memory efficiency.
    
    Args:
        filepath: Path to edge list file
        sample_ratio: Fraction of nodes to sample
        max_edges: Maximum number of edges to load
        
    Returns:
        Sampled graph as adjacency list
    """
    print(f"Loading network from {filepath}...")
    print(f"Sample ratio: {sample_ratio}, Max edges: {max_edges}")
    
    # First pass: count nodes and get degree distribution sample
    node_degrees = {}
    edge_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                try:
                    u = int(parts[0])
                    v = int(parts[1])
                    
                    node_degrees[u] = node_degrees.get(u, 0) + 1
                    node_degrees[v] = node_degrees.get(v, 0) + 1
                    edge_count += 1
                    
                    if edge_count >= max_edges * 2:  # Sample for analysis
                        break
                        
                except ValueError:
                    continue
    
    total_nodes = len(node_degrees)
    print(f"Total nodes in sample: {total_nodes}")
    print(f"Total edges in sample: {edge_count}")
    
    # Select high-degree nodes for sampling (more representative)
    sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)
    sample_size = int(total_nodes * sample_ratio)
    
    # Mix of high-degree and random nodes
    high_degree_count = sample_size // 2
    random_count = sample_size - high_degree_count
    
    sampled_nodes = set()
    for node, _ in sorted_nodes[:high_degree_count]:
        sampled_nodes.add(node)
    
    # Add random nodes
    remaining_nodes = [n for n, _ in sorted_nodes[high_degree_count:]]
    if remaining_nodes and random_count > 0:
        sampled_nodes.update(random.sample(remaining_nodes, 
                                          min(random_count, len(remaining_nodes))))
    
    print(f"Sampled {len(sampled_nodes)} nodes")
    
    # Second pass: build subgraph
    graph = {node: set() for node in sampled_nodes}
    edges_loaded = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                try:
                    u = int(parts[0])
                    v = int(parts[1])
                    
                    if u in sampled_nodes and v in sampled_nodes:
                        graph[u].add(v)
                        graph[v].add(u)
                        edges_loaded += 1
                        
                    if edges_loaded >= max_edges:
                        break
                        
                except ValueError:
                    continue
    
    # Remove isolated nodes
    graph = {n: neighbors for n, neighbors in graph.items() if neighbors}
    
    print(f"Final sampled graph: {len(graph)} nodes, {edges_loaded} edges")
    return graph


def compute_basic_stats(graph: Dict[int, Set[int]]) -> NetworkStats:
    """Compute basic network statistics."""
    n = len(graph)
    
    degrees = [len(neighbors) for neighbors in graph.values()]
    m = sum(degrees) // 2
    avg_k = sum(degrees) / n if n > 0 else 0
    max_k = max(degrees) if degrees else 0
    
    return NetworkStats(
        name="sampled_network",
        num_nodes=n,
        num_edges=m,
        avg_degree=avg_k,
        max_degree=max_k,
        sample_size=n
    )


def compute_clustering_coefficient(graph: Dict[int, Set[int]], 
                                   sample_size: int = 1000) -> float:
    """
    Compute average clustering coefficient (sampled for speed).
    """
    nodes = list(graph.keys())
    sample = random.sample(nodes, min(sample_size, len(nodes)))
    
    clustering_sum = 0.0
    valid_nodes = 0
    
    for node in sample:
        neighbors = graph[node]
        k = len(neighbors)
        
        if k < 2:
            continue
        
        # Count triangles
        triangles = 0
        neighbor_list = list(neighbors)
        
        for i in range(k):
            for j in range(i + 1, k):
                if neighbor_list[j] in graph.get(neighbor_list[i], set()):
                    triangles += 1
        
        possible = k * (k - 1) / 2
        if possible > 0:
            clustering_sum += triangles / possible
            valid_nodes += 1
    
    return clustering_sum / valid_nodes if valid_nodes > 0 else 0.0


def compute_box_dimension_fast(graph: Dict[int, Set[int]], 
                               max_box: int = 5,
                               num_samples: int = 100) -> float:
    """
    Fast box-counting using sampling (for large networks).
    """
    nodes = list(graph.keys())
    n = len(nodes)
    
    if n < 100:
        return 1.0
    
    box_sizes = []
    box_counts = []
    
    # Use smaller range for large networks
    for lb in range(1, min(max_box + 1, n // 20)):
        # Sample nodes for box centers
        centers = random.sample(nodes, min(num_samples, n))
        
        # Greedy covering from sampled centers
        uncovered = set(nodes)
        num_boxes = 0
        
        for center in centers:
            if center not in uncovered:
                continue
            
            # BFS ball of radius lb
            ball = bfs_ball(graph, center, lb)
            ball &= uncovered
            
            if ball:
                uncovered -= ball
                num_boxes += 1
            
            if not uncovered:
                break
        
        # Count remaining isolated nodes as their own boxes
        num_boxes += len(uncovered)
        
        box_sizes.append(lb)
        box_counts.append(num_boxes)
    
    # Log-log regression
    if len(box_sizes) < 2:
        return 1.0
    
    log_inv_sizes = [math.log(1.0 / lb) for lb in box_sizes]
    log_counts = [math.log(max(c, 1)) for c in box_counts]
    
    # Linear regression
    n_pts = len(log_inv_sizes)
    x_mean = sum(log_inv_sizes) / n_pts
    y_mean = sum(log_counts) / n_pts
    
    numerator = sum((log_inv_sizes[i] - x_mean) * (log_counts[i] - y_mean) 
                   for i in range(n_pts))
    denominator = sum((x - x_mean) ** 2 for x in log_inv_sizes)
    
    if denominator == 0:
        return 1.0
    
    dimension = numerator / denominator
    return max(0.5, min(5.0, dimension))


def bfs_ball(graph: Dict[int, Set[int]], center: int, radius: int) -> Set[int]:
    """BFS to get ball of given radius."""
    ball = {center}
    frontier = {center}
    
    for _ in range(radius):
        new_frontier = set()
        for node in frontier:
            new_frontier.update(graph.get(node, set()))
        new_frontier -= ball
        ball.update(new_frontier)
        frontier = new_frontier
        if not frontier:
            break
    
    return ball


def analyze_as_skitter(filepath: str = "./as-skitter.txt"):
    """Analyze the AS-Skitter network."""
    print("=" * 80)
    print("AS-Skitter Internet Topology Analysis")
    print("=" * 80)
    print()
    
    # Load with sampling (10% of nodes, max 100k edges)
    graph = load_large_network_sample(filepath, sample_ratio=0.05, max_edges=50000)
    
    if not graph:
        print("Failed to load graph")
        return
    
    # Basic stats
    print("\nComputing basic statistics...")
    stats = compute_basic_stats(graph)
    print(f"Sampled Nodes: {stats.num_nodes:,}")
    print(f"Sampled Edges: {stats.num_edges:,}")
    print(f"Average Degree: {stats.avg_degree:.2f}")
    print(f"Max Degree: {stats.max_degree:,}")
    
    # Clustering
    print("\nComputing clustering coefficient (sampled)...")
    C = compute_clustering_coefficient(graph, sample_size=500)
    print(f"Clustering Coefficient: {C:.3f}")
    
    # Box dimension
    print("\nComputing box dimension (fast method)...")
    d_B = compute_box_dimension_fast(graph, max_box=5, num_samples=200)
    print(f"Box Dimension: {d_B:.3f}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY - AS-Skitter Internet AS Topology")
    print("=" * 80)
    print(f"Full Network: 1,696,415 nodes, 11,095,298 edges")
    print(f"Sample Analyzed: {stats.num_nodes:,} nodes, {stats.num_edges:,} edges")
    print(f"Average Degree: {stats.avg_degree:.2f}")
    print(f"Clustering Coefficient: {C:.3f}")
    print(f"Box Dimension: {d_B:.3f}")
    print("=" * 80)
    
    return {
        'num_nodes': stats.num_nodes,
        'num_edges': stats.num_edges,
        'avg_degree': stats.avg_degree,
        'clustering': C,
        'box_dim': d_B
    }


def compare_all_real_networks():
    """Compare all available real networks."""
    print("\n" + "=" * 80)
    print("REAL NETWORK COMPARISON")
    print("=" * 80)
    print()
    
    results = []
    
    # Facebook
    print("Loading Facebook...")
    fb_graph = load_edge_list_simple("./facebook_combined.txt")
    if fb_graph:
        fb_stats = compute_basic_stats(fb_graph)
        fb_C = compute_clustering_coefficient(fb_graph, sample_size=1000)
        fb_dB = compute_box_dimension_fast(fb_graph, max_box=10, num_samples=500)
        results.append({
            'name': 'Facebook',
            'nodes': fb_stats.num_nodes,
            'edges': fb_stats.num_edges,
            'avg_k': fb_stats.avg_degree,
            'C': fb_C,
            'd_B': fb_dB
        })
    
    # AS-Skitter
    print("\nLoading AS-Skitter (sampled)...")
    as_graph = load_large_network_sample("./as-skitter.txt", 
                                          sample_ratio=0.02, max_edges=30000)
    if as_graph:
        as_stats = compute_basic_stats(as_graph)
        as_C = compute_clustering_coefficient(as_graph, sample_size=300)
        as_dB = compute_box_dimension_fast(as_graph, max_box=5, num_samples=150)
        results.append({
            'name': 'Internet AS',
            'nodes': 1696415,  # Full size
            'edges': 11095298,
            'sample_nodes': as_stats.num_nodes,
            'avg_k': as_stats.avg_degree,
            'C': as_C,
            'd_B': as_dB
        })
    
    # Print comparison
    print("\n" + "=" * 80)
    print(f"{'Network':<15} {'Nodes':<12} {'<k>':<8} {'C':<8} {'d_B':<8}")
    print("-" * 80)
    for r in results:
        nodes_str = f"{r['nodes']:,}"
        if 'sample_nodes' in r:
            nodes_str += f"({r['sample_nodes']:,})"
        print(f"{r['name']:<15} {nodes_str:<12} {r['avg_k']:<8.2f} {r['C']:<8.3f} {r['d_B']:<8.3f}")
    print("=" * 80)
    
    return results


def load_edge_list_simple(filepath: str) -> Optional[Dict[int, Set[int]]]:
    """Simple edge list loader."""
    graph = {}
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        u = int(parts[0])
                        v = int(parts[1])
                        
                        if u not in graph:
                            graph[u] = set()
                        if v not in graph:
                            graph[v] = set()
                        
                        graph[u].add(v)
                        graph[v].add(u)
                    except ValueError:
                        continue
        return graph
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    # Analyze AS-Skitter
    analyze_as_skitter("./as-skitter.txt")
    
    # Compare with Facebook
    print("\n\n")
    compare_all_real_networks()
