"""
Fisher Information Matrix for neural network effective dimension.
"""

import numpy as np


def fisher_information_matrix(gradients):
    """
    Compute Fisher Information Matrix from gradients.
    
    Parameters:
    -----------
    gradients : ndarray
        Shape (n_samples, n_parameters) gradient vectors
        
    Returns:
    --------
    FIM : ndarray
        Fisher Information Matrix
    """
    # FIM = E[grad * grad^T]
    return np.dot(gradients.T, gradients) / len(gradients)


def effective_dimension(fim, n_samples):
    """
    Compute effective dimension from Fisher Information Matrix.
    
    Parameters:
    -----------
    fim : ndarray
        Fisher Information Matrix
    n_samples : int
        Number of training samples
        
    Returns:
    --------
    d_eff : float
        Effective dimension (as fraction of total parameters)
    """
    eigenvalues = np.linalg.eigvalsh(fim)
    eigenvalues = np.maximum(eigenvalues, 1e-10)  # Numerical stability
    
    # Effective dimension formula
    d_eff = np.sum(eigenvalues / (eigenvalues + 1.0 / n_samples))
    
    # Normalize by total parameters
    n_params = len(eigenvalues)
    return d_eff / n_params
