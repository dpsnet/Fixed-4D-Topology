"""
Spectral analysis of complex networks.
"""

import numpy as np
from scipy.sparse import csgraph


def network_spectral_dimension(laplacian, t_values=None):
    """
    Compute spectral dimension of a network.
    
    Parameters:
    -----------
    laplacian : ndarray or sparse matrix
        Graph Laplacian
    t_values : array_like, optional
        Time values for heat kernel
        
    Returns:
    --------
    d_s : float
        Spectral dimension
    """
    if t_values is None:
        t_values = np.logspace(-2, 1, 50)
    
    eigenvalues = np.linalg.eigvalsh(laplacian)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]  # Remove zero modes
    
    # Heat kernel trace
    Z_t = np.array([np.sum(np.exp(-t * eigenvalues)) for t in t_values])
    
    # Spectral dimension from scaling
    log_t = np.log(t_values)
    log_Z = np.log(Z_t)
    
    # Linear fit to extract dimension
    slope = np.polyfit(log_t, log_Z, 1)[0]
    d_s = -2 * slope
    
    return max(0, d_s)


def laplacian_eigenvalues(adjacency_matrix, k=10):
    """
    Compute Laplacian eigenvalues.
    
    Parameters:
    -----------
    adjacency_matrix : ndarray
        Adjacency matrix
    k : int
        Number of eigenvalues to compute
        
    Returns:
    --------
    eigenvalues : ndarray
        Smallest k eigenvalues
    """
    laplacian = csgraph.laplacian(adjacency_matrix, normed=False)
    eigenvalues = np.linalg.eigvalsh(laplacian)
    return eigenvalues[:k]
