"""
Real Network Data Loader
========================

Framework for loading and analyzing real-world network datasets.
Includes data generators that mimic real network characteristics.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import json
import random
import math
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict


@dataclass
class RealNetworkProfile:
    """Profile of a real-world network."""
    name: str
    category: str  # 'internet', 'social', 'biological', 'transport'
    num_nodes: int
    num_edges: int
    avg_degree: float
    max_degree: int
    clustering_coeff: float
    diameter: int
    power_law_exponent: Optional[float] = None
    description: str = ""


class RealNetworkGenerator:
    """
    Generate networks with characteristics matching real-world networks.
    
    Since we cannot download actual datasets, we generate networks that
    match the statistical properties of real networks.
    """
    
    # Known network profiles from literature
    NETWORK_PROFILES = {
        'internet_as': RealNetworkProfile(
            name='Internet AS-level',
            category='internet',
            num_nodes=22000,
            num_edges=48000,
            avg_degree=4.4,
            max_degree=2500,
            clustering_coeff=0.18,
            diameter=10,
            power_law_exponent=2.1,
            description='Autonomous Systems level internet topology'
        ),
        'facebook': RealNetworkProfile(
            name='Facebook Social Network',
            category='social',
            num_nodes=4000,
            num_edges=88000,
            avg_degree=44,
            max_degree=1000,
            clustering_coeff=0.6,
            diameter=8,
            power_law_exponent=2.9,
            description='Facebook user friendship network'
        ),
        'yeast_protein': RealNetworkProfile(
            name='Yeast Protein Interaction',
            category='biological',
            num_nodes=1900,
            num_edges=2200,
            avg_degree=2.3,
            max_degree=60,
            clustering_coeff=0.12,
            diameter=14,
            power_law_exponent=2.4,
            description='Yeast protein-protein interaction network'
        ),
        'us_airports': RealNetworkProfile(
            name='US Airport Network',
            category='transport',
            num_nodes=500,
            num_edges=6000,
            avg_degree=24,
            max_degree=150,
            clustering_coeff=0.4,
            diameter=6,
            power_law_exponent=2.0,
            description='US airport connection network'
        ),
        'power_grid': RealNetworkProfile(
            name='Western US Power Grid',
            category='infrastructure',
            num_nodes=4900,
            num_edges=6600,
            avg_degree=2.7,
            max_degree=20,
            clustering_coeff=0.08,
            diameter=46,
            power_law_exponent=None,  # Exponential degree distribution
            description='Western US power transmission network'
        ),
        'collaboration': RealNetworkProfile(
            name='Scientific Collaboration',
            category='social',
            num_nodes=12000,
            num_edges=24000,
            avg_degree=4.0,
            max_degree=100,
            clustering_coeff=0.45,
            diameter=15,
            power_law_exponent=2.5,
            description='Scientist collaboration network'
        )
    }
    
    @classmethod
    def generate_from_profile(cls, profile_name: str, 
                             scale_factor: float = 1.0,
                             seed: int = 42) -> Dict[int, Set[int]]:
        """
        Generate network matching real-world profile.
        
        Args:
            profile_name: Name of network profile
            scale_factor: Scale down network size (for testing)
            seed: Random seed
            
        Returns:
            Generated network as adjacency list
        """
        if profile_name not in cls.NETWORK_PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}")
        
        profile = cls.NETWORK_PROFILES[profile_name]
        random.seed(seed)
        
        # Scale network
        n = int(profile.num_nodes * scale_factor)
        
        # Generate based on category
        if profile.category == 'internet' or profile.power_law_exponent is not None:
            return cls._generate_power_law_network(
                n, profile.power_law_exponent, 
                profile.avg_degree, profile.clustering_coeff
            )
        elif profile.category == 'social':
            return cls._generate_social_network(
                n, profile.avg_degree, profile.clustering_coeff
            )
        elif profile.category == 'biological':
            return cls._generate_biological_network(
                n, profile.avg_degree, profile.clustering_coeff
            )
        elif profile.category == 'transport':
            return cls._generate_transport_network(
                n, profile.avg_degree, profile.diameter
            )
        else:
            return cls._generate_generic_network(
                n, profile.avg_degree, profile.clustering_coeff
            )
    
    @staticmethod
    def _generate_power_law_network(n: int, gamma: float, 
                                   avg_k: float, C: float) -> Dict[int, Set[int]]:
        """Generate network with power-law degree distribution."""
        graph = {i: set() for i in range(n)}
        
        # Generate degrees from power law
        degrees = []
        for i in range(n):
            # P(k) ~ k^(-gamma)
            # Use rejection sampling
            while True:
                k = random.paretovariate(gamma - 1)
                if k < n:
                    degrees.append(min(int(k) + 1, n - 1))
                    break
        
        # Adjust to match average degree
        current_avg = sum(degrees) / n
        if current_avg > 0:
            scale = avg_k / current_avg
            degrees = [min(int(k * scale), n - 1) for k in degrees]
        
        # Ensure even sum
        if sum(degrees) % 2 != 0:
            degrees[0] += 1
        
        # Configuration model
        stubs = []
        for node, deg in enumerate(degrees):
            stubs.extend([node] * deg)
        
        random.shuffle(stubs)
        
        for i in range(0, len(stubs) - 1, 2):
            u, v = stubs[i], stubs[i + 1]
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
        
        return graph
    
    @staticmethod
    def _generate_social_network(n: int, avg_k: float, C: float) -> Dict[int, Set[int]]:
        """Generate social network with high clustering."""
        graph = {i: set() for i in range(n)}
        
        # Start with Watts-Strogatz-like structure
        k = int(avg_k)
        k = k if k % 2 == 0 else k + 1
        
        # Ring lattice
        for i in range(n):
            for j in range(1, k // 2 + 1):
                neighbor = (i + j) % n
                graph[i].add(neighbor)
                graph[neighbor].add(i)
        
        # Rewire with community structure (high clustering)
        p_rewire = 0.1
        for i in range(n):
            neighbors = list(graph[i])
            for j in neighbors:
                if j > i and random.random() < p_rewire:
                    # Rewire to create triangles
                    possible = [n for n in graph[j] if n != i and n not in graph[i]]
                    if possible and random.random() < C:
                        new_neighbor = random.choice(possible)
                        graph[i].remove(j)
                        graph[j].remove(i)
                        graph[i].add(new_neighbor)
                        graph[new_neighbor].add(i)
        
        return graph
    
    @staticmethod
    def _generate_biological_network(n: int, avg_k: float, 
                                    C: float) -> Dict[int, Set[int]]:
        """Generate biological network (sparse, modular)."""
        graph = {i: set() for i in range(n)}
        
        # Biological networks often have modular structure
        module_size = int(math.sqrt(n))
        num_modules = n // module_size
        
        # Intra-module connections (dense)
        for module in range(num_modules):
            start = module * module_size
            end = min(start + module_size, n)
            
            for i in range(start, end):
                for j in range(i + 1, end):
                    if random.random() < 0.3:  # Dense within module
                        graph[i].add(j)
                        graph[j].add(i)
        
        # Inter-module connections (sparse)
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i] and random.random() < 0.01:
                    graph[i].add(j)
                    graph[j].add(i)
        
        return graph
    
    @staticmethod
    def _generate_transport_network(n: int, avg_k: float, 
                                   diameter: int) -> Dict[int, Set[int]]:
        """Generate transportation network (spatial, hub-spoke)."""
        graph = {i: set() for i in range(n)}
        
        # Assign random positions in 2D space
        positions = [(random.random(), random.random()) for _ in range(n)]
        
        # Connect nearby nodes (spatial network)
        for i in range(n):
            # Find closest nodes
            distances = []
            for j in range(n):
                if i != j:
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    dist = math.sqrt(dx**2 + dy**2)
                    distances.append((dist, j))
            
            distances.sort()
            
            # Connect to k closest neighbors
            k = int(avg_k / 2)
            for _, j in distances[:k]:
                graph[i].add(j)
                graph[j].add(i)
        
        # Add hub connections
        num_hubs = max(1, n // 20)
        hubs = random.sample(range(n), num_hubs)
        
        for hub in hubs:
            for other in random.sample(range(n), min(10, n)):
                if other != hub:
                    graph[hub].add(other)
                    graph[other].add(hub)
        
        return graph
    
    @staticmethod
    def _generate_generic_network(n: int, avg_k: float, 
                                 C: float) -> Dict[int, Set[int]]:
        """Generate generic network."""
        graph = {i: set() for i in range(n)}
        
        k = int(avg_k)
        p = k / n
        
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    graph[i].add(j)
                    graph[j].add(i)
        
        return graph
    
    @classmethod
    def get_available_networks(cls) -> List[str]:
        """Get list of available network profiles."""
        return list(cls.NETWORK_PROFILES.keys())
    
    @classmethod
    def get_network_info(cls, profile_name: str) -> Dict:
        """Get information about a network profile."""
        if profile_name in cls.NETWORK_PROFILES:
            return asdict(cls.NETWORK_PROFILES[profile_name])
        return {}


class NetworkDatasetManager:
    """Manager for network datasets."""
    
    def __init__(self, data_dir: str = './datasets'):
        self.data_dir = data_dir
        self.datasets = {}
    
    def generate_all_datasets(self, scale_factor: float = 0.1, 
                             seed: int = 42) -> Dict[str, Dict]:
        """
        Generate all real-world-like datasets.
        
        Args:
            scale_factor: Scale down for testing (0.1 = 10% of real size)
            seed: Random seed
            
        Returns:
            Dictionary of dataset name -> network
        """
        print("Generating real-world network datasets...")
        print(f"Scale factor: {scale_factor}")
        print()
        
        results = {}
        
        for name in RealNetworkGenerator.get_available_networks():
            print(f"Generating: {name}...")
            
            try:
                network = RealNetworkGenerator.generate_from_profile(
                    name, scale_factor, seed
                )
                
                profile = RealNetworkGenerator.NETWORK_PROFILES[name]
                
                results[name] = {
                    'network': network,
                    'profile': profile,
                    'num_nodes': len(network),
                    'num_edges': sum(len(neighbors) for neighbors in network.values()) // 2
                }
                
                print(f"  Generated: {len(network)} nodes, "
                      f"{results[name]['num_edges']} edges")
                
            except Exception as e:
                print(f"  Error: {e}")
        
        return results
    
    def analyze_dataset_properties(self, network: Dict[int, Set[int]], 
                                   name: str) -> Dict:
        """Analyze properties of a network."""
        n = len(network)
        m = sum(len(neighbors) for neighbors in network.values()) // 2
        
        # Degree distribution
        degrees = [len(neighbors) for neighbors in network.values()]
        avg_degree = sum(degrees) / n if n > 0 else 0
        max_degree = max(degrees) if degrees else 0
        
        # Clustering coefficient (simplified)
        def local_clustering(node):
            neighbors = list(network[node])
            k = len(neighbors)
            if k < 2:
                return 0.0
            
            edges_between = 0
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if n2 in network[n1]:
                        edges_between += 1
            
            return 2.0 * edges_between / (k * (k - 1))
        
        clustering = sum(local_clustering(i) for i in range(n)) / n if n > 0 else 0
        
        return {
            'name': name,
            'num_nodes': n,
            'num_edges': m,
            'avg_degree': avg_degree,
            'max_degree': max_degree,
            'clustering_coeff': clustering,
            'density': 2 * m / (n * (n - 1)) if n > 1 else 0
        }


def run_real_network_tests():
    """Test real network generation and analysis."""
    print("=" * 70)
    print("I Direction: Real Network Dataset Tests")
    print("=" * 70)
    
    manager = NetworkDatasetManager()
    
    # Generate datasets at 10% scale
    print("\n[1] Generating Network Datasets (10% scale)")
    print("-" * 50)
    
    datasets = manager.generate_all_datasets(scale_factor=0.1, seed=42)
    
    # Analyze properties
    print("\n[2] Network Property Analysis")
    print("-" * 50)
    print(f"{'Network':<25} {'Nodes':<8} {'Edges':<8} {'<k>':<8} {'C':<8}")
    print("-" * 70)
    
    for name, data in datasets.items():
        props = manager.analyze_dataset_properties(data['network'], name)
        print(f"{name:<25} {props['num_nodes']:<8} {props['num_edges']:<8} "
              f"{props['avg_degree']:<8.2f} {props['clustering_coeff']:<8.3f}")
    
    print("\n[3] Comparison with Real Network Characteristics")
    print("-" * 50)
    
    for name, data in datasets.items():
        profile = data['profile']
        actual = manager.analyze_dataset_properties(data['network'], name)
        
        print(f"\n{name}:")
        print(f"  Category: {profile.category}")
        print(f"  Description: {profile.description}")
        print(f"  Target avg_degree: {profile.avg_degree:.2f}, "
              f"Actual: {actual['avg_degree']:.2f}")
        print(f"  Target clustering: {profile.clustering_coeff:.3f}, "
              f"Actual: {actual['clustering_coeff']:.3f}")
    
    print("\n" + "=" * 70)
    print("Real Network Tests Complete")
    print("=" * 70)
    
    return datasets


if __name__ == "__main__":
    datasets = run_real_network_tests()
