"""
3D Percolation Simulation
=========================

Monte Carlo simulation of 3D percolation on cubic lattice.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import random
import math
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass


@dataclass
class Percolation3DResult:
    """Results from 3D percolation simulation."""
    probability: float
    has_percolation: bool
    largest_cluster_size: int
    num_clusters: int
    spanning_probability: float  # Probability of spanning cluster
    

class LatticePercolation3D:
    """Site and bond percolation on 3D cubic lattice."""
    
    def __init__(self, width: int, height: int, depth: int):
        """
        Initialize 3D lattice.
        
        Args:
            width: Lattice width (x)
            height: Lattice height (y)
            depth: Lattice depth (z)
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.size = width * height * depth
    
    def site_percolation(self, p: float, seed: int = None) -> List[bool]:
        """
        Generate 3D site percolation configuration.
        
        Args:
            p: Site occupation probability
            seed: Random seed
            
        Returns:
            List of occupied sites
        """
        if seed is not None:
            random.seed(seed)
        
        return [random.random() < p for _ in range(self.size)]
    
    def _index(self, x: int, y: int, z: int) -> int:
        """Convert 3D coordinates to 1D index."""
        return z * (self.width * self.height) + y * self.width + x
    
    def _coordinates(self, idx: int) -> Tuple[int, int, int]:
        """Convert 1D index to 3D coordinates."""
        z = idx // (self.width * self.height)
        remainder = idx % (self.width * self.height)
        y = remainder // self.width
        x = remainder % self.width
        return x, y, z
    
    def _get_neighbors(self, idx: int) -> List[int]:
        """Get 6-connected neighbors in 3D."""
        x, y, z = self._coordinates(idx)
        neighbors = []
        
        # 6 neighbors in 3D: +x, -x, +y, -y, +z, -z
        deltas = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        
        for dx, dy, dz in deltas:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < self.width and 0 <= ny < self.height and 0 <= nz < self.depth:
                neighbors.append(self._index(nx, ny, nz))
        
        return neighbors
    
    def find_clusters(self, occupied: List[bool]) -> Tuple[List[int], int]:
        """
        Find connected clusters using union-find (6-connectivity).
        
        Args:
            occupied: List of occupied sites
            
        Returns:
            (labels, num_clusters)
        """
        labels = [0] * self.size
        parent = list(range(self.size))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Union step
        for idx in range(self.size):
            if not occupied[idx]:
                continue
            
            for neighbor in self._get_neighbors(idx):
                if occupied[neighbor]:
                    union(idx, neighbor)
        
        # Label assignment
        label_map = {}
        current_label = 0
        
        for idx in range(self.size):
            if occupied[idx]:
                root = find(idx)
                if root not in label_map:
                    current_label += 1
                    label_map[root] = current_label
                labels[idx] = label_map[root]
        
        return labels, current_label
    
    def check_percolation(self, labels: List[int]) -> Tuple[bool, bool]:
        """
        Check for percolation in 3D.
        
        Checks:
        1. z-spanning (top to bottom)
        2. Any spanning direction
        
        Args:
            labels: Cluster labels
            
        Returns:
            (z_spanning, any_spanning)
        """
        # Get labels on top face (z=0) and bottom face (z=depth-1)
        top_labels = set()
        bottom_labels = set()
        
        for x in range(self.width):
            for y in range(self.height):
                top_idx = self._index(x, y, 0)
                bottom_idx = self._index(x, y, self.depth - 1)
                
                if labels[top_idx] > 0:
                    top_labels.add(labels[top_idx])
                if labels[bottom_idx] > 0:
                    bottom_labels.add(labels[bottom_idx])
        
        z_spanning = len(top_labels & bottom_labels) > 0
        
        # Check other directions
        x_spanning = False
        y_spanning = False
        
        # X-spanning
        left_labels = set()
        right_labels = set()
        for y in range(self.height):
            for z in range(self.depth):
                left_idx = self._index(0, y, z)
                right_idx = self._index(self.width - 1, y, z)
                if labels[left_idx] > 0:
                    left_labels.add(labels[left_idx])
                if labels[right_idx] > 0:
                    right_labels.add(labels[right_idx])
        x_spanning = len(left_labels & right_labels) > 0
        
        # Y-spanning
        front_labels = set()
        back_labels = set()
        for x in range(self.width):
            for z in range(self.depth):
                front_idx = self._index(x, 0, z)
                back_idx = self._index(x, self.height - 1, z)
                if labels[front_idx] > 0:
                    front_labels.add(labels[front_idx])
                if labels[back_idx] > 0:
                    back_labels.add(labels[back_idx])
        y_spanning = len(front_labels & back_labels) > 0
        
        any_spanning = z_spanning or x_spanning or y_spanning
        
        return z_spanning, any_spanning
    
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
        # Extract largest cluster sites
        cluster_sites = []
        for idx in range(self.size):
            if labels[idx] == max_cluster_label:
                cluster_sites.append(self._coordinates(idx))
        
        if len(cluster_sites) < 10:
            return 0.0
        
        # Box counting in 3D
        box_sizes = []
        num_boxes = []
        
        for box_size in [2, 4, 8]:
            if box_size > min(self.width, self.height, self.depth):
                break
            
            boxes = set()
            for (x, y, z) in cluster_sites:
                box_x = x // box_size
                box_y = y // box_size
                box_z = z // box_size
                boxes.add((box_x, box_y, box_z))
            
            box_sizes.append(box_size)
            num_boxes.append(len(boxes))
        
        if len(box_sizes) < 2:
            return 0.0
        
        # Linear fit in log-log
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


class Percolation3DAnalyzer:
    """Analyze 3D percolation properties."""
    
    def __init__(self, width: int, height: int, depth: int):
        self.width = width
        self.height = height
        self.depth = depth
        self.lattice = LatticePercolation3D(width, height, depth)
    
    def find_critical_probability(self, num_samples: int = 50,
                                  p_min: float = 0.1,
                                  p_max: float = 0.5) -> float:
        """
        Estimate 3D percolation threshold.
        
        Args:
            num_samples: Number of samples per probability
            p_min, p_max: Search range
            
        Returns:
            Estimated critical probability
        """
        p_low, p_high = p_min, p_max
        
        # Binary search for spanning probability = 0.5
        for iteration in range(8):
            p_mid = (p_low + p_high) / 2
            
            spanning_count = 0
            for seed in range(num_samples):
                occupied = self.lattice.site_percolation(p_mid, seed)
                labels, _ = self.lattice.find_clusters(occupied)
                _, any_spanning = self.lattice.check_percolation(labels)
                
                if any_spanning:
                    spanning_count += 1
            
            fraction = spanning_count / num_samples
            print(f"  Iter {iteration+1}: p={p_mid:.4f}, spanning={fraction:.2f}")
            
            if fraction > 0.5:
                p_high = p_mid
            else:
                p_low = p_mid
        
        return (p_low + p_high) / 2
    
    def spanning_probability_curve(self, p_values: List[float],
                                   num_samples: int = 100) -> Dict[float, float]:
        """
        Calculate spanning probability as function of p.
        
        Args:
            p_values: List of probabilities to test
            num_samples: Samples per probability
            
        Returns:
            Dictionary of p -> spanning_probability
        """
        results = {}
        
        for p in p_values:
            spanning_count = 0
            for seed in range(num_samples):
                occupied = self.lattice.site_percolation(p, seed)
                labels, _ = self.lattice.find_clusters(occupied)
                _, any_spanning = self.lattice.check_percolation(labels)
                if any_spanning:
                    spanning_count += 1
            
            results[p] = spanning_count / num_samples
        
        return results


def run_3d_percolation_tests():
    """Run 3D percolation tests."""
    print("=" * 70)
    print("J Direction: 3D Percolation Tests")
    print("=" * 70)
    
    # Test 1: Critical probability estimation
    print("\n[1] Estimating 3D Percolation Threshold")
    print("-" * 50)
    print("System: 20x20x20 cubic lattice")
    print()
    
    analyzer = Percolation3DAnalyzer(20, 20, 20)
    p_c = analyzer.find_critical_probability(num_samples=30)
    
    print(f"\nEstimated p_c (3D): {p_c:.4f}")
    print(f"Theoretical p_c (3D site): ~0.3116")
    print(f"Error: {abs(p_c - 0.3116) / 0.3116 * 100:.2f}%")
    
    # Test 2: Spanning probability curve
    print("\n[2] Spanning Probability vs Occupation Probability")
    print("-" * 50)
    
    p_values = [0.20, 0.25, 0.28, 0.30, 0.31, 0.32, 0.35, 0.40]
    curve = analyzer.spanning_probability_curve(p_values, num_samples=50)
    
    print(f"{'p':<8} {'P_span':<8}")
    print("-" * 20)
    for p in sorted(curve.keys()):
        print(f"{p:<8.2f} {curve[p]:<8.3f}")
    
    # Test 3: Fractal dimension at criticality
    print("\n[3] Fractal Dimension at Criticality (3D)")
    print("-" * 50)
    
    p_c_3d = 0.3116
    occupied = analyzer.lattice.site_percolation(p_c_3d, seed=42)
    labels, num_clusters = analyzer.lattice.find_clusters(occupied)
    
    from collections import Counter
    cluster_sizes = Counter(labels)
    if 0 in cluster_sizes:
        del cluster_sizes[0]
    
    if cluster_sizes:
        largest_label = cluster_sizes.most_common(1)[0][0]
        d_f = analyzer.lattice.calculate_fractal_dimension(
            occupied, labels, largest_label
        )
        
        print(f"Fractal dimension d_f: {d_f:.4f}")
        print(f"Theoretical (3D percolation): ~2.52")
    else:
        print("No clusters found")
    
    # Test 4: Comparison with 2D
    print("\n[4] 2D vs 3D Percolation Comparison")
    print("-" * 50)
    
    comparison = {
        'Property': ['p_c (site)', 'Fractal dim', 'Upper critical dim'],
        '2D': ['0.5927', '1.896', '6'],
        '3D': ['0.3116', '2.52', '6']
    }
    
    print(f"{'Property':<25} {'2D':<12} {'3D':<12}")
    print("-" * 50)
    for i, prop in enumerate(comparison['Property']):
        print(f"{prop:<25} {comparison['2D'][i]:<12} {comparison['3D'][i]:<12}")
    
    print("\n" + "=" * 70)
    print("3D Percolation Tests Complete")
    print("=" * 70)


if __name__ == "__main__":
    run_3d_percolation_tests()
