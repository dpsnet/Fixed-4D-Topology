#!/usr/bin/env python3
"""
3D Percolation Simulation (Pure Python)
======================================

Site percolation on cubic lattice.
Computes cluster statistics and effective dimensions.
"""

import random
import math
import json
from typing import List, Tuple, Set, Dict
from collections import deque


class Percolation3D:
    """
    3D site percolation simulation.
    """
    
    def __init__(self, L: int = 30):
        """
        Initialize 3D lattice.
        
        Args:
            L: Linear size (L x L x L lattice)
        """
        self.L = L
        self.N = L ** 3
        self.lattice = [[[0 for _ in range(L)] for _ in range(L)] for _ in range(L)]
        self.occupation = [[[False for _ in range(L)] for _ in range(L)] for _ in range(L)]
        
    def generate(self, p: float):
        """
        Generate percolation configuration.
        
        Args:
            p: Occupation probability
        """
        self.p = p
        for x in range(self.L):
            for y in range(self.L):
                for z in range(self.L):
                    self.occupation[x][y][z] = random.random() < p
    
    def find_clusters(self) -> List[Set[Tuple[int, int, int]]]:
        """
        Identify all clusters using Hoshen-Kopelman algorithm (simplified).
        
        Returns:
            List of clusters (each cluster is a set of occupied sites)
        """
        visited = [[[False for _ in range(self.L)] for _ in range(self.L)] for _ in range(self.L)]
        clusters = []
        
        for x in range(self.L):
            for y in range(self.L):
                for z in range(self.L):
                    if self.occupation[x][y][z] and not visited[x][y][z]:
                        # BFS to find cluster
                        cluster = self._bfs_cluster(x, y, z, visited)
                        clusters.append(cluster)
        
        return clusters
    
    def _bfs_cluster(self, x0: int, y0: int, z0: int, visited: List) -> Set[Tuple[int, int, int]]:
        """BFS to find all sites in a cluster."""
        cluster = set()
        queue = deque([(x0, y0, z0)])
        visited[x0][y0][z0] = True
        
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        
        while queue:
            x, y, z = queue.popleft()
            cluster.add((x, y, z))
            
            for dx, dy, dz in directions:
                nx, ny, nz = x + dx, y + dy, z + dz
                if (0 <= nx < self.L and 0 <= ny < self.L and 0 <= nz < self.L and
                    self.occupation[nx][ny][nz] and not visited[nx][ny][nz]):
                    visited[nx][ny][nz] = True
                    queue.append((nx, ny, nz))
        
        return cluster
    
    def has_spanning_cluster(self) -> bool:
        """
        Check if there's a cluster spanning from z=0 to z=L-1.
        """
        clusters = self.find_clusters()
        
        for cluster in clusters:
            z_values = [site[2] for site in cluster]
            if min(z_values) == 0 and max(z_values) == self.L - 1:
                return True
        
        return False
    
    def box_counting_dimension(self, cluster: Set[Tuple[int, int, int]]) -> float:
        """
        Estimate fractal dimension using box counting.
        
        Args:
            cluster: Set of sites in cluster
            
        Returns:
            Estimated fractal dimension
        """
        if len(cluster) < 10:
            return 0.0
        
        # Box sizes
        box_sizes = [2, 3, 4, 5, 6]
        counts = []
        
        for box_size in box_sizes:
            # Count boxes needed to cover cluster
            boxes = set()
            for x, y, z in cluster:
                bx, by, bz = x // box_size, y // box_size, z // box_size
                boxes.add((bx, by, bz))
            counts.append(len(boxes))
        
        # Linear regression on log-log plot
        log_sizes = [math.log(1.0 / s) for s in box_sizes]
        log_counts = [math.log(c) if c > 0 else 0 for c in counts]
        
        # Simple linear fit
        n = len(log_sizes)
        if n < 2:
            return 0.0
        
        mean_x = sum(log_sizes) / n
        mean_y = sum(log_counts) / n
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_sizes, log_counts))
        denominator = sum((x - mean_x) ** 2 for x in log_sizes)
        
        if abs(denominator) < 1e-10:
            return 0.0
        
        dimension = numerator / denominator
        return dimension
    
    def analyze(self) -> Dict:
        """
        Full analysis of percolation configuration.
        
        Returns:
            Dictionary with statistics
        """
        clusters = self.find_clusters()
        
        if not clusters:
            return {
                'num_clusters': 0,
                'max_cluster_size': 0,
                'max_cluster_dim': 0.0,
                'has_spanning': False,
                'p': self.p
            }
        
        # Find largest cluster
        largest = max(clusters, key=len)
        
        # Compute dimension
        dim = self.box_counting_dimension(largest)
        
        return {
            'num_clusters': len(clusters),
            'max_cluster_size': len(largest),
            'max_cluster_dim': dim,
            'has_spanning': self.has_spanning_cluster(),
            'p': self.p,
            'avg_cluster_size': sum(len(c) for c in clusters) / len(clusters)
        }


def find_critical_point(L: int = 30, num_samples: int = 100) -> Dict:
    """
    Estimate critical point by finding where spanning probability = 0.5.
    
    Args:
        L: Lattice size
        num_samples: Number of samples per p value
        
    Returns:
        Results dictionary
    """
    print(f"Finding critical point for L={L}")
    print(f"Samples per p: {num_samples}")
    print("-" * 50)
    
    # Test different p values
    p_values = [0.28, 0.30, 0.31, 0.312, 0.315, 0.32, 0.33, 0.35]
    results = []
    
    for p in p_values:
        spanning_count = 0
        dimensions = []
        
        for sample in range(num_samples):
            perc = Percolation3D(L)
            perc.generate(p)
            
            if perc.has_spanning_cluster():
                spanning_count += 1
            
            # Analyze largest cluster
            clusters = perc.find_clusters()
            if clusters:
                largest = max(clusters, key=len)
                if len(largest) > 100:  # Only for substantial clusters
                    dim = perc.box_counting_dimension(largest)
                    if dim > 0:
                        dimensions.append(dim)
        
        spanning_prob = spanning_count / num_samples
        avg_dim = sum(dimensions) / len(dimensions) if dimensions else 0
        
        results.append({
            'p': p,
            'spanning_prob': spanning_prob,
            'avg_dimension': avg_dim,
            'num_samples': num_samples
        })
        
        print(f"p={p:.4f}: Spanning={spanning_prob:.2%}, Avg dim={avg_dim:.3f}")
    
    # Find p where spanning_prob ≈ 0.5
    closest = min(results, key=lambda r: abs(r['spanning_prob'] - 0.5))
    
    print("\n" + "=" * 50)
    print(f"Estimated critical point: p_c ≈ {closest['p']:.4f}")
    print(f"Literature value (3D site): p_c ≈ 0.3116")
    print(f"Fractal dimension at p_c: d_f ≈ {closest['avg_dimension']:.3f}")
    print(f"Literature value: d_f ≈ 2.52")
    print("=" * 50)
    
    return {
        'L': L,
        'num_samples': num_samples,
        'p_c_estimate': closest['p'],
        'results': results
    }


def dimension_vs_p(L: int = 30, num_samples: int = 50):
    """
    Study how fractal dimension changes with occupation probability.
    """
    print("\n" + "=" * 60)
    print("Dimension vs Occupation Probability")
    print("=" * 60)
    
    p_values = [0.25, 0.28, 0.30, 0.31, 0.3116, 0.32, 0.35, 0.40]
    
    results = []
    for p in p_values:
        dimensions = []
        
        for _ in range(num_samples):
            perc = Percolation3D(L)
            perc.generate(p)
            
            clusters = perc.find_clusters()
            if clusters:
                largest = max(clusters, key=len)
                if len(largest) > 50:
                    dim = perc.box_counting_dimension(largest)
                    if dim > 0:
                        dimensions.append(dim)
        
        avg_dim = sum(dimensions) / len(dimensions) if dimensions else 0
        std_dim = math.sqrt(sum((d - avg_dim)**2 for d in dimensions) / len(dimensions)) if dimensions else 0
        
        results.append({
            'p': p,
            'dimension': avg_dim,
            'std': std_dim
        })
        
        status = "CRITICAL" if abs(p - 0.3116) < 0.01 else ""
        print(f"p={p:.4f}: d_f={avg_dim:.3f} ± {std_dim:.3f} {status}")
    
    return results


def finite_size_scaling():
    """
    Study how results depend on system size.
    """
    print("\n" + "=" * 60)
    print("Finite Size Scaling Analysis")
    print("=" * 60)
    
    sizes = [10, 15, 20, 25, 30]
    p_c_values = []
    
    for L in sizes:
        print(f"\nL = {L}:")
        result = find_critical_point(L=L, num_samples=50)
        p_c_values.append(result['p_c_estimate'])
    
    print("\n" + "-" * 60)
    print("Finite Size Scaling Summary:")
    for L, pc in zip(sizes, p_c_values):
        print(f"  L={L:2d}: p_c ≈ {pc:.4f}")
    
    # Extrapolate to L -> infinity
    # p_c(L) = p_c(inf) + a * L^(-1/nu)
    # Simple extrapolation: use largest L
    print(f"\nExtrapolated p_c(∞) ≈ {p_c_values[-1]:.4f}")
    print("(Literature: 0.3116)")


if __name__ == '__main__':
    print("3D Percolation Simulation (Pure Python)")
    print("=" * 60)
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # 1. Find critical point
    result = find_critical_point(L=20, num_samples=50)
    
    # Save results
    with open('percolation_critical_3d.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\nResults saved to percolation_critical_3d.json")
    
    # 2. Dimension vs p
    dim_results = dimension_vs_p(L=20, num_samples=30)
    
    with open('percolation_dimension_vs_p.json', 'w') as f:
        json.dump(dim_results, f, indent=2)
    
    print("\nDimension data saved to percolation_dimension_vs_p.json")
    
    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("Note: For higher precision, increase L and num_samples")
    print("      (but will take longer to run)")
    print("=" * 60)
