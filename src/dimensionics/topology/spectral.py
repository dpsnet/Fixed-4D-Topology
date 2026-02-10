"""Spectral Topology"""
import numpy as np

class SpectralTopology:
    """Spectral methods in topology"""
    def __init__(self, n, R):
        self.n = n
        self.R = R
    
    def d_s(self, t):
        """Spectral dimension"""
        return self.n - (self.R / 3) * t
