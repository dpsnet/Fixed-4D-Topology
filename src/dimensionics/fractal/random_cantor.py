"""
Random Cantor sets and fractal dimension.
"""

import numpy as np


def random_cantor_set(n_iterations=10, removal_prob=0.5):
    """
    Generate random Cantor set.
    
    Parameters:
    -----------
    n_iterations : int
        Number of construction iterations
    removal_prob : float
        Probability of removing a subinterval
        
    Returns:
    --------
    intervals : list
        List of remaining intervals [(a,b), ...]
    """
    intervals = [(0.0, 1.0)]
    
    for _ in range(n_iterations):
        new_intervals = []
        for a, b in intervals:
            if np.random.random() > removal_prob:
                # Keep interval
                mid = (a + b) / 2
                new_intervals.extend([(a, mid), (mid, b)])
        intervals = new_intervals
    
    return intervals


def fractal_dimension(intervals, epsilon=1e-3):
    """
    Estimate fractal dimension from intervals.
    
    Parameters:
    -----------
    intervals : list
        Cantor set intervals
    epsilon : float
        Scale parameter
        
    Returns:
    --------
    d_f : float
        Fractal dimension estimate
    """
    total_length = sum(b - a for a, b in intervals)
    N = len(intervals)
    
    if N == 0:
        return 0.0
    
    # Box counting dimension
    return np.log(N) / np.log(1.0 / epsilon)
