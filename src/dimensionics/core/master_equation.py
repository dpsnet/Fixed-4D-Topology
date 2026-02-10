#!/usr/bin/env python3
"""
Master Equation Implementation

The central equation governing dimension selection:
d_eff = argmin_d [E(d) - T·S(d) + Λ(d)]
"""

import numpy as np
from typing import Callable, Tuple, Optional
from scipy.optimize import minimize_scalar


class MasterEquation:
    """
    Implements the Dimensionics Master Equation.
    
    The Master Equation governs the effective dimension through a variational
    principle balancing energy, entropy, and spectral corrections.
    
    Parameters:
        alpha: Energy coefficient
        beta: Dissipation coefficient
        gamma: Nonlinear coupling (optional)
        
    Example:
        >>> me = MasterEquation(alpha=0.5, beta=0.3)
        >>> d_s = me.solve_dimension_flow(d_initial=4.0, t_span=10.0)
    """
    
    def __init__(self, alpha: float = 0.5, beta: float = 0.3, gamma: float = 0.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
    def energy(self, d: float) -> float:
        """Energy cost function E(d)"""
        return 0.5 * (d - 2.0)**2
    
    def entropy(self, d: float) -> float:
        """Entropy function S(d)"""
        if d <= 0:
            return -np.inf
        return np.log(d) + 0.5 * np.log(2 * np.pi * np.e)
    
    def spectral_correction(self, d: float) -> float:
        """Spectral correction Λ(d)"""
        return self.gamma * (d - 4.0)**4 / (1 + d**2)
    
    def action(self, d: float, T: float = 1.0) -> float:
        """
        Compute the action: S[d] = E(d) - T·S(d) + Λ(d)
        
        Parameters:
            d: Dimension value
            T: Temperature parameter
            
        Returns:
            Action value
        """
        return self.energy(d) - T * self.entropy(d) + self.spectral_correction(d)
    
    def solve_equilibrium(self, T: float = 1.0, d_bounds: Tuple[float, float] = (1.0, 10.0)) -> float:
        """
        Solve for equilibrium dimension: d_eff = argmin S[d]
        
        Parameters:
            T: Temperature
            d_bounds: (min, max) bounds for dimension
            
        Returns:
            Equilibrium dimension
        """
        result = minimize_scalar(
            lambda d: self.action(d, T),
            bounds=d_bounds,
            method='bounded'
        )
        return result.x
    
    def solve_dimension_flow(self, d_initial: float, t_span: float, dt: float = 0.01) -> np.ndarray:
        """
        Solve the dimension flow ODE: dd/dt = alpha - beta·d + gamma·f(d)
        
        Parameters:
            d_initial: Initial dimension
            t_span: Time span
            dt: Time step
            
        Returns:
            Array of dimension values over time
        """
        n_steps = int(t_span / dt)
        d_values = np.zeros(n_steps)
        d = d_initial
        
        for i in range(n_steps):
            d_values[i] = d
            # Master equation dynamics
            dd_dt = self.alpha - self.beta * d
            if self.gamma != 0:
                dd_dt += self.gamma * np.sin(np.pi * d / 2)
            d += dd_dt * dt
        
        return d_values
    
    def check_convexity(self, T: float = 1.0) -> bool:
        """
        Check if convexity condition is satisfied: alpha + beta > T/8
        
        Parameters:
            T: Temperature
            
        Returns:
            True if convexity condition satisfied
        """
        return self.alpha + self.beta > T / 8.0


# For backward compatibility
UnifiedDimension = MasterEquation
