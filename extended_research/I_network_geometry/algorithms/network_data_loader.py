"""
Network Data Loader and Generator
=================================

Load real network datasets or generate synthetic networks for testing.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import random
import math
import json
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass


@dataclass
class NetworkMetrics:
    """Metrics for a complex network."""
    name: str
    num_nodes: int
    num_edges: int
    avg_degree: float
    clustering_coeff: float
    diameter: int
    effective_dimension: float = 0.0


class NetworkGenerator:
    """Generate various types of complex networks."""
    
    @staticmethod
    def erdos_renyi(n: int, p: float, seed: int = 42) -> Dict[int, Set[int]]:
        """
        Generate Erdős-Rényi random graph G(n, p).
        
        Args:
            n: Number of nodes
            p: Edge probability
            seed: Random seed
            
        Returns:
            Adjacency list representation
        """
        random.seed(seed)
        graph = {i: set() for i in range(n)}
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    graph[i].add(j)
                    graph[j].add(i)
        
        return graph
    
    @staticmethod
    def barabasi_albert(n: int, m: int, seed: int = 42) -> Dict[int, Set[int]]:
        """
        Generate Barabási-Albert scale-free network.
        
        Args:
            n: Number of nodes
            m: Number of edges to attach from new node
            seed: Random seed
            
        Returns:
            Adjacency list representation
        """
        random.seed(seed)
        graph = {i: set() for i in range(n)}
        
        # Start with m nodes forming a complete graph
        for i in range(m):
            for j in range(i + 1, m):
                graph[i].add(j)
                graph[j].add(i)
        
        # Add remaining nodes with preferential attachment
        degrees = [m - 1] * m  # Initial degrees
        
        for new_node in range(m, n):
            targets = set()
            total_degree = sum(degrees)
            
            while len(targets) < m and len(targets) < new_node:
                # Preferential attachment
                r = random.random() * total_degree
                cumsum = 0
                for node, deg in enumerate(degrees):
                    cumsum += deg
                    if cumsum >= r and node not in targets:
                        targets.add(node)
                        break
            
            # Add edges
            for target in targets:
                if target < new_node:
                    graph[new_node].add(target)
                    graph[target].add(new_node)
                    degrees[target] += 1
            
            degrees.append(m)
        
        return graph
    
    @staticmethod
    def watts_strogatz(n: int, k: int, p: float, seed: int = 42) -> Dict[int, Set[int]]:
        """
        Generate Watts-Strogatz small-world network.
        
        Args:
            n: Number of nodes
            k: Each node connected to k nearest neighbors
            p: Rewiring probability
            seed: Random seed
            
        Returns:
            Adjacency list representation
        """
        random.seed(seed)
        graph = {i: set() for i in range(n)}
        
        # Create ring lattice
        for i in range(n):
            for j in range(1, k // 2 + 1):
                neighbor = (i + j) % n
                graph[i].add(neighbor)
                graph[neighbor].add(i)
        
        # Rewire edges
        for i in range(n):
            neighbors = list(graph[i])
            for j in neighbors:
                if j > i:  # Only process each edge once
                    if random.random() < p:
                        # Rewire
                        graph[i].remove(j)
                        graph[j].remove(i)
                        
                        # Find new target
                        new_target = random.randint(0, n - 1)
                        while new_target == i or new_target in graph[i]:
                            new_target = random.randint(0, n - 1)
                        
                        graph[i].add(new_target)
                        graph[new_target].add(i)
        
        return graph
    
    @staticmethod
    def grid_2d(width: int, height: int) -> Dict[int, Set[int]]:
        """
        Generate 2D grid network.
        
        Args:
            width: Grid width
            height: Grid height
            
        Returns:
            Adjacency list representation
        """
        n = width * height
        graph = {i: set() for i in range(n)}
        
        def node_id(x: int, y: int) -> int:
            return y * width + x
        
        for y in range(height):
            for x in range(width):
                node = node_id(x, y)
                
                # Connect to neighbors
                neighbors = []
                if x > 0:
                    neighbors.append(node_id(x - 1, y))
                if x < width - 1:
                    neighbors.append(node_id(x + 1, y))
                if y > 0:
                    neighbors.append(node_id(x, y - 1))
                if y < height - 1:
                    neighbors.append(node_id(x, y + 1))
                
                graph[node] = set(neighbors)
        
        return graph


class NetworkAnalyzer:
    """Analyze network properties."""
    
    def __init__(self, graph: Dict[int, Set[int]]):
        self.graph = graph
        self.n = len(graph)
    
    def num_edges(self) -> int:
        """Count total number of edges."""
        return sum(len(neighbors) for neighbors in self.graph.values()) // 2
    
    def average_degree(self) -> float:
        """Calculate average degree."""
        return sum(len(neighbors) for neighbors in self.graph.values()) / self.n
    
    def degree_distribution(self) -> Dict[int, int]:
        """Calculate degree distribution."""
        dist = {}
        for neighbors in self.graph.values():
            d = len(neighbors)
            dist[d] = dist.get(d, 0) + 1
        return dist
    
    def clustering_coefficient(self) -> float:
        """
        Calculate average clustering coefficient.
        
        C = (1/N) * sum(C_i)
        where C_i = 2 * e_i / (k_i * (k_i - 1))
        """
        total_c = 0.0
        
        for node, neighbors in self.graph.items():
            k = len(neighbors)
            if k < 2:
                continue
            
            # Count edges between neighbors
            edges_between_neighbors = 0
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 < n2 and n2 in self.graph[n1]:
                        edges_between_neighbors += 1
            
            c_i = 2.0 * edges_between_neighbors / (k * (k - 1))
            total_c += c_i
        
        return total_c / self.n
    
    def bfs_distance(self, start: int) -> Dict[int, int]:
        """BFS to find shortest distances from start node."""
        distances = {start: 0}
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            for neighbor in self.graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return distances
    
    def diameter(self) -> int:
        """Calculate network diameter (longest shortest path)."""
        max_dist = 0
        
        for start in range(min(100, self.n)):  # Sample for large networks
            distances = self.bfs_distance(start)
            if distances:
                max_dist = max(max_dist, max(distances.values()))
        
        return max_dist
    
    def average_path_length(self) -> float:
        """Calculate average shortest path length."""
        total_length = 0
        num_paths = 0
        
        for start in range(min(50, self.n)):  # Sample for efficiency
            distances = self.bfs_distance(start)
            for end, dist in distances.items():
                if end > start:
                    total_length += dist
                    num_paths += 1
        
        return total_length / num_paths if num_paths > 0 else 0.0
    
    def get_metrics(self, name: str) -> NetworkMetrics:
        """Get comprehensive network metrics."""
        return NetworkMetrics(
            name=name,
            num_nodes=self.n,
            num_edges=self.num_edges(),
            avg_degree=self.average_degree(),
            clustering_coeff=self.clustering_coefficient(),
            diameter=self.diameter()
        )


class NetworkDimensionCalculator:
    """Calculate various dimensions of networks."""
    
    def __init__(self, graph: Dict[int, Set[int]]):
        self.graph = graph
        self.analyzer = NetworkAnalyzer(graph)
        self.n = len(graph)
    
    def box_covering_dimension(self, max_box_size: int = None) -> float:
        """
        Calculate box-counting dimension.
        
        d_B = -lim_{l->0} log(N_B(l)) / log(l)
        """
        if max_box_size is None:
            max_box_size = self.n // 4
        
        box_sizes = []
        num_boxes = []
        
        for l_B in range(1, min(max_box_size + 1, 50)):
            n_boxes = self._count_boxes_greedy(l_B)
            if n_boxes > 0:
                box_sizes.append(l_B)
                num_boxes.append(n_boxes)
        
        # Linear fit in log-log scale
        if len(box_sizes) < 2:
            return 0.0
        
        log_sizes = [math.log(1.0 / l) for l in box_sizes]
        log_boxes = [math.log(n) for n in num_boxes]
        
        # Simple linear fit
        n = len(log_sizes)
        sum_x = sum(log_sizes)
        sum_y = sum(log_boxes)
        sum_xy = sum(x * y for x, y in zip(log_sizes, log_boxes))
        sum_x2 = sum(x ** 2 for x in log_sizes)
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def _count_boxes_greedy(self, box_size: int) -> int:
        """Count minimum number of boxes of given size using greedy algorithm."""
        uncovered = set(self.graph.keys())
        num_boxes = 0
        
        while uncovered:
            # Pick a random uncovered node as box center
            center = random.choice(list(uncovered))
            
            # Find all nodes within distance box_size from center
            box = self._nodes_within_distance(center, box_size)
            
            uncovered -= box
            num_boxes += 1
        
        return num_boxes
    
    def _nodes_within_distance(self, start: int, max_dist: int) -> Set[int]:
        """Find all nodes within given distance from start."""
        distances = {start: 0}
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            if distances[node] >= max_dist:
                continue
            
            for neighbor in self.graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    if distances[neighbor] <= max_dist:
                        queue.append(neighbor)
        
        return set(distances.keys())
    
    def correlation_dimension(self, num_samples: int = 1000) -> float:
        """
        Calculate correlation dimension.
        
        d_2 = lim_{r->0} log(C(r)) / log(r)
        where C(r) is correlation sum.
        """
        # Sample random pairs
        nodes = list(self.graph.keys())
        distances = []
        
        for _ in range(num_samples):
            i, j = random.sample(nodes, 2)
            dist = self._shortest_path_length(i, j)
            if dist is not None:
                distances.append(dist)
        
        if not distances:
            return 0.0
        
        # Calculate correlation sum for different radii
        radii = range(1, max(distances) + 1)
        correlation_sums = []
        
        for r in radii:
            c_r = sum(1 for d in distances if d <= r) / len(distances)
            if c_r > 0:
                correlation_sums.append(c_r)
            else:
                correlation_sums.append(1e-10)
        
        # Linear fit
        log_r = [math.log(r) for r in radii]
        log_c = [math.log(c) for c in correlation_sums]
        
        n = len(log_r)
        sum_x = sum(log_r)
        sum_y = sum(log_c)
        sum_xy = sum(x * y for x, y in zip(log_r, log_c))
        sum_x2 = sum(x ** 2 for x in log_r)
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope
    
    def _shortest_path_length(self, i: int, j: int) -> Optional[int]:
        """Find shortest path length between two nodes."""
        if i == j:
            return 0
        
        distances = {i: 0}
        queue = [i]
        
        while queue:
            node = queue.pop(0)
            for neighbor in self.graph[node]:
                if neighbor == j:
                    return distances[node] + 1
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return None


def run_network_tests():
    """Run tests on various network types."""
    import math
    
    print("=" * 70)
    print("I Direction: Network Geometry Tests")
    print("=" * 70)
    
    networks = [
        ("ER (n=100, p=0.05)", NetworkGenerator.erdos_renyi(100, 0.05)),
        ("BA (n=100, m=2)", NetworkGenerator.barabasi_albert(100, 2)),
        ("WS (n=100, k=4, p=0.1)", NetworkGenerator.watts_strogatz(100, 4, 0.1)),
        ("Grid (10x10)", NetworkGenerator.grid_2d(10, 10)),
    ]
    
    print("\nNetwork Analysis:")
    print("-" * 70)
    print(f"{'Network':<25} {'Nodes':<8} {'Edges':<8} {'<k>':<8} {'C':<8} {'d_B':<8}")
    print("-" * 70)
    
    for name, graph in networks:
        analyzer = NetworkAnalyzer(graph)
        metrics = analyzer.get_metrics(name)
        
        dim_calc = NetworkDimensionCalculator(graph)
        d_B = dim_calc.box_covering_dimension(max_box_size=10)
        
        print(f"{name:<25} {metrics.num_nodes:<8} {metrics.num_edges:<8} "
              f"{metrics.avg_degree:<8.2f} {metrics.clustering_coeff:<8.3f} {d_B:<8.3f}")
    
    print("\n" + "=" * 70)
    print("I Direction Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    run_network_tests()
