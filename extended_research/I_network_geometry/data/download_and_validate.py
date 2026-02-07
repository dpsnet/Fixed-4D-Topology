"""
Download and Validate Real Network Data
======================================

Downloads real network datasets from public sources and validates
dimension measurements against simulated data.

Usage:
    python download_and_validate.py --dataset facebook
    python download_and_validate.py --dataset power_grid
    python download_and_validate.py --validate-all
"""

import os
import sys
import gzip
import urllib.request
import urllib.error
from typing import Dict, Set, Optional, Tuple, List
from dataclasses import dataclass
import math
import random


# Set random seed for reproducibility
random.seed(42)


@dataclass
class DimensionResult:
    """Result of dimension measurement."""
    network_name: str
    data_type: str  # 'real' or 'simulated'
    num_nodes: int
    num_edges: int
    avg_degree: float
    box_dim: float
    corr_dim: float
    clustering: float


class RealNetworkValidator:
    """Validator for real network dimension measurements."""
    
    # Dataset download URLs
    DATASET_URLS = {
        'facebook': {
            'url': 'https://snap.stanford.edu/data/facebook_combined.txt.gz',
            'filename': 'facebook_combined.txt.gz',
            'directed': False
        },
        'power_grid': {
            'url': 'https://networkrepository.com/power-grid-edges.txt',
            'filename': 'power_grid.txt',
            'directed': False
        },
        'yeast': {
            'url': 'https://networkrepository.com/bio-yeast-edges.txt',
            'filename': 'yeast.txt',
            'directed': False
        }
    }
    
    def __init__(self, data_dir: str = './real_data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def download_dataset(self, name: str) -> bool:
        """Download a dataset if not already present."""
        if name not in self.DATASET_URLS:
            print(f"Unknown dataset: {name}")
            return False
        
        info = self.DATASET_URLS[name]
        filepath = os.path.join(self.data_dir, info['filename'])
        
        if os.path.exists(filepath):
            print(f"Dataset {name} already exists at {filepath}")
            return True
        
        print(f"Downloading {name} from {info['url']}...")
        
        try:
            # Set user agent to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Academic Research; Dimensionics Study)'
            }
            request = urllib.request.Request(info['url'], headers=headers)
            
            with urllib.request.urlopen(request, timeout=60) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            
            print(f"Downloaded to {filepath}")
            
            # Decompress if gzipped
            if filepath.endswith('.gz'):
                print("Decompressing...")
                with gzip.open(filepath, 'rb') as f_in:
                    with open(filepath[:-3], 'wb') as f_out:
                        f_out.write(f_in.read())
                os.remove(filepath)
                print(f"Decompressed to {filepath[:-3]}")
            
            return True
            
        except urllib.error.URLError as e:
            print(f"Download failed: {e}")
            print("\nPossible reasons:")
            print("1. Network connectivity issues")
            print("2. Server blocking automated downloads")
            print("3. URL has changed")
            print("\nTry manual download:")
            print(f"  wget {info['url']} -O {filepath}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def load_edge_list(self, name: str) -> Optional[Dict[int, Set[int]]]:
        """Load network from edge list file."""
        if name not in self.DATASET_URLS:
            return None
        
        info = self.DATASET_URLS[name]
        
        # Try different possible filenames
        possible_files = [
            info['filename'].replace('.gz', ''),
            info['filename'],
            f"{name}.txt",
            f"{name}.edges"
        ]
        
        filepath = None
        for fname in possible_files:
            path = os.path.join(self.data_dir, fname)
            if os.path.exists(path):
                filepath = path
                break
        
        if not filepath:
            print(f"File not found for {name}. Run download first.")
            return None
        
        print(f"Loading {filepath}...")
        
        graph = {}
        edge_count = 0
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        u = int(parts[0])
                        v = int(parts[1])
                        
                        # Add nodes
                        if u not in graph:
                            graph[u] = set()
                        if v not in graph:
                            graph[v] = set()
                        
                        # Add undirected edge
                        if v not in graph[u]:
                            graph[u].add(v)
                            graph[v].add(u)
                            edge_count += 1
                            
                    except ValueError:
                        continue
        
        print(f"Loaded: {len(graph)} nodes, {edge_count} edges")
        return graph
    
    def compute_network_stats(self, graph: Dict[int, Set[int]]) -> Dict:
        """Compute basic network statistics."""
        n = len(graph)
        
        # Count edges (each edge counted twice in undirected graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        
        # Average degree
        avg_k = 2 * m / n if n > 0 else 0
        
        # Clustering coefficient (approximate for large networks)
        clustering_sum = 0.0
        sampled_nodes = list(graph.keys())[:min(1000, n)]  # Sample for speed
        
        for node in sampled_nodes:
            neighbors = graph[node]
            ki = len(neighbors)
            if ki < 2:
                continue
            
            # Count triangles
            triangles = 0
            neighbors_list = list(neighbors)
            for i in range(ki):
                for j in range(i + 1, ki):
                    if neighbors_list[j] in graph[neighbors_list[i]]:
                        triangles += 1
            
            max_triangles = ki * (ki - 1) / 2
            if max_triangles > 0:
                clustering_sum += triangles / max_triangles
        
        C = clustering_sum / len(sampled_nodes) if sampled_nodes else 0
        
        return {
            'num_nodes': n,
            'num_edges': m,
            'avg_degree': avg_k,
            'clustering': C
        }
    
    def compute_box_dimension(self, graph: Dict[int, Set[int]], 
                             max_box: int = 10) -> float:
        """
        Compute box-counting dimension using greedy coloring algorithm.
        Simplified version for pure Python.
        """
        nodes = list(graph.keys())
        n = len(nodes)
        
        if n < 10:
            return 0.0
        
        # For efficiency, use sampling on large networks
        if n > 5000:
            sample_size = 5000
            nodes = random.sample(nodes, sample_size)
            # Create subgraph
            subgraph = {u: graph[u] & set(nodes) for u in nodes}
        else:
            subgraph = graph
        
        box_sizes = []
        box_counts = []
        
        # Use box sizes from 1 to max_box
        for lb in range(1, min(max_box, n // 10) + 1):
            # Greedy box covering
            uncovered = set(subgraph.keys())
            num_boxes = 0
            
            while uncovered:
                # Pick a random uncovered node as box center
                center = random.choice(list(uncovered))
                
                # Find all nodes within distance lb
                box = self._ball(subgraph, center, lb)
                box &= uncovered  # Only uncovered nodes
                
                uncovered -= box
                num_boxes += 1
            
            if num_boxes > 0:
                box_sizes.append(lb)
                box_counts.append(num_boxes)
        
        # Linear regression for dimension
        if len(box_sizes) < 2:
            return 1.0
        
        # log(N) vs log(1/lb)
        log_inv_sizes = [math.log(1.0 / lb) for lb in box_sizes]
        log_counts = [math.log(n) for n in box_counts]
        
        # Simple linear fit
        n_pts = len(log_inv_sizes)
        x_mean = sum(log_inv_sizes) / n_pts
        y_mean = sum(log_counts) / n_pts
        
        numerator = sum((log_inv_sizes[i] - x_mean) * (log_counts[i] - y_mean) 
                       for i in range(n_pts))
        denominator = sum((log_inv_sizes[i] - x_mean) ** 2 for i in range(n_pts))
        
        if denominator == 0:
            return 1.0
        
        dimension = numerator / denominator
        return max(0.5, min(5.0, dimension))  # Clamp to reasonable range
    
    def _ball(self, graph: Dict[int, Set[int]], center: int, 
              radius: int) -> Set[int]:
        """Get ball of given radius around center node (BFS)."""
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
    
    def validate_dataset(self, name: str) -> Optional[DimensionResult]:
        """Download, load, and measure dimensions of a real network."""
        # Try to download if not exists
        if not self.download_dataset(name):
            print(f"Could not download {name}")
            return None
        
        # Load the network
        graph = self.load_edge_list(name)
        if not graph:
            return None
        
        # Compute statistics
        print(f"\nAnalyzing {name}...")
        stats = self.compute_network_stats(graph)
        print(f"  Nodes: {stats['num_nodes']:,}")
        print(f"  Edges: {stats['num_edges']:,}")
        print(f"  <k>: {stats['avg_degree']:.2f}")
        print(f"  C: {stats['clustering']:.3f}")
        
        # Compute dimensions
        print("  Computing box dimension...")
        d_B = self.compute_box_dimension(graph)
        print(f"  d_B = {d_B:.3f}")
        
        return DimensionResult(
            network_name=name,
            data_type='real',
            num_nodes=stats['num_nodes'],
            num_edges=stats['num_edges'],
            avg_degree=stats['avg_degree'],
            box_dim=d_B,
            corr_dim=0.0,  # Not computed for speed
            clustering=stats['clustering']
        )
    
    def compare_with_simulated(self, real_result: DimensionResult) -> None:
        """Compare real network with simulated counterpart."""
        # Simulated results from Week 3
        simulated = {
            'facebook': {
                'num_nodes': 800,
                'avg_degree': 36.92,
                'clustering': 0.200,
                'box_dim': 1.274
            },
            'power_grid': {
                'num_nodes': 980,
                'avg_degree': 1.93,
                'clustering': 0.000,
                'box_dim': 0.403
            },
            'yeast': {
                'num_nodes': 380,
                'avg_degree': 2.36,
                'clustering': 0.000,
                'box_dim': 0.085
            }
        }
        
        name = real_result.network_name
        if name not in simulated:
            print(f"No simulated data for {name}")
            return
        
        sim = simulated[name]
        
        print("\n" + "=" * 60)
        print(f"Comparison: Real vs Simulated ({name})")
        print("=" * 60)
        print(f"{'Metric':<20} {'Real':<15} {'Simulated':<15} {'Error':<10}")
        print("-" * 60)
        
        # Average degree
        error_k = abs(real_result.avg_degree - sim['avg_degree']) / sim['avg_degree'] * 100
        print(f"{'Avg degree':<20} {real_result.avg_degree:<15.2f} {sim['avg_degree']:<15.2f} {error_k:<10.1f}%")
        
        # Clustering
        error_c = abs(real_result.clustering - sim['clustering']) / max(sim['clustering'], 0.001) * 100
        print(f"{'Clustering':<20} {real_result.clustering:<15.3f} {sim['clustering']:<15.3f} {error_c:<10.1f}%")
        
        # Box dimension
        error_d = abs(real_result.box_dim - sim['box_dim']) / max(sim['box_dim'], 0.001) * 100
        print(f"{'Box dimension':<20} {real_result.box_dim:<15.3f} {sim['box_dim']:<15.3f} {error_d:<10.1f}%")
        
        print("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download and validate real network data')
    parser.add_argument('--dataset', type=str, 
                       choices=['facebook', 'power_grid', 'yeast', 'all'],
                       default='all',
                       help='Dataset to download and validate')
    parser.add_argument('--data-dir', type=str, default='./real_data',
                       help='Directory to store downloaded data')
    
    args = parser.parse_args()
    
    validator = RealNetworkValidator(args.data_dir)
    
    if args.dataset == 'all':
        datasets = ['facebook', 'power_grid', 'yeast']
    else:
        datasets = [args.dataset]
    
    results = []
    for name in datasets:
        result = validator.validate_dataset(name)
        if result:
            results.append(result)
            validator.compare_with_simulated(result)
    
    # Summary
    if results:
        print("\n" + "=" * 60)
        print("Validation Summary")
        print("=" * 60)
        print(f"{'Network':<15} {'Nodes':<10} {'<k>':<8} {'C':<8} {'d_B':<8}")
        print("-" * 60)
        for r in results:
            print(f"{r.network_name:<15} {r.num_nodes:<10} {r.avg_degree:<8.2f} {r.clustering:<8.3f} {r.box_dim:<8.3f}")
        print("=" * 60)


if __name__ == "__main__":
    main()
