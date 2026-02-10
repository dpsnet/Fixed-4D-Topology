#!/usr/bin/env python3
"""
Spectral Dimension Implementation

Implements the spectral dimension formula:
d_s(t) = n - (R/3)t + O(t²)
"""

import numpy as np
from typing import Optional, Tuple


class SpectralDimension:
    """
    Calculate and analyze spectral dimensions for various manifolds.
    
    The spectral dimension describes how the effective dimension of a space
    changes with the scale of observation (diffusion time).
    
    Formula: d_s(t) = n - (R/3)t + O(t²)
    
    where:
        n: topological dimension
        R: Ricci scalar curvature
        t: diffusion time
    """
    
    def __init__(self, n: int, R: float, volume: float = 1.0):
        """
        Initialize spectral dimension calculator.
        
        Parameters:
            n: Topological dimension
            R: Ricci scalar curvature
            volume: Volume of manifold
        """
        self.n = n
        self.R = R
        self.V = volume
    
    def d_s(self, t: float, order: int = 1) -> float:
        """
        Calculate spectral dimension at diffusion time t.
        
        Parameters:
            t: Diffusion time
            order: Order of expansion (1 or 2)
            
        Returns:
            Spectral dimension
        """
        if t < 0:
            raise ValueError("Diffusion time must be non-negative")
        
        d = self.n - (self.R / 3.0) * t
        
        if order >= 2:
            # Second-order correction (simplified)
            a2 = self._seeley_deWitt_a2()
            d += a2 * t**2
        
        return max(d, 0.0)  # Dimension can't be negative
    
    def _seeley_deWitt_a2(self) -> float:
        """Calculate Seeley-DeWitt coefficient a_2"""
        # Simplified: a_2 ∝ R² for flat manifolds
        return (self.R ** 2) / 60.0
    
    def heat_kernel_trace(self, t: float) -> float:
        """
        Calculate heat kernel trace: K(t) = Tr(e^(-tΔ))
        
        Parameters:
            t: Diffusion time
            
        Returns:
            Heat kernel trace
        """
        # Asymptotic expansion
        a0 = self.V / (4 * np.pi * t)**(self.n/2)
        a1 = self.R * self.V / 6.0
        
        return a0 * (1 + a1 * t + O(t**2))
    
    def verify_formula(self, t_values: np.ndarray, d_numerical: np.ndarray) -> dict:
        """
        Verify the spectral dimension formula against numerical data.
        
        Parameters:
            t_values: Array of diffusion times
            d_numerical: Numerically computed spectral dimensions
            
        Returns:
            Dictionary with error statistics
        """
        d_theoretical = np.array([self.d_s(t) for t in t_values])
        
        error = np.abs(d_theoretical - d_numerical)
        
        return {
            'max_error': np.max(error),
            'mean_error': np.mean(error),
            'rms_error': np.sqrt(np.mean(error**2)),
            'percent_error': 100 * np.mean(error) / np.mean(np.abs(d_numerical))
        }


class O:
    """Big-O notation helper"""
    def __init__(self, order: int):
        self.order = order
    
    def __rmul__(self, other):
        return other * (self.order > 0)
    
    def __repr__(self):
        return f"O(t^{self.order})"
