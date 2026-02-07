"""
Real Network Data Interface
===========================

Interface for loading actual real-world network datasets.
Provides adapters for SNAP, Network Repository, and other sources.

Note: Real data files need to be downloaded separately due to size.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import os
import gzip
from typing import Dict, Set, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RealDatasetInfo:
    """Information about a real network dataset."""
    name: str
    source: str  # 'SNAP', 'NetworkRepository', 'CAIDA', etc.
    url: str
    num_nodes: int
    num_edges: int
    file_size_mb: float
    file_format: str  # 'edges', 'adjlist', 'mtx', etc.
    description: str
    citation: str


class RealDataCatalog:
    """Catalog of available real-world datasets."""
    
    # Real datasets that can be downloaded
    AVAILABLE_DATASETS = {
        'facebook_combined': RealDatasetInfo(
            name='Facebook Combined',
            source='SNAP',
            url='https://snap.stanford.edu/data/egonets-Facebook.html',
            num_nodes=4039,
            num_edges=88234,
            file_size_mb=0.5,
            file_format='edges',
            description='Facebook social network (combined ego networks)',
            citation='McAuley, Leskovec (2012)'
        ),
        
        'twitter_combined': RealDatasetInfo(
            name='Twitter Combined',
            source='SNAP',
            url='https://snap.stanford.edu/data/egonets-Twitter.html',
            num_nodes=81306,
            num_edges=1768149,
            file_size_mb=9.5,
            file_format='edges',
            description='Twitter social network',
            citation='McAuley, Leskovec (2012)'
        ),
        
        'as_caida_2007': RealDatasetInfo(
            name='AS CAIDA 2007',
            source='CAIDA',
            url='http://www.caida.org/data/active/as-relationships/',
            num_nodes=26475,
            num_edges=106762,
            file_size_mb=1.5,
            file_format='edges',
            description='CAIDA AS Relationships (2007)',
            citation='CAIDA AS Relationships Dataset'
        ),
        
        'as_skitter': RealDatasetInfo(
            name='AS Skitter',
            source='SNAP',
            url='https://snap.stanford.edu/data/as-skitter.html',
            num_nodes=1696415,
            num_edges=11095298,
            file_size_mb=150.0,
            file_format='edges',
            description='Internet topology graph from skitter',
            citation='Leskovec et al. (2005)'
        ),
        
        'power_grid': RealDatasetInfo(
            name='US Power Grid',
            source='NetworkRepository',
            url='https://networkrepository.com/power-grid.php',
            num_nodes=4941,
            num_edges=6594,
            file_size_mb=0.1,
            file_format='edges',
            description='Western US power grid',
            citation='Watts, Strogatz (1998)'
        ),
        
        'yeast_protein': RealDatasetInfo(
            name='Yeast Protein Interactions',
            source='NetworkRepository',
            url='https://networkrepository.com/bio-yeast.php',
            num_nodes=1870,
            num_edges=2277,
            file_size_mb=0.05,
            file_format='edges',
            description='Yeast protein-protein interaction network',
            citation='Jeong et al. (2001)'
        ),
        
        'airport_usa': RealDatasetInfo(
            name='US Airport Network',
            source='NetworkRepository',
            url='https://networkrepository.com/inf-openflights.php',
            num_nodes=2939,
            num_edges=30501,
            file_size_mb=0.3,
            file_format='edges',
            description='US airport connections (OpenFlights)',
            citation='OpenFlights Database'
        ),
        
        'collab_dblp': RealDatasetInfo(
            name='DBLP Collaboration',
            source='SNAP',
            url='https://snap.stanford.edu/data/com-DBLP.html',
            num_nodes=317080,
            num_edges=1049866,
            file_size_mb=15.0,
            file_format='edges',
            description='DBLP collaboration network',
            citation='Yang, Leskovec (2012)'
        ),
        
        'internet_topology': RealDatasetInfo(
            name='Internet Topology',
            source='NetworkRepository',
            url='https://networkrepository.com/tech-internet-as.php',
            num_nodes=40164,
            num_edges=85123,
            file_size_mb=1.0,
            file_format='edges',
            description='Internet AS-level topology',
            citation='NetworkRepository'
        ),
        
        'road_network_pa': RealDatasetInfo(
            name='PA Road Network',
            source='SNAP',
            url='https://snap.stanford.edu/data/roadNet-PA.html',
            num_nodes=1088092,
            num_edges=1541898,
            file_size_mb=30.0,
            file_format='edges',
            description='Pennsylvania road network',
            citation='Leskovec et al. (2010)'
        )
    }
    
    @classmethod
    def list_available(cls) -> List[str]:
        """List names of available datasets."""
        return list(cls.AVAILABLE_DATASETS.keys())
    
    @classmethod
    def get_info(cls, name: str) -> Optional[RealDatasetInfo]:
        """Get information about a dataset."""
        return cls.AVAILABLE_DATASETS.get(name)
    
    @classmethod
    def print_catalog(cls):
        """Print catalog of all datasets."""
        print("=" * 80)
        print("Real Network Dataset Catalog")
        print("=" * 80)
        print()
        
        for name, info in cls.AVAILABLE_DATASETS.items():
            print(f"{name}")
            print(f"  Source: {info.source}")
            print(f"  Nodes: {info.num_nodes:,}, Edges: {info.num_edges:,}")
            print(f"  Size: {info.file_size_mb} MB")
            print(f"  URL: {info.url}")
            print(f"  Description: {info.description}")
            print()


class RealNetworkLoader:
    """Loader for real network data files."""
    
    def __init__(self, data_dir: str = './real_data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def load_edge_list(self, filename: str, 
                       directed: bool = False,
                       delimiter: str = None) -> Optional[Dict[int, Set[int]]]:
        """
        Load network from edge list file.
        
        Args:
            filename: Name of file (relative to data_dir)
            directed: Whether graph is directed
            delimiter: Field delimiter (None for whitespace)
            
        Returns:
            Graph as adjacency list, or None if file not found
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            print(f"Please download from the URL in catalog")
            return None
        
        graph = {}
        
        # Handle gzipped files
        if filepath.endswith('.gz'):
            opener = lambda: gzip.open(filepath, 'rt')
        else:
            opener = lambda: open(filepath, 'r')
        
        print(f"Loading {filename}...")
        
        with opener() as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(delimiter)
                if len(parts) >= 2:
                    try:
                        u = int(parts[0])
                        v = int(parts[1])
                        
                        # Add edge
                        if u not in graph:
                            graph[u] = set()
                        if v not in graph:
                            graph[v] = set()
                        
                        graph[u].add(v)
                        if not directed:
                            graph[v].add(u)
                            
                    except ValueError:
                        continue
        
        print(f"Loaded: {len(graph)} nodes")
        return graph
    
    def check_data_availability(self, dataset_name: str) -> bool:
        """Check if a dataset is available locally."""
        info = RealDataCatalog.get_info(dataset_name)
        if not info:
            return False
        
        # Check for common file names
        possible_files = [
            f"{dataset_name}.txt",
            f"{dataset_name}.edges",
            f"{dataset_name}.csv",
            f"{dataset_name}.txt.gz",
            f"{dataset_name}.edges.gz",
        ]
        
        for fname in possible_files:
            if os.path.exists(os.path.join(self.data_dir, fname)):
                return True
        
        return False
    
    def print_download_instructions(self, dataset_name: str):
        """Print instructions for downloading a dataset."""
        info = RealDataCatalog.get_info(dataset_name)
        if not info:
            print(f"Unknown dataset: {dataset_name}")
            return
        
        print("=" * 80)
        print(f"Download Instructions: {info.name}")
        print("=" * 80)
        print()
        print(f"1. Visit: {info.url}")
        print(f"2. Download the edge list file")
        print(f"3. Place in: {os.path.abspath(self.data_dir)}")
        print(f"4. Rename to: {dataset_name}.txt (or .edges, .csv)")
        print()
        print(f"Expected format: One edge per line")
        print(f"  <source_node> <target_node>")
        print()
        print(f"File size: ~{info.file_size_mb} MB")
        print(f"Citation: {info.citation}")
        print("=" * 80)


def generate_download_script():
    """Generate a shell script to download datasets."""
    script = """#!/bin/bash
# Download script for real network datasets
# Run this script to download real network data

mkdir -p real_data
cd real_data

echo "Downloading real network datasets..."

# Facebook (SNAP)
echo "1. Downloading Facebook network..."
wget -O facebook_combined.txt.gz \\
    https://snap.stanford.edu/data/facebook_combined.txt.gz
gunzip facebook_combined.txt.gz

# Power Grid (NetworkRepository)
echo "2. Downloading Power Grid..."
wget -O power_grid.txt \\
    https://networkrepository.com/power-grid-edges.txt

# Yeast Protein (NetworkRepository)
echo "3. Downloading Yeast Protein..."
wget -O yeast_protein.txt \\
    https://networkrepository.com/bio-yeast-edges.txt

echo "Done! Datasets saved in real_data/"
echo "Note: Some datasets require manual download due to terms of service"
"""
    
    with open('download_real_data.sh', 'w') as f:
        f.write(script)
    
    print("Generated download script: download_real_data.sh")
    print("Run: bash download_real_data.sh")


def compare_real_vs_simulated():
    """
    Compare statistics of real vs simulated networks.
    This shows the validation of our simulation approach.
    """
    print("=" * 80)
    print("Real vs Simulated Network Comparison")
    print("=" * 80)
    print()
    
    # Known statistics from literature
    real_stats = {
        'facebook': {
            'num_nodes': 4039,
            'avg_degree': 43.7,
            'clustering': 0.605,
            'diameter': 8,
            'source': 'SNAP'
        },
        'power_grid': {
            'num_nodes': 4941,
            'avg_degree': 2.67,
            'clustering': 0.080,
            'diameter': 46,
            'source': 'Watts-Strogatz (1998)'
        },
        'internet_as': {
            'num_nodes': 26475,
            'avg_degree': 4.03,
            'clustering': 0.208,
            'diameter': 11,
            'source': 'CAIDA'
        }
    }
    
    # Our simulated results (from Week 3)
    simulated_stats = {
        'facebook': {
            'num_nodes': 800,  # 20% scale
            'avg_degree': 36.92,
            'clustering': 0.200,
            'diameter': 'N/A'
        },
        'power_grid': {
            'num_nodes': 980,
            'avg_degree': 1.93,
            'clustering': 0.000,
            'diameter': 'N/A'
        },
        'internet_as': {
            'num_nodes': 4400,
            'avg_degree': 3.12,
            'clustering': 0.089,
            'diameter': 'N/A'
        }
    }
    
    print(f"{'Network':<15} {'Metric':<15} {'Real':<12} {'Simulated':<12} {'Error':<10}")
    print("-" * 80)
    
    for network in real_stats.keys():
        if network in simulated_stats:
            real = real_stats[network]
            sim = simulated_stats[network]
            
            # Average degree comparison
            error_k = abs(real['avg_degree'] - sim['avg_degree']) / real['avg_degree'] * 100
            print(f"{network:<15} {'<k>':<15} {real['avg_degree']:<12.2f} {sim['avg_degree']:<12.2f} {error_k:<10.1f}%")
            
            # Clustering comparison
            error_c = abs(real['clustering'] - sim['clustering']) / real['clustering'] * 100
            print(f"{'':<15} {'C':<15} {real['clustering']:<12.3f} {sim['clustering']:<12.3f} {error_c:<10.1f}%")
            print()
    
    print("=" * 80)
    print("Analysis:")
    print("- Simulated networks capture qualitative features")
    print("- Quantitative differences due to simplified models")
    print("- Real data validation essential for publication")
    print("=" * 80)


if __name__ == "__main__":
    # Print catalog
    RealDataCatalog.print_catalog()
    
    print("\n")
    
    # Show real vs simulated comparison
    compare_real_vs_simulated()
    
    print("\n")
    
    # Generate download script
    generate_download_script()
