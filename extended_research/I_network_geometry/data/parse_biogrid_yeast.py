"""
Parse BioGRID Yeast PPI Data
============================

Parse BioGRID yeast protein-protein interaction data and build network.
"""

from typing import Dict, Set, Tuple
import sys
sys.path.insert(0, '.')
import analyze_large_network as aln


def parse_biogrid_yeast(filepath: str, use_physical_only: bool = True) -> Dict[int, Set[int]]:
    """
    Parse BioGRID yeast PPI file and build network.
    
    Args:
        filepath: Path to BioGRID tab3 file
        use_physical_only: If True, only include physical interactions
        
    Returns:
        Graph as adjacency list (gene ID -> set of gene IDs)
    """
    graph = {}
    edges = set()
    
    print(f"Parsing {filepath}...")
    print(f"Physical interactions only: {use_physical_only}")
    
    with open(filepath, 'r') as f:
        # Skip header
        header = f.readline()
        
        line_count = 0
        for line in f:
            line_count += 1
            if line_count % 100000 == 0:
                print(f"  Processed {line_count:,} lines...")
            
            parts = line.strip().split('\t')
            if len(parts) < 20:
                continue
            
            # Extract gene IDs (Entrez Gene ID)
            try:
                gene_a = int(parts[1])  # Entrez Gene Interactor A
                gene_b = int(parts[2])  # Entrez Gene Interactor B
            except (ValueError, IndexError):
                continue
            
            # Filter for physical interactions only
            if use_physical_only:
                exp_type = parts[12] if len(parts) > 12 else ""
                if exp_type.lower() != "physical":
                    continue
            
            # Add edge (undirected)
            if gene_a != gene_b:  # Skip self-interactions
                edge = tuple(sorted([gene_a, gene_b]))
                edges.add(edge)
    
    print(f"Total interactions parsed: {line_count:,}")
    print(f"Unique edges: {len(edges):,}")
    
    # Build graph
    for gene_a, gene_b in edges:
        if gene_a not in graph:
            graph[gene_a] = set()
        if gene_b not in graph:
            graph[gene_b] = set()
        
        graph[gene_a].add(gene_b)
        graph[gene_b].add(gene_a)
    
    return graph


def analyze_yeast_ppi(graph: Dict[int, Set[int]], name: str = "Yeast PPI"):
    """Analyze yeast PPI network."""
    n = len(graph)
    
    if n == 0:
        print(f"No valid graph data for {name}")
        return None
    
    # Basic stats
    m = sum(len(neighbors) for neighbors in graph.values()) // 2
    avg_k = 2 * m / n if n > 0 else 0
    
    degrees = [len(neighbors) for neighbors in graph.values()]
    max_k = max(degrees) if degrees else 0
    
    print(f"\n{'='*60}")
    print(f"{name} Analysis")
    print(f"{'='*60}")
    print(f"Proteins (nodes): {n:,}")
    print(f"Interactions (edges): {m:,}")
    print(f"Average degree: {avg_k:.2f}")
    print(f"Max degree: {max_k}")
    
    # Clustering coefficient (sampled)
    print("\nComputing clustering coefficient (sampled)...")
    C = aln.compute_clustering_coefficient(graph, sample_size=1000)
    print(f"Clustering coefficient: {C:.3f}")
    
    # Box dimension
    print("\nComputing box dimension...")
    # For large networks, use smaller parameters
    if n > 5000:
        d_B = aln.compute_box_dimension_fast(graph, max_box=5, num_samples=200)
    else:
        d_B = aln.compute_box_dimension_fast(graph, max_box=10, num_samples=300)
    print(f"Box dimension: {d_B:.3f}")
    
    return {
        'name': name,
        'nodes': n,
        'edges': m,
        'avg_degree': avg_k,
        'max_degree': max_k,
        'clustering': C,
        'box_dim': d_B,
        'graph': graph
    }


if __name__ == "__main__":
    # Parse BioGRID yeast PPI data
    print("="*60)
    print("BioGRID Yeast PPI Network Analysis")
    print("Source: Saccharomyces cerevisiae S288c")
    print("Version: BioGRID 5.0.254")
    print("="*60)
    
    yeast_file = "./real_data/BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-5.0.254.tab3.txt"
    
    # Parse with physical interactions only
    graph = parse_biogrid_yeast(yeast_file, use_physical_only=True)
    
    if graph:
        # Analyze
        result = analyze_yeast_ppi(graph, "BioGRID Yeast PPI (Physical)")
        
        if result:
            print(f"\n{'='*60}")
            print("Summary: Yeast Protein-Protein Interaction Network")
            print(f"{'='*60}")
            print(f"This is the most comprehensive yeast PPI dataset available,")
            print(f"containing physical protein-protein interactions from")
            print(f"multiple high-throughput experiments.")
            print(f"\nNetwork characteristics:")
            print(f"- Proteins: {result['nodes']:,}")
            print(f"- Interactions: {result['edges']:,}")
            print(f"- Average degree: {result['avg_degree']:.2f}")
            print(f"- Clustering coefficient: {result['clustering']:.3f}")
            print(f"- Box dimension: {result['box_dim']:.3f}")
            print(f"\nExpected: Low dimension (d < 2.0) due to tree-like structure")
            print(f"Literature: Jeong et al. (2001), Nature 411:41-42")
