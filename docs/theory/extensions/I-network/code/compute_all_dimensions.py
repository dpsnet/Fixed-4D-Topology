"""
Compute Dimensions for All Real Networks
========================================

Calculate box-counting and spectral dimensions for all generated networks.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import sys
import math
import time
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# Add parent directory to path
sys.path.append('..')
sys.path.append('../data')

from real_network_loader import RealNetworkGenerator, NetworkDatasetManager


@dataclass
class NetworkDimensionResult:
    """Dimension analysis result for a network."""
    network_name: str
    category: str
    num_nodes: int
    num_edges: int
    avg_degree: float
    clustering_coeff: float
    
    # Dimensions
    box_counting_dim: float
    correlation_dim: float
    
    # Computation info
    computation_time: float
    max_box_size: int


class NetworkDimensionAnalyzer:
    """Analyze dimensions of networks."""
    
    def __init__(self, graph: Dict[int, set]):
        self.graph = graph
        self.n = len(graph)
        self.adj_cache = {}
    
    def _get_neighbors(self, node: int) -> set:
        """Get neighbors with caching."""
        if node not in self.adj_cache:
            self.adj_cache[node] = self.graph[node]
        return self.adj_cache[node]
    
    def box_counting_dimension(self, max_box_size: int = None) -> float:
        """
        Calculate box-counting dimension using greedy covering.
        
        d_B = -lim log(N_B)/log(box_size)
        """
        if max_box_size is None:
            max_box_size = min(self.n // 4, 20)
        
        box_sizes = []
        num_boxes = []
        
        for box_size in range(1, max_box_size + 1):
            n_boxes = self._greedy_box_cover(box_size)
            if n_boxes > 0:
                box_sizes.append(box_size)
                num_boxes.append(n_boxes)
        
        if len(box_sizes) < 2:
            return 0.0
        
        # Log-log fit
        log_inv_size = [math.log(1.0 / s) for s in box_sizes]
        log_boxes = [math.log(n) for n in num_boxes]
        
        # Linear regression
        n = len(log_inv_size)
        sum_x = sum(log_inv_size)
        sum_y = sum(log_boxes)
        sum_xy = sum(x * y for x, y in zip(log_inv_size, log_boxes))
        sum_x2 = sum(x ** 2 for x in log_inv_size)
        
        if abs(n * sum_x2 - sum_x ** 2) < 1e-10:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def _greedy_box_cover(self, box_size: int) -> int:
        """Greedy algorithm for minimum box covering."""
        uncovered = set(self.graph.keys())
        num_boxes = 0
        
        while uncovered:
            # Choose node with maximum uncovered degree
            center = max(uncovered, 
                        key=lambda n: len(self._get_neighbors(n) & uncovered))
            
            # Find all nodes within distance box_size
            box = self._nodes_within_distance(center, box_size)
            
            uncovered -= box
            num_boxes += 1
        
        return num_boxes
    
    def _nodes_within_distance(self, start: int, max_dist: int) -> set:
        """Find all nodes within given distance."""
        distances = {start: 0}
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            if distances[node] >= max_dist:
                continue
            
            for neighbor in self._get_neighbors(node):
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    if distances[neighbor] <= max_dist:
                        queue.append(neighbor)
        
        return set(distances.keys())
    
    def correlation_dimension(self, num_samples: int = 500) -> float:
        """
        Calculate correlation dimension.
        
        d_2 = lim_{r->0} log(C(r)) / log(r)
        """
        nodes = list(self.graph.keys())
        if len(nodes) < 10:
            return 0.0
        
        # Sample random pairs
        distances = []
        for _ in range(num_samples):
            if len(nodes) < 2:
                break
            i, j = random.sample(nodes, 2)
            dist = self._shortest_path_length(i, j)
            if dist is not None and dist > 0:
                distances.append(dist)
        
        if not distances:
            return 0.0
        
        # Count pairs within radius r
        max_r = min(max(distances), 20)
        radii = list(range(1, max_r + 1))
        correlation_sum = []
        
        for r in radii:
            count = sum(1 for d in distances if d <= r)
            correlation_sum.append(max(count, 1))
        
        # Log-log fit
        log_r = [math.log(r) for r in radii]
        log_c = [math.log(c) for c in correlation_sum]
        
        n = len(log_r)
        if n < 2:
            return 0.0
        
        sum_x = sum(log_r)
        sum_y = sum(log_c)
        sum_xy = sum(x * y for x, y in zip(log_r, log_c))
        sum_x2 = sum(x ** 2 for x in log_r)
        
        if abs(n * sum_x2 - sum_x ** 2) < 1e-10:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def _shortest_path_length(self, i: int, j: int) -> int:
        """BFS shortest path."""
        if i == j:
            return 0
        
        distances = {i: 0}
        queue = [i]
        
        while queue:
            node = queue.pop(0)
            for neighbor in self._get_neighbors(node):
                if neighbor == j:
                    return distances[node] + 1
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return None
    
    def compute_all_metrics(self) -> Dict:
        """Compute all network metrics."""
        # Basic metrics
        degrees = [len(self._get_neighbors(n)) for n in self.graph.keys()]
        avg_degree = sum(degrees) / self.n if self.n > 0 else 0
        max_degree = max(degrees) if degrees else 0
        
        # Clustering coefficient
        def local_clustering(node):
            neighbors = list(self._get_neighbors(node))
            k = len(neighbors)
            if k < 2:
                return 0.0
            
            edges = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if n2 in self._get_neighbors(n1):
                        edges += 1
            
            return 2.0 * edges / (k * (k - 1))
        
        clustering = sum(local_clustering(n) for n in self.graph.keys()) / self.n if self.n > 0 else 0
        
        return {
            'num_nodes': self.n,
            'num_edges': sum(degrees) // 2,
            'avg_degree': avg_degree,
            'max_degree': max_degree,
            'clustering_coeff': clustering
        }


def analyze_all_networks():
    """Analyze dimensions for all network types."""
    print("=" * 70)
    print("I Direction: Computing Dimensions for All Networks")
    print("=" * 70)
    print()
    
    # Generate all networks at 20% scale
    print("Generating networks at 20% scale...")
    manager = NetworkDatasetManager()
    datasets = manager.generate_all_datasets(scale_factor=0.2, seed=42)
    
    print(f"Generated {len(datasets)} network datasets\n")
    
    results = []
    
    print("Analyzing dimensions...")
    print("-" * 70)
    print(f"{'Network':<25} {'Nodes':<8} {'d_B':<10} {'d_2':<10} {'Time':<8}")
    print("-" * 70)
    
    for name, data in datasets.items():
        network = data['network']
        profile = data['profile']
        
        start_time = time.time()
        
        # Create analyzer
        analyzer = NetworkDimensionAnalyzer(network)
        
        # Compute dimensions
        try:
            d_box = analyzer.box_counting_dimension(max_box_size=10)
            d_corr = analyzer.correlation_dimension(num_samples=300)
        except Exception as e:
            print(f"Error analyzing {name}: {e}")
            d_box = 0.0
            d_corr = 0.0
        
        elapsed = time.time() - start_time
        
        # Get basic metrics
        metrics = analyzer.compute_all_metrics()
        
        # Create result
        result = NetworkDimensionResult(
            network_name=name,
            category=profile.category,
            num_nodes=metrics['num_nodes'],
            num_edges=metrics['num_edges'],
            avg_degree=metrics['avg_degree'],
            clustering_coeff=metrics['clustering_coeff'],
            box_counting_dim=d_box,
            correlation_dim=d_corr,
            computation_time=elapsed,
            max_box_size=10
        )
        
        results.append(result)
        
        print(f"{name:<25} {metrics['num_nodes']:<8} {d_box:<10.3f} "
              f"{d_corr:<10.3f} {elapsed:<8.2f}")
    
    # Summary
    print("\n" + "=" * 70)
    print("Dimension Analysis Summary")
    print("=" * 70)
    print()
    
    # Group by category
    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)
    
    for cat, cat_results in categories.items():
        print(f"\n{cat.upper()}:")
        print("-" * 50)
        avg_d_box = sum(r.box_counting_dim for r in cat_results) / len(cat_results)
        avg_d_corr = sum(r.correlation_dim for r in cat_results) / len(cat_results)
        print(f"  Average box-counting dimension: {avg_d_box:.3f}")
        print(f"  Average correlation dimension:  {avg_d_corr:.3f}")
    
    # Save results
    output = {
        'analysis_type': 'network_dimension_computation',
        'scale_factor': 0.2,
        'num_networks': len(results),
        'results': [asdict(r) for r in results]
    }
    
    with open('network_dimensions.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 70)
    print("Results saved to: network_dimensions.json")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    import random
    results = analyze_all_networks()
