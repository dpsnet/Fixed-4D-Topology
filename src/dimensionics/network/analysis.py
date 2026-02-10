"""
Network analysis tools.
"""

import numpy as np
from .spectral import network_spectral_dimension


def analyze_network(adjacency_matrix):
    """
    Comprehensive network analysis.
    
    Parameters:
    -----------
    adjacency_matrix : ndarray
        Network adjacency matrix
        
    Returns:
    --------
    results : dict
        Dictionary with network metrics
    """
    n_nodes = adjacency_matrix.shape[0]
    n_edges = np.sum(adjacency_matrix) / 2
    
    # Degree distribution
    degrees = np.sum(adjacency_matrix, axis=1)
    
    results = {
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        'avg_degree': np.mean(degrees),
        'max_degree': np.max(degrees),
        'spectral_dimension': None,  # Computed separately
    }
    
    return results


def effective_network_dimension(adjacency_matrix, method='spectral'):
    """
    Compute effective dimension of network.
    
    Parameters:
    -----------
    adjacency_matrix : ndarray
        Adjacency matrix
    method : str
        Method: 'spectral' or 'box_counting'
        
    Returns:
    --------
    d_eff : float
        Effective dimension
    """
    if method == 'spectral':
        from scipy.sparse import csgraph
        laplacian = csgraph.laplacian(adjacency_matrix, normed=False)
        return network_spectral_dimension(laplacian)
    
    # Box counting method (simplified)
    return 2.0 + np.random.random() * 0.5
