"""
Entanglement entropy and correlation functions.
"""

import numpy as np


def entanglement_entropy(singular_values):
    """
    Compute von Neumann entanglement entropy.
    
    Parameters:
    -----------
    singular_values : array_like
        Singular values from SVD
        
    Returns:
    --------
    S : float
        Entanglement entropy S = -sum(λ² log λ²)
    """
    s2 = singular_values ** 2
    s2 = s2 / np.sum(s2)  # Normalize
    return -np.sum(s2 * np.log(s2 + 1e-15))


def correlation_length(transfer_matrix):
    """
    Compute correlation length from transfer matrix.
    
    Parameters:
    -----------
    transfer_matrix : ndarray
        Transfer matrix
        
    Returns:
    --------
    xi : float
        Correlation length
    """
    eigenvalues = np.linalg.eigvals(transfer_matrix)
    eigenvalues = np.sort(np.abs(eigenvalues))[::-1]
    
    if len(eigenvalues) >= 2 and eigenvalues[1] > 0:
        return -1.0 / np.log(eigenvalues[1] / eigenvalues[0])
    return np.inf
