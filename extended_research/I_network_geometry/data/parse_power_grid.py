"""
Parse IEEE Power System Data
============================

Parse IEEE power system test cases and extract network topology.
"""

import re
from typing import Dict, Set, Tuple


def parse_ieee_cdf(filepath: str) -> Dict[int, Set[int]]:
    """
    Parse IEEE Common Data Format (CDF) file and extract network topology.
    
    Returns:
        Graph as adjacency list (bus connections)
    """
    graph = {}
    buses = set()
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Parse bus data
    in_bus_data = False
    in_branch_data = False
    
    for line in lines:
        line = line.rstrip()
        
        # Check section headers
        if 'BUS DATA FOLLOWS' in line:
            in_bus_data = True
            continue
        elif 'BRANCH DATA FOLLOWS' in line:
            in_bus_data = False
            in_branch_data = True
            continue
        elif 'END OF DATA' in line:
            break
        
        # Parse bus data - extract bus numbers
        if in_bus_data and line.strip():
            # Bus number is in first 4 columns
            try:
                bus_num = int(line[0:4].strip())
                if bus_num > 0:
                    buses.add(bus_num)
                    if bus_num not in graph:
                        graph[bus_num] = set()
            except ValueError:
                pass
        
        # Parse branch data - extract connections
        if in_branch_data and line.strip():
            # Tap bus and Z bus are in first 8 columns (4 each)
            try:
                tap_bus = int(line[0:4].strip())
                z_bus = int(line[4:8].strip())
                
                if tap_bus > 0 and z_bus > 0:
                    # Add edge
                    if tap_bus not in graph:
                        graph[tap_bus] = set()
                    if z_bus not in graph:
                        graph[z_bus] = set()
                    
                    graph[tap_bus].add(z_bus)
                    graph[z_bus].add(tap_bus)
            except ValueError:
                pass
    
    # Remove isolated nodes
    graph = {k: v for k, v in graph.items() if v}
    
    return graph


def analyze_power_grid(graph: Dict[int, Set[int]], name: str = "Power Grid"):
    """Analyze power grid network."""
    n = len(graph)
    
    if n == 0:
        print(f"No valid graph data found for {name}")
        return None
    
    # Count edges
    m = sum(len(neighbors) for neighbors in graph.values()) // 2
    
    # Average degree
    avg_k = 2 * m / n if n > 0 else 0
    
    # Degree distribution
    degrees = [len(neighbors) for neighbors in graph.values()]
    max_k = max(degrees) if degrees else 0
    
    print(f"\n{'='*60}")
    print(f"{name} Analysis")
    print(f"{'='*60}")
    print(f"Nodes: {n}")
    print(f"Edges: {m}")
    print(f"Average degree: {avg_k:.2f}")
    print(f"Max degree: {max_k}")
    print(f"Density: {2*m/(n*(n-1)):.4f}" if n > 1 else "Density: 0")
    
    # Estimate clustering coefficient (simplified)
    clustering_sum = 0
    valid_nodes = 0
    
    for node, neighbors in list(graph.items())[:100]:  # Sample
        k = len(neighbors)
        if k < 2:
            continue
        
        # Count triangles
        triangles = 0
        neighbor_list = list(neighbors)
        for i in range(k):
            for j in range(i + 1, k):
                if neighbor_list[j] in graph.get(neighbor_list[i], set()):
                    triangles += 1
        
        possible = k * (k - 1) / 2
        if possible > 0:
            clustering_sum += triangles / possible
            valid_nodes += 1
    
    C = clustering_sum / valid_nodes if valid_nodes > 0 else 0
    print(f"Clustering coefficient (sampled): {C:.3f}")
    
    return {
        'name': name,
        'nodes': n,
        'edges': m,
        'avg_degree': avg_k,
        'max_degree': max_k,
        'clustering': C,
        'graph': graph
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    import analyze_large_network as aln
    
    # Parse IEEE 118 bus system
    print("Parsing IEEE 118 Bus Test Case...")
    graph = parse_ieee_cdf('./real_data/ieee_power.txt')
    
    if graph:
        # Basic analysis
        result = analyze_power_grid(graph, "IEEE 118 Bus Power Grid")
        
        if result:
            # Compute box dimension
            print("\nComputing box dimension...")
            d_B = aln.compute_box_dimension_fast(graph, max_box=10, num_samples=100)
            print(f"Box dimension: {d_B:.3f}")
            
            print(f"\n{'='*60}")
            print("Summary: IEEE 118 Bus Power Grid")
            print(f"{'='*60}")
            print(f"This is a standard IEEE power system test case")
            print(f"representing a portion of the American Electric Power")
            print(f"system in the midwestern United States.")
            print(f"\nNetwork characteristics:")
            print(f"- Nodes (buses): {result['nodes']}")
            print(f"- Edges (branches): {result['edges']}")
            print(f"- Average degree: {result['avg_degree']:.2f}")
            print(f"- Clustering coefficient: {result['clustering']:.3f}")
            print(f"- Box dimension: {d_B:.3f}")
            print(f"\nExpected dimension: ~2.0 (planar graph constraint)")
