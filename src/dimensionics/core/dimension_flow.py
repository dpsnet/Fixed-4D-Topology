#!/usr/bin/env python3
"""
Dimension Flow

Implements UV-IR dimension flow: d_s(μ): 2 → 4
"""

import numpy as np


class DimensionFlow:
    """
    Calculate dimension flow from UV to IR.
    
    The dimension flows from d_s = 2 (UV, high energy) to
    d_s = 4 (IR, low energy) as energy scale μ changes.
    """
    
    def __init__(self, d_uv: float = 2.0, d_ir: float = 4.0, mu_star: float = 1.0):
        self.d_uv = d_uv
        self.d_ir = d_ir
        self.mu_star = mu_star
    
    def d_s(self, mu: float, gamma: float = 1.5) -> float:
        """
        Calculate spectral dimension at energy scale mu.
        
        Formula: d_s(μ) = d_uv + (d_ir - d_uv) / (1 + (μ/μ*)^(-γ))
        """
        return self.d_uv + (self.d_ir - self.d_uv) / (1 + (mu / self.mu_star)**(-gamma))
    
    def flow_array(self, mu_values: np.ndarray) -> np.ndarray:
        """Calculate dimension flow for array of energy scales"""
        return np.array([self.d_s(mu) for mu in mu_values])
