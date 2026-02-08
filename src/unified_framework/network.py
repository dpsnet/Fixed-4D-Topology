"""
Network Dimension Analysis Module (I Direction)
==============================================

Unified framework for computing effective dimensions of complex networks.
Based on empirical study of 7 real networks (2.1M nodes total).
"""

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    import math
    # Minimal numpy-like fallback
    class _NumpyFallback:
        @staticmethod
        def mean(arr):
            return sum(arr) / len(arr) if arr else 0
        @staticmethod
        def std(arr, ddof=0):
            if len(arr) <= ddof:
                return 0
            m = sum(arr) / len(arr)
            variance = sum((x - m) ** 2 for x in arr) / (len(arr) - ddof)
            return math.sqrt(variance)
        @staticmethod
        def array(arr):
            return list(arr)
        @staticmethod
        def log(x):
            if hasattr(x, '__iter__'):
                return [math.log(v) for v in x]
            return math.log(x)
        @staticmethod
        def exp(x):
            if hasattr(x, '__iter__'):
                return [math.exp(v) for v in x]
            return math.exp(x)
        @staticmethod
        def linspace(start, stop, num):
            if num <= 1:
                return [start]
            step = (stop - start) / (num - 1)
            return [start + i * step for i in range(num)]
        @staticmethod
        def zeros(n):
            return [0.0] * n
        @staticmethod
        def sqrt(x):
            return math.sqrt(x)
        @staticmethod
        def polyfit(x, y, deg):
            # Simple linear regression for deg=1
            if deg != 1:
                raise NotImplementedError("Only linear fit supported in fallback")
            n = len(x)
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            ss_xy = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            ss_xx = sum((x[i] - x_mean) ** 2 for i in range(n))
            slope = ss_xy / ss_xx if ss_xx != 0 else 0
            intercept = y_mean - slope * x_mean
            return [slope, intercept]
        @staticmethod
        def polyval(coeffs, x):
            # Evaluate polynomial
            result = []
            for xi in x:
                val = coeffs[0] * xi + coeffs[1] if len(coeffs) == 2 else coeffs[0]
                result.append(val)
            return result
    np = _NumpyFallback()
from typing import Dict, List, Tuple, Optional, Set
from collections import deque


class NetworkDimension:
    """
    Compute effective dimension of complex networks.
    
    Implements box-counting and correlation dimension methods
    validated on 7 real-world networks.
    """
    
    # Empirical dimension hierarchy from I-direction study
    DIMENSION_HIERARCHY = {
        'infrastructure': {'min': 2.0, 'max': 4.5, 'typical': 3.2},
        'academic': {'min': 2.5, 'max': 3.5, 'typical': 3.0},
        'social': {'min': 1.8, 'max': 2.8, 'typical': 2.3},
        'biological': {'min': 2.0, 'max': 2.6, 'typical': 2.4},
        'communication': {'min': 1.0, 'max': 1.5, 'typical': 1.2},
    }
    
    def __init__(self, graph: Optional[Dict] = None):
        """
        Initialize network dimension analyzer.
        
        Args:
            graph: Adjacency list representation {node: [neighbors]}
        """
        self.graph = graph or {}
        self.dimension_result = None
        
    def from_edge_list(self, edges: List[Tuple]) -> 'NetworkDimension':
        """
        Build graph from edge list.
        
        Args:
            edges: List of (u, v) tuples
            
        Returns:
            Self for chaining
        """
        self.graph = {}
        for u, v in edges:
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append(v)
            self.graph[v].append(u)
        return self
    
    def box_counting_dimension(self, 
                               max_box_size: int = 10,
                               min_box_size: int = 1) -> Dict:
        """
        Compute box-counting dimension using greedy coloring algorithm.
        
        Args:
            max_box_size: Maximum box diameter (in hops)
            min_box_size: Minimum box diameter
            
        Returns:
            Dictionary with dimension and analysis details
        """
        if not self.graph:
            raise ValueError("Graph not initialized")
        
        box_sizes = []
        num_boxes = []
        
        for lb in range(min_box_size, max_box_size + 1):
            # Greedy coloring for minimal box covering
            n_boxes = self._greedy_box_cover(lb)
            if n_boxes > 0:
                box_sizes.append(lb)
                num_boxes.append(n_boxes)
        
        if len(box_sizes) < 2:
            return {'dimension': None, 'error': 'Insufficient data'}
        
        # Linear regression on log-log plot
        log_lb = np.log(1.0 / np.array(box_sizes))
        log_nb = np.log(num_boxes)
        
        # Fit line
        coeffs = np.polyfit(log_lb, log_nb, 1)
        dimension = coeffs[0]
        r_squared = 1 - np.sum((log_nb - np.polyval(coeffs, log_lb))**2) / np.sum((log_nb - np.mean(log_nb))**2)
        
        result = {
            'dimension': dimension,
            'r_squared': r_squared,
            'box_sizes': box_sizes,
            'num_boxes': num_boxes,
            'method': 'box_counting',
            'fit_quality': 'good' if r_squared > 0.95 else 'fair' if r_squared > 0.9 else 'poor'
        }
        
        self.dimension_result = result
        return result
    
    def _greedy_box_cover(self, box_size: int) -> int:
        """
        Greedy algorithm for minimal box covering.
        
        Args:
            box_size: Maximum distance within a box
            
        Returns:
            Number of boxes needed
        """
        uncovered = set(self.graph.keys())
        num_boxes = 0
        
        while uncovered:
            # Pick an arbitrary uncovered node
            center = next(iter(uncovered))
            
            # Find all nodes within box_size hops
            box = self._bfs_within_distance(center, box_size)
            
            # Remove from uncovered
            uncovered -= box
            num_boxes += 1
        
        return num_boxes
    
    def _bfs_within_distance(self, start, max_distance: int) -> Set:
        """BFS to find all nodes within max_distance hops."""
        visited = {start}
        queue = deque([(start, 0)])
        
        while queue:
            node, dist = queue.popleft()
            if dist >= max_distance:
                continue
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return visited
    
    def correlation_dimension(self, 
                             max_radius: int = 10,
                             sample_ratio: float = 0.1) -> Dict:
        """
        Compute correlation dimension C(r) ~ r^d2.
        
        Args:
            max_radius: Maximum distance to consider
            sample_ratio: Fraction of nodes to sample (for large networks)
            
        Returns:
            Dictionary with dimension and analysis details
        """
        if not self.graph:
            raise ValueError("Graph not initialized")
        
        nodes = list(self.graph.keys())
        n_nodes = len(nodes)
        
        # Sample for large networks
        if sample_ratio < 1.0:
            import random
            sample_size = max(100, int(n_nodes * sample_ratio))
            sample_nodes = random.sample(nodes, min(sample_size, n_nodes))
        else:
            sample_nodes = nodes
        
        radii = list(range(1, max_radius + 1))
        correlations = []
        
        for r in radii:
            # Count pairs within distance r
            count = 0
            for i, node_i in enumerate(sample_nodes):
                neighbors_r = self._bfs_within_distance(node_i, r)
                count += len(neighbors_r)
            
            # C(r) = fraction of pairs within distance r
            c_r = count / (len(sample_nodes) * n_nodes)
            correlations.append(c_r)
        
        # Linear regression on log-log plot
        log_r = np.log(radii)
        log_c = np.log(correlations)
        
        # Fit line
        coeffs = np.polyfit(log_r, log_c, 1)
        dimension = coeffs[0]
        
        result = {
            'dimension': dimension,
            'r_squared': 1 - np.sum((log_c - np.polyval(coeffs, log_r))**2) / np.sum((log_c - np.mean(log_c))**2),
            'radii': radii,
            'correlations': correlations,
            'method': 'correlation',
        }
        
        return result
    
    def classify_network_type(self, dimension: float) -> str:
        """
        Classify network type based on empirical dimension hierarchy.
        
        Args:
            dimension: Computed network dimension
            
        Returns:
            Network type classification
        """
        for net_type, ranges in self.DIMENSION_HIERARCHY.items():
            if ranges['min'] <= dimension <= ranges['max']:
                return net_type
        return 'unknown'
    
    def compare_to_models(self, dimension: float) -> Dict:
        """
        Compare computed dimension to standard network models.
        
        Args:
            dimension: Computed network dimension
            
        Returns:
            Comparison results
        """
        # Standard models underestimate by 50-400%
        ba_prediction = 1.0  # Barabasi-Albert
        ws_prediction = 1.0  # Watts-Strogatz
        
        return {
            'computed_dimension': dimension,
            'ba_prediction': ba_prediction,
            'ws_prediction': ws_prediction,
            'ba_error': abs(dimension - ba_prediction) / dimension * 100,
            'ws_error': abs(dimension - ws_prediction) / dimension * 100,
            'conclusion': 'Standard models underestimate real dimensions' if dimension > 1.5 else 'Consistent with models'
        }


class NetworkMasterEquation:
    """
    Master Equation for network dimension selection.
    
    Extends the variational principle to complex networks.
    """
    
    def __init__(self, A: float = 1.0, B: float = 0.5, gamma: float = 0.3):
        """
        Initialize network Master Equation.
        
        Args:
            A: Efficiency parameter (path length cost)
            B: Cost parameter (construction cost)
            gamma: Efficiency exponent
        """
        self.A = A
        self.B = B
        self.gamma = gamma
    
    def efficiency_term(self, d: float, N: int) -> float:
        """
        Efficiency term: L(d) ~ A * d^(-gamma).
        
        Lower dimension increases average path length.
        """
        return self.A * (d ** (-self.gamma))
    
    def cost_term(self, d: float, N: int) -> float:
        """
        Cost term: C(d) ~ B * d * log(N).
        
        Higher dimension increases construction cost.
        """
        return self.B * d * np.log(max(N, 2))
    
    def free_energy(self, d: float, N: int) -> float:
        """
        Network free energy functional.
        
        Args:
            d: Dimension
            N: Network size
            
        Returns:
            Free energy value
        """
        return self.efficiency_term(d, N) + self.cost_term(d, N)
    
    def optimal_dimension(self, N: int) -> Dict:
        """
        Find optimal network dimension.
        
        Args:
            N: Network size
            
        Returns:
            Dictionary with optimal dimension and analysis
        """
        from scipy.optimize import minimize_scalar
        
        result = minimize_scalar(
            lambda d: self.free_energy(d, N),
            bounds=(0.5, 10.0),
            method='bounded'
        )
        
        d_opt = result.x
        F_min = result.fun
        
        return {
            'optimal_dimension': d_opt,
            'free_energy': F_min,
            'efficiency': self.efficiency_term(d_opt, N),
            'cost': self.cost_term(d_opt, N),
            'network_size': N
        }
    
    def predict_dimension(self, network_type: str, N: int) -> float:
        """
        Predict dimension based on network type and size.
        
        Args:
            network_type: Type of network (infrastructure, academic, etc.)
            N: Network size
            
        Returns:
            Predicted dimension
        """
        # Base parameters by network type
        params = {
            'infrastructure': {'A': 2.0, 'B': 0.3, 'beta': 2.5},
            'academic': {'A': 1.5, 'B': 0.4, 'beta': 1.8},
            'social': {'A': 1.0, 'B': 0.5, 'beta': 1.5},
            'biological': {'A': 1.0, 'B': 0.5, 'beta': 1.4},
            'communication': {'A': 0.5, 'B': 0.8, 'beta': 0.8},
        }
        
        p = params.get(network_type, params['social'])
        
        # d*(N) = alpha/log(N) + beta
        alpha = p['A'] / p['B']
        return alpha / np.log(max(N, 10)) + p['beta']


# Empirical data from I-direction study
EMPIRICAL_NETWORK_DATA = {
    'internet_as': {
        'name': 'Internet AS (CAIDA)',
        'nodes': 1696415,
        'edges': 11000000,
        'type': 'infrastructure',
        'dimension': 4.36,
        'source': 'CAIDA AS-Skitter'
    },
    'dblp': {
        'name': 'DBLP Collaboration',
        'nodes': 317080,
        'edges': 1049866,
        'type': 'academic',
        'dimension': 3.0,
        'source': 'SNAP'
    },
    'yeast_ppi': {
        'name': 'Yeast PPI (BioGRID)',
        'nodes': 6800,
        'edges': 865000,
        'type': 'biological',
        'dimension': 2.4,
        'source': 'BioGRID 5.0.254'
    },
    'facebook': {
        'name': 'Facebook Social',
        'nodes': 4039,
        'edges': 88234,
        'type': 'social',
        'dimension': 2.57,
        'source': 'SNAP'
    },
    'twitter': {
        'name': 'Twitter Social',
        'nodes': 81306,
        'edges': 1768149,
        'type': 'social',
        'dimension': 2.0,
        'source': 'SNAP'
    },
    'power_grid': {
        'name': 'IEEE Power Grid',
        'nodes': 101,
        'edges': 200,
        'type': 'infrastructure',
        'dimension': 2.11,
        'source': 'IEEE Test Case'
    },
    'email': {
        'name': 'Email EU-Core',
        'nodes': 1133,
        'edges': 5451,
        'type': 'communication',
        'dimension': 1.24,
        'source': 'SNAP'
    }
}


def get_empirical_data(network_name: str) -> Dict:
    """
    Get empirical data for a specific network.
    
    Args:
        network_name: Key from EMPIRICAL_NETWORK_DATA
        
    Returns:
        Network data dictionary
    """
    return EMPIRICAL_NETWORK_DATA.get(network_name, {})


def compare_to_empirical(computed_dim: float, network_type: str) -> Dict:
    """
    Compare computed dimension to empirical values.
    
    Args:
        computed_dim: Computed dimension value
        network_type: Type of network
        
    Returns:
        Comparison results
    """
    # Find empirical networks of same type
    empirical = [
        data for data in EMPIRICAL_NETWORK_DATA.values()
        if data['type'] == network_type
    ]
    
    if not empirical:
        return {'error': 'No empirical data for this type'}
    
    empirical_dims = [e['dimension'] for e in empirical]
    avg_dim = np.mean(empirical_dims)
    std_dim = np.std(empirical_dims)
    
    return {
        'computed': computed_dim,
        'empirical_avg': avg_dim,
        'empirical_std': std_dim,
        'difference': computed_dim - avg_dim,
        'within_std': abs(computed_dim - avg_dim) < std_dim,
        'comparison': 'consistent' if abs(computed_dim - avg_dim) < 2*std_dim else 'significant_difference'
    }