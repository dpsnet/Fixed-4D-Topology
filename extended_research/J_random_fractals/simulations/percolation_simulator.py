"""
Percolation Simulator
=====================

Monte Carlo simulation of percolation on 2D and 3D lattices.
Calculates percolation thresholds and fractal dimensions.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import random
import math
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass


@dataclass
class PercolationResult:
    """Results from a percolation simulation."""
    probability: float
    has_percolation: bool
    largest_cluster_size: int
    num_clusters: int
    fractal_dimension: float
    correlation_length: float


class LatticePercolation:
    """Site and bond percolation on regular lattices."""
    
    def __init__(self, width: int, height: int, dimension: int = 2):
        """
        Initialize lattice.
        
        Args:
            width: Lattice width
            height: Lattice height
            dimension: Lattice dimension (2 or 3)
        """
        self.width = width
        self.height = height
        self.dimension = dimension
        self.size = width * height
        
        if dimension == 3:
            self.depth = height
            self.size *= height
    
    def site_percolation(self, p: float, seed: int = None) -> List[bool]:
        """
        Generate site percolation configuration.
        
        Args:
            p: Site occupation probability
            seed: Random seed
            
        Returns:
            List of occupied sites (True = occupied)
        """
        if seed is not None:
            random.seed(seed)
        
        return [random.random() < p for _ in range(self.size)]
    
    def bond_percolation(self, p: float, seed: int = None) -> Dict[Tuple[int, int], bool]:
        """
        Generate bond percolation configuration.
        
        Args:
            p: Bond occupation probability
            seed: Random seed
            
        Returns:
            Dictionary of bonds (True = present)
        """
        if seed is not None:
            random.seed(seed)
        
        bonds = {}
        
        for i in range(self.height):
            for j in range(self.width):
                node = i * self.width + j
                
                # Right neighbor
                if j < self.width - 1:
                    right_node = i * self.width + (j + 1)
                    bonds[(node, right_node)] = random.random() < p
                
                # Bottom neighbor
                if i < self.height - 1:
                    bottom_node = (i + 1) * self.width + j
                    bonds[(node, bottom_node)] = random.random() < p
        
        return bonds
    
    def find_clusters(self, occupied: List[bool]) -> Tuple[List[int], int]:
        """
        Find connected clusters using Hoshen-Kopelman algorithm.
        
        Args:
            occupied: List of occupied sites
            
        Returns:
            (labels, num_clusters)
        """
        labels = [0] * self.size
        label_counter = 0
        
        # Union-Find structure
        parent = list(range(self.size + 1))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        for i in range(self.height):
            for j in range(self.width):
                idx = i * self.width + j
                
                if not occupied[idx]:
                    continue
                
                # Check left and top neighbors
                neighbors = []
                
                # Left
                if j > 0 and occupied[idx - 1]:
                    neighbors.append(idx - 1)
                
                # Top
                if i > 0 and occupied[idx - self.width]:
                    neighbors.append(idx - self.width)
                
                if not neighbors:
                    label_counter += 1
                    labels[idx] = label_counter
                else:
                    # Assign smallest label
                    min_label = min(labels[n] for n in neighbors)
                    labels[idx] = min_label
                    
                    # Union all neighbor labels
                    for n in neighbors:
                        union(labels[n], min_label)
        
        # Second pass: flatten labels
        for i in range(self.size):
            if occupied[i]:
                labels[i] = find(labels[i])
        
        # Relabel to consecutive integers
        unique_labels = sorted(set(labels[i] for i in range(self.size) if occupied[i]))
        label_map = {old: new + 1 for new, old in enumerate(unique_labels)}
        
        for i in range(self.size):
            if occupied[i]:
                labels[i] = label_map[labels[i]]
        
        return labels, len(unique_labels)
    
    def check_percolation(self, labels: List[int]) -> bool:
        """
        Check if percolation occurs (top-to-bottom connectivity).
        
        Args:
            labels: Cluster labels
            
        Returns:
            True if percolation occurs
        """
        # Get labels on top and bottom edges
        top_labels = set(labels[j] for j in range(self.width) if labels[j] > 0)
        bottom_labels = set(labels[(self.height - 1) * self.width + j] 
                          for j in range(self.width) if labels[(self.height - 1) * self.width + j] > 0)
        
        return len(top_labels & bottom_labels) > 0
    
    def largest_cluster_size(self, labels: List[int]) -> int:
        """Find size of largest cluster."""
        from collections import Counter
        cluster_sizes = Counter(labels)
        if 0 in cluster_sizes:
            del cluster_sizes[0]
        return max(cluster_sizes.values()) if cluster_sizes else 0
    
    def calculate_fractal_dimension(self, occupied: List[bool], 
                                   labels: List[int],
                                   max_cluster_label: int) -> float:
        """
        Calculate fractal dimension of largest cluster using box counting.
        
        Args:
            occupied: Occupied sites
            labels: Cluster labels
            max_cluster_label: Label of largest cluster
            
        Returns:
            Fractal dimension
        """
        # Extract largest cluster coordinates
        cluster_sites = []
        for i in range(self.height):
            for j in range(self.width):
                idx = i * self.width + j
                if labels[idx] == max_cluster_label:
                    cluster_sites.append((i, j))
        
        if len(cluster_sites) < 10:
            return 0.0
        
        # Box counting
        box_sizes = []
        num_boxes = []
        
        for box_size in [2, 4, 8, 16, 32]:
            if box_size > self.width or box_size > self.height:
                break
            
            boxes = set()
            for (i, j) in cluster_sites:
                box_i = i // box_size
                box_j = j // box_size
                boxes.add((box_i, box_j))
            
            box_sizes.append(box_size)
            num_boxes.append(len(boxes))
        
        if len(box_sizes) < 2:
            return 0.0
        
        # Linear fit
        log_sizes = [math.log(1.0 / s) for s in box_sizes]
        log_boxes = [math.log(n) for n in num_boxes]
        
        n = len(log_sizes)
        sum_x = sum(log_sizes)
        sum_y = sum(log_boxes)
        sum_xy = sum(x * y for x, y in zip(log_sizes, log_boxes))
        sum_x2 = sum(x ** 2 for x in log_sizes)
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope


class RandomWalkOnPercolation:
    """Simulate random walks on percolation clusters."""
    
    def __init__(self, lattice: LatticePercolation, labels: List[int],
                 cluster_label: int):
        """
        Initialize random walk on specific cluster.
        
        Args:
            lattice: LatticePercolation object
            labels: Cluster labels
            cluster_label: Label of cluster to walk on
        """
        self.lattice = lattice
        self.labels = labels
        self.cluster_label = cluster_label
        
        # Get cluster sites
        self.cluster_sites = []
        for i in range(lattice.height):
            for j in range(lattice.width):
                idx = i * lattice.width + j
                if labels[idx] == cluster_label:
                    self.cluster_sites.append((i, j))
    
    def random_walk(self, steps: int, start_pos: Tuple[int, int] = None,
                   seed: int = None) -> List[Tuple[int, int]]:
        """
        Perform random walk on cluster.
        
        Args:
            steps: Number of steps
            start_pos: Starting position (random if None)
            seed: Random seed
            
        Returns:
            List of positions
        """
        if seed is not None:
            random.seed(seed)
        
        if start_pos is None:
            start_pos = random.choice(self.cluster_sites)
        
        positions = [start_pos]
        current = start_pos
        
        for _ in range(steps):
            # Get valid neighbors
            i, j = current
            neighbors = []
            
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.lattice.height and 0 <= nj < self.lattice.width:
                    idx = ni * self.lattice.width + nj
                    if self.labels[idx] == self.cluster_label:
                        neighbors.append((ni, nj))
            
            if neighbors:
                current = random.choice(neighbors)
            
            positions.append(current)
        
        return positions
    
    def mean_square_displacement(self, num_walks: int = 100,
                                 max_steps: int = 1000) -> List[float]:
        """
        Calculate mean square displacement.
        
        Args:
            num_walks: Number of random walks to average
            max_steps: Maximum number of steps
            
        Returns:
            MSD as function of time
        """
        msd = [0.0] * (max_steps + 1)
        
        for walk_id in range(num_walks):
            start = random.choice(self.cluster_sites)
            positions = self.random_walk(max_steps, start, seed=walk_id)
            
            x0, y0 = start
            for t, (x, y) in enumerate(positions):
                msd[t] += (x - x0) ** 2 + (y - y0) ** 2
        
        return [m / num_walks for m in msd]
    
    def calculate_walk_dimension(self, msd: List[float], 
                                 t_range: Tuple[int, int] = (10, 100)) -> float:
        """
        Calculate walk dimension from MSD.
        
        d_w = 2 / slope where MSD ~ t^(2/d_w)
        
        Args:
            msd: Mean square displacement
            t_range: Range of times to fit
            
        Returns:
            Walk dimension
        """
        t_start, t_end = t_range
        t_vals = list(range(t_start, min(t_end, len(msd))))
        
        log_t = [math.log(t) for t in t_vals]
        log_msd = [math.log(max(msd[t], 1e-10)) for t in t_vals]
        
        # Linear fit
        n = len(log_t)
        sum_x = sum(log_t)
        sum_y = sum(log_msd)
        sum_xy = sum(x * y for x, y in zip(log_t, log_msd))
        sum_x2 = sum(x ** 2 for x in log_t)
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        # d_w = 2 / slope where slope = 2 / d_w
        if abs(slope) < 1e-10:
            return float('inf')
        
        return 2.0 / slope


class PercolationAnalyzer:
    """Analyze percolation properties across probabilities."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.lattice = LatticePercolation(width, height)
    
    def find_critical_probability(self, num_samples: int = 100,
                                  p_min: float = 0.4,
                                  p_max: float = 0.8) -> float:
        """
        Estimate percolation threshold using binary search.
        
        Args:
            num_samples: Number of samples per probability
            p_min, p_max: Search range
            
        Returns:
            Estimated critical probability
        """
        p_low, p_high = p_min, p_max
        
        for _ in range(10):  # 10 iterations for precision
            p_mid = (p_low + p_high) / 2
            
            percolation_count = 0
            for seed in range(num_samples):
                occupied = self.lattice.site_percolation(p_mid, seed)
                labels, _ = self.lattice.find_clusters(occupied)
                
                if self.lattice.check_percolation(labels):
                    percolation_count += 1
            
            fraction = percolation_count / num_samples
            
            if fraction > 0.5:
                p_high = p_mid
            else:
                p_low = p_mid
        
        return (p_low + p_high) / 2
    
    def cluster_size_distribution(self, p: float, num_samples: int = 100) -> Dict[int, float]:
        """
        Calculate cluster size distribution.
        
        Args:
            p: Occupation probability
            num_samples: Number of samples
            
        Returns:
            Dictionary of size -> frequency
        """
        from collections import Counter
        
        size_counter = Counter()
        
        for seed in range(num_samples):
            occupied = self.lattice.site_percolation(p, seed)
            labels, num_clusters = self.lattice.find_clusters(occupied)
            
            cluster_sizes = Counter(labels)
            if 0 in cluster_sizes:
                del cluster_sizes[0]
            
            size_counter.update(cluster_sizes.values())
        
        # Normalize
        total = sum(size_counter.values())
        return {size: count / total for size, count in size_counter.items()}


def run_percolation_tests():
    """Run comprehensive percolation tests."""
    print("=" * 70)
    print("J Direction: Percolation and Random Walk Tests")
    print("=" * 70)
    
    # Test 1: Find critical probability
    print("\n[1] Estimating Percolation Threshold (2D)")
    print("-" * 50)
    
    analyzer = PercolationAnalyzer(50, 50)
    p_c = analyzer.find_critical_probability(num_samples=50)
    
    print(f"Estimated p_c: {p_c:.4f}")
    print(f"Theoretical p_c (2D): 0.5927")
    print(f"Error: {abs(p_c - 0.5927) / 0.5927 * 100:.2f}%")
    
    # Test 2: Fractal dimension at criticality
    print("\n[2] Fractal Dimension at Criticality")
    print("-" * 50)
    
    lattice = LatticePercolation(100, 100)
    occupied = lattice.site_percolation(0.5927, seed=42)
    labels, num_clusters = lattice.find_clusters(occupied)
    
    # Find largest cluster
    from collections import Counter
    cluster_sizes = Counter(labels)
    if 0 in cluster_sizes:
        del cluster_sizes[0]
    largest_label = cluster_sizes.most_common(1)[0][0]
    
    d_f = lattice.calculate_fractal_dimension(occupied, labels, largest_label)
    
    print(f"Fractal dimension d_f: {d_f:.4f}")
    print(f"Theoretical (2D percolation): 91/48 ≈ 1.8958")
    
    # Test 3: Random walk on percolation cluster
    print("\n[3] Random Walk on Percolation Cluster")
    print("-" * 50)
    
    rw = RandomWalkOnPercolation(lattice, labels, largest_label)
    msd = rw.mean_square_displacement(num_walks=50, max_steps=500)
    d_w = rw.calculate_walk_dimension(msd, t_range=(50, 400))
    
    print(f"Walk dimension d_w: {d_w:.4f}")
    print(f"Theoretical (2D percolation): ~2.87")
    
    # Test 4: Alexander-Orbach relation
    print("\n[4] Alexander-Orbach Relation")
    print("-" * 50)
    
    if d_f > 0 and d_w > 0:
        d_s = 2 * d_f / d_w
        print(f"Spectral dimension d_s = 2*d_f/d_w: {d_s:.4f}")
        print(f"Alexander-Orbach prediction (d≥2): 4/3 ≈ 1.333")
    
    print("\n" + "=" * 70)
    print("J Direction Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    run_percolation_tests()
