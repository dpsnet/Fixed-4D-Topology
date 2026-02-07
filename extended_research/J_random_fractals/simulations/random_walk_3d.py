"""
3D Random Walk on Percolation Clusters
======================================

Random walk simulations on 3D percolation clusters to compute
walk dimension and spectral dimension.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import sys
import math
import random
import time
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass

sys.path.append('.')
from percolation_3d import LatticePercolation3D


@dataclass
class RandomWalkResult:
    """Results from random walk simulation."""
    num_steps: int
    num_walkers: int
    msd_values: List[float]
    walk_dimension: float
    spectral_dimension: float
    computation_time: float


class RandomWalk3D:
    """Random walk on 3D percolation cluster."""
    
    def __init__(self, lattice: LatticePercolation3D, 
                 occupied: List[bool], labels: List[int],
                 target_cluster: int):
        """
        Initialize random walk on specific cluster.
        
        Args:
            lattice: 3D lattice
            occupied: Occupied sites
            labels: Cluster labels
            target_cluster: Label of cluster to walk on
        """
        self.lattice = lattice
        self.occupied = occupied
        self.labels = labels
        self.target_cluster = target_cluster
        
        # Extract cluster sites
        self.cluster_sites = []
        for idx in range(lattice.size):
            if labels[idx] == target_cluster:
                self.cluster_sites.append(lattice._coordinates(idx))
        
        # Create set for fast lookup
        self.cluster_set = set(self.cluster_sites)
    
    def _get_neighbors_on_cluster(self, pos: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Get neighbors on the same cluster."""
        x, y, z = pos
        neighbors = []
        
        # 6 neighbors in 3D
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in self.cluster_set:
                neighbors.append((nx, ny, nz))
        
        return neighbors
    
    def single_walk(self, start_pos: Tuple[int, int, int],
                   num_steps: int, seed: int = None) -> List[Tuple[int, int, int]]:
        """
        Perform single random walk.
        
        Args:
            start_pos: Starting position
            num_steps: Number of steps
            seed: Random seed
            
        Returns:
            List of positions
        """
        if seed is not None:
            random.seed(seed)
        
        positions = [start_pos]
        current = start_pos
        
        for _ in range(num_steps):
            neighbors = self._get_neighbors_on_cluster(current)
            
            if neighbors:
                current = random.choice(neighbors)
            # If no neighbors, stay in place (dead end)
            
            positions.append(current)
        
        return positions
    
    def compute_msd(self, num_walkers: int = 100,
                   max_steps: int = 1000) -> List[float]:
        """
        Compute mean square displacement.
        
        Args:
            num_walkers: Number of independent walkers
            max_steps: Maximum number of steps
            
        Returns:
            MSD as function of time
        """
        if not self.cluster_sites:
            return [0.0] * (max_steps + 1)
        
        msd = [0.0] * (max_steps + 1)
        
        for walker_id in range(num_walkers):
            # Random starting position on cluster
            start = random.choice(self.cluster_sites)
            
            # Perform walk
            positions = self.single_walk(start, max_steps, seed=walker_id)
            
            # Compute MSD
            x0, y0, z0 = start
            for t, (x, y, z) in enumerate(positions):
                dist_sq = (x - x0)**2 + (y - y0)**2 + (z - z0)**2
                msd[t] += dist_sq
        
        # Average
        msd = [m / num_walkers for m in msd]
        
        return msd
    
    def estimate_walk_dimension(self, msd: List[float],
                                t_min: int = 50,
                                t_max: int = 500) -> float:
        """
        Estimate walk dimension from MSD.
        
        MSD ~ t^(2/d_w) => d_w = 2 / slope
        
        Args:
            msd: Mean square displacement
            t_min, t_max: Fitting range
            
        Returns:
            Walk dimension
        """
        t_vals = list(range(t_min, min(t_max, len(msd))))
        
        if len(t_vals) < 10:
            return 0.0
        
        log_t = [math.log(t) for t in t_vals]
        log_msd = [math.log(max(msd[t], 1e-10)) for t in t_vals]
        
        # Linear fit
        n = len(log_t)
        sum_x = sum(log_t)
        sum_y = sum(log_msd)
        sum_xy = sum(x * y for x, y in zip(log_t, log_msd))
        sum_x2 = sum(x ** 2 for x in log_t)
        
        if abs(n * sum_x2 - sum_x ** 2) < 1e-10:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        # d_w = 2 / slope where MSD ~ t^(2/d_w)
        if abs(slope) < 1e-10:
            return float('inf')
        
        return 2.0 / slope
    
    def estimate_spectral_dimension(self, d_w: float, 
                                    d_f: float) -> float:
        """
        Estimate spectral dimension using Alexander-Orbach relation.
        
        d_s = 2 * d_f / d_w
        
        Args:
            d_w: Walk dimension
            d_f: Fractal dimension
            
        Returns:
            Spectral dimension
        """
        if d_w > 0:
            return 2.0 * d_f / d_w
        return 0.0


class RandomWalkAnalyzer3D:
    """Analyze random walks on 3D percolation."""
    
    def __init__(self, width: int, height: int, depth: int):
        self.width = width
        self.height = height
        self.depth = depth
        self.lattice = LatticePercolation3D(width, height, depth)
    
    def analyze_at_criticality(self, p: float = None,
                              num_walkers: int = 50,
                              max_steps: int = 500,
                              seed: int = 42) -> RandomWalkResult:
        """
        Analyze random walks at criticality.
        
        Args:
            p: Occupation probability (use critical if None)
            num_walkers: Number of walkers
            max_steps: Max steps per walk
            seed: Random seed
            
        Returns:
            Analysis results
        """
        if p is None:
            p = 0.3116  # 3D critical point
        
        print(f"  Generating 3D percolation at p={p}...")
        occupied = self.lattice.site_percolation(p, seed)
        labels, num_clusters = self.lattice.find_clusters(occupied)
        
        # Find largest cluster
        from collections import Counter
        cluster_sizes = Counter(labels)
        if 0 in cluster_sizes:
            del cluster_sizes[0]
        
        if not cluster_sizes:
            print("  No clusters found!")
            return RandomWalkResult(
                num_steps=max_steps,
                num_walkers=0,
                msd_values=[],
                walk_dimension=0.0,
                spectral_dimension=0.0,
                computation_time=0.0
            )
        
        largest_label = cluster_sizes.most_common(1)[0][0]
        largest_size = cluster_sizes.most_common(1)[0][1]
        
        print(f"  Largest cluster size: {largest_size}")
        
        # Compute fractal dimension
        d_f = self.lattice.calculate_fractal_dimension(
            occupied, labels, largest_label
        )
        print(f"  Fractal dimension: {d_f:.3f}")
        
        # Setup random walk
        print(f"  Running {num_walkers} random walks...")
        start_time = time.time()
        
        rw = RandomWalk3D(self.lattice, occupied, labels, largest_label)
        msd = rw.compute_msd(num_walkers, max_steps)
        
        # Estimate dimensions
        d_w = rw.estimate_walk_dimension(msd, t_min=50, t_max=min(400, max_steps))
        d_s = rw.estimate_spectral_dimension(d_w, d_f)
        
        elapsed = time.time() - start_time
        
        return RandomWalkResult(
            num_steps=max_steps,
            num_walkers=num_walkers,
            msd_values=msd,
            walk_dimension=d_w,
            spectral_dimension=d_s,
            computation_time=elapsed
        )


def run_3d_random_walk_analysis():
    """Run complete 3D random walk analysis."""
    print("=" * 70)
    print("J Direction: 3D Random Walk on Percolation Clusters")
    print("=" * 70)
    print()
    
    # System sizes
    sizes = [(20, 20, 20), (30, 30, 30)]
    
    all_results = []
    
    for w, h, d in sizes:
        print(f"\nSystem: {w}x{h}x{d}")
        print("-" * 50)
        
        analyzer = RandomWalkAnalyzer3D(w, h, d)
        result = analyzer.analyze_at_criticality(
            p=0.3116,
            num_walkers=50,
            max_steps=500,
            seed=42
        )
        
        print(f"\nResults:")
        print(f"  Walk dimension d_w: {result.walk_dimension:.3f}")
        print(f"  Spectral dimension d_s: {result.spectral_dimension:.3f}")
        print(f"  Computation time: {result.computation_time:.2f}s")
        
        all_results.append((w, h, d, result))
    
    # Summary and comparison
    print("\n" + "=" * 70)
    print("Summary: 2D vs 3D Random Walk")
    print("=" * 70)
    print()
    print(f"{'System':<20} {'d_w':<10} {'d_s':<10} {'Theory d_s':<12}")
    print("-" * 70)
    
    # 2D values from previous analysis
    print(f"{'2D (20x20)':<20} {'2.573':<10} {'1.223':<10} {'1.333':<12}")
    
    # 3D values
    for w, h, d, result in all_results:
        name = f"3D ({w}x{h}x{d})"
        print(f"{name:<20} {result.walk_dimension:<10.3f} "
              f"{result.spectral_dimension:<10.3f} {'1.333':<12}")
    
    print("\nAlexander-Orbach relation: d_s = 2*d_f/d_w ≈ 4/3")
    print("Expected spectral dimension for d ≥ 2: 1.333")
    
    print("\n" + "=" * 70)
    print("3D Random Walk Analysis Complete")
    print("=" * 70)
    
    return all_results


if __name__ == "__main__":
    results = run_3d_random_walk_analysis()
