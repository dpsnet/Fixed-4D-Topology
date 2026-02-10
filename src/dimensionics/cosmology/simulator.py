"""Cosmological Simulator"""
import numpy as np

class CosmologicalSimulator:
    """Simulate cosmological evolution with dimension flow"""
    def __init__(self, H0=67.4, Omega_m=0.315):
        self.H0 = H0
        self.Omega_m = Omega_m
    
    def dimension_evolution(self, t):
        """d_s(t) evolution"""
        return 2 + 2 / (1 + np.exp(-(t - 1)))
