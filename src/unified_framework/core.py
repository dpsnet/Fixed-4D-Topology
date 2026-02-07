"""
Unified Dimensionics Framework - Core Module
============================================

Core classes: Dimension and VariationalPrinciple
"""

import numpy as np
from typing import Union, Optional, Callable
from fractions import Fraction


class Dimension:
    """
    Unified dimension representation supporting multiple forms:
    - Continuous (real number)
    - Cantor (rational combination of Cantor dimensions)
    - Grothendieck (group element)
    """
    
    def __init__(self, value: float, representation: str = 'continuous'):
        """
        Initialize dimension.
        
        Args:
            value: Dimension value or identifier
            representation: 'continuous', 'cantor', or 'grothendieck'
        """
        self.value = float(value)
        self.representation = representation
        self._cantor_coeffs = None  # For Cantor representation
        self._group_element = None  # For Grothendieck representation
        
    def __float__(self):
        return float(self.value)
    
    def __repr__(self):
        return f"Dimension({self.value:.4f}, '{self.representation}')"
    
    def to_cantor(self, precision: float = 1e-6) -> 'Dimension':
        """
        Convert to Cantor representation using greedy algorithm (T1).
        
        Args:
            precision: Target approximation error
            
        Returns:
            Dimension with Cantor representation
        """
        from .cantor import CantorRepresentation
        
        cantor = CantorRepresentation()
        coeffs = cantor.greedy_approximate(self.value, precision)
        
        d = Dimension(self.value, 'cantor')
        d._cantor_coeffs = coeffs
        return d
    
    def to_grothendieck(self, scaling_ratio: float = 1/3) -> 'Dimension':
        """
        Convert to Grothendieck group element (T4).
        
        Args:
            scaling_ratio: Base scaling ratio r
            
        Returns:
            Dimension with Grothendieck representation
        """
        from .algebraic import GrothendieckGroup
        
        group = GrothendieckGroup(scaling_ratio)
        # Approximate by rational
        q = Fraction(self.value).limit_denominator(1000)
        g = group.from_rational(q)
        
        d = Dimension(self.value, 'grothendieck')
        d._group_element = g
        return d
    
    def evolve(self, t: float, method: str = 'variational') -> float:
        """
        Compute evolved dimension at scale t.
        
        Args:
            t: Evolution parameter (time/scale)
            method: 'variational', 'pde', or 'flow'
            
        Returns:
            Evolved dimension value
        """
        if method == 'variational':
            # G direction: minimize free energy
            vp = VariationalPrinciple()
            return vp.optimal_dimension(temperature=t)
        elif method == 'pde':
            # T2 direction: spectral PDE
            from .evolution import SpectralPDE
            pde = SpectralPDE()
            return pde.compute_spectral_dimension(t)
        elif method == 'flow':
            # B direction: dimension flow
            from .evolution import DimensionFlow
            flow = DimensionFlow()
            return flow.evolve_dimension(self.value, t)
        else:
            raise ValueError(f"Unknown method: {method}")


class VariationalPrinciple:
    """
    Variational principle for dimension selection (G direction).
    
    Free energy: F(d) = A/d^alpha + T*d*log(d)
    """
    
    def __init__(self, A: float = 1.0, alpha: float = 0.5, T: float = 0.3):
        """
        Initialize variational principle.
        
        Args:
            A: Energy scale parameter
            alpha: Energy exponent
            T: Temperature parameter
        """
        self.A = A
        self.alpha = alpha
        self.T = T
        
    def free_energy(self, d: float) -> float:
        """
        Compute free energy F(d).
        
        Args:
            d: Dimension value
            
        Returns:
            Free energy
        """
        if d <= 0:
            return np.inf
        
        energy = self.A / (d ** self.alpha)
        entropy = self.T * d * np.log(d)
        return energy + entropy
    
    def optimal_dimension(self, temperature: Optional[float] = None) -> float:
        """
        Find optimal dimension d* = argmin F(d).
        
        Args:
            temperature: Optional override for T
            
        Returns:
            Optimal dimension
        """
        T = temperature if temperature is not None else self.T
        
        # Use scipy optimization
        from scipy.optimize import minimize_scalar
        
        result = minimize_scalar(
            lambda d: self.A / (d ** self.alpha) + T * d * np.log(d),
            bounds=(0.01, 10.0),
            method='bounded'
        )
        
        return result.x
    
    def critical_temperature(self) -> float:
        """
        Compute critical temperature where phase transition occurs.
        
        Returns:
            Critical temperature T_c
        """
        # Solve for T where second derivative vanishes
        # Approximate: T_c ≈ A * alpha / (d_c^(alpha+1))
        d_c = 1.0  # Approximate critical dimension
        return self.A * self.alpha / (d_c ** (self.alpha + 1))
    
    def on_grothendieck_group(self, group_element, group) -> float:
        """
        Evaluate functional on Grothendieck group element (Fusion FG-T4).
        
        Args:
            group_element: Element of Grothendieck group
            group: GrothendieckGroup instance
            
        Returns:
            Free energy value
        """
        d = group.isomorphism(group_element)
        return self.free_energy(d)
    
    def master_equation_solution(self, spectral_correction: Callable = None) -> float:
        """
        Solve Master Equation with optional spectral correction (Chapter 7).
        
        Args:
            spectral_correction: Function Lambda(d) for spectral term
            
        Returns:
            Solution d_eff
        """
        from scipy.optimize import minimize_scalar
        
        def total_functional(d):
            F = self.free_energy(d)
            if spectral_correction is not None:
                F += spectral_correction(d)
            return F
        
        result = minimize_scalar(
            total_functional,
            bounds=(0.001, 100.0),
            method='bounded'
        )
        
        return result.x


class DimensionicsFramework:
    """
    Main entry point for the unified dimensionics framework.
    
    Provides high-level interface to all directions (A-G, T1-T4).
    """
    
    def __init__(self):
        self.vp = VariationalPrinciple()
        self.dimensions = []
        
    def compute_effective_dimension(self, 
                                   target: float,
                                   method: str = 'variational',
                                   **kwargs) -> Dimension:
        """
        Compute effective dimension using specified method.
        
        Args:
            target: Target dimension value
            method: 'variational', 'cantor', 'grothendieck', 'pde', 'flow'
            **kwargs: Method-specific parameters
            
        Returns:
            Dimension object
        """
        if method == 'variational':
            d_opt = self.vp.optimal_dimension(**kwargs)
            return Dimension(d_opt, 'variational')
        
        elif method == 'cantor':
            d = Dimension(target)
            return d.to_cantor(**kwargs)
        
        elif method == 'grothendieck':
            d = Dimension(target)
            return d.to_grothendieck(**kwargs)
        
        elif method == 'pde':
            d = Dimension(target)
            evolved = d.evolve(method='pde', **kwargs)
            return Dimension(evolved, 'pde')
        
        elif method == 'flow':
            d = Dimension(target)
            evolved = d.evolve(method='flow', **kwargs)
            return Dimension(evolved, 'flow')
        
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def verify_fusion_theorems(self, verbose: bool = True) -> dict:
        """
        Verify all three fusion theorems numerically.
        
        Args:
            verbose: Print progress
            
        Returns:
            Dictionary of verification results
        """
        results = {}
        
        # FE-T1: E-T1 fusion
        if verbose:
            print("Verifying FE-T1 (E-T1 fusion)...")
        from .fusion import Fusion_ET1
        fusion_et1 = Fusion_ET1()
        results['FE-T1'] = fusion_et1.verify()
        
        # FB-T2: B-T2 fusion
        if verbose:
            print("Verifying FB-T2 (B-T2 fusion)...")
        from .fusion import Fusion_BT2
        fusion_bt2 = Fusion_BT2()
        results['FB-T2'] = fusion_bt2.verify()
        
        # FG-T4: G-T4 fusion
        if verbose:
            print("Verifying FG-T4 (G-T4 fusion)...")
        from .fusion import Fusion_GT4
        fusion_gt4 = Fusion_GT4()
        results['FG-T4'] = fusion_gt4.verify()
        
        if verbose:
            print("\nVerification complete!")
            for name, result in results.items():
                status = "✓" if result['success'] else "✗"
                print(f"  {status} {name}: {result['error']:.2%} error")
        
        return results


# Utility functions

def dimension_taxonomy(d: float, context: str = 'general') -> dict:
    """
    Classify dimension in the taxonomy (Section 7.4).
    
    Args:
        d: Dimension value
        context: 'general', 'quantum', 'network', 'random'
        
    Returns:
        Dictionary with classification
    """
    classification = {
        'value': d,
        'context': context,
        'category': None,
        'relations': {}
    }
    
    if 0 < d < 1:
        classification['category'] = 'fractal_curve'
    elif d == 1:
        classification['category'] = 'line'
    elif 1 < d < 2:
        classification['category'] = 'fractal_surface'
    elif d == 2:
        classification['category'] = 'plane'
    elif d > 2:
        classification['category'] = 'higher_dimensional'
    
    # Relations to other dimensions
    classification['relations']['d_s'] = f"≤ {d}"  # Spectral ≤ Hausdorff
    classification['relations']['d_eff'] = f"≥ {d}"  # Effective ≥ Hausdorff
    
    return classification


def master_equation(A: float = 1.0, 
                   alpha: float = 0.5, 
                   T: float = 0.3,
                   spectral_correction: Callable = None) -> float:
    """
    Solve Master Equation (Chapter 7).
    
    Args:
        A: Energy parameter
        alpha: Energy exponent
        T: Temperature
        spectral_correction: Optional Lambda(d) function
        
    Returns:
        Effective dimension d_eff
    """
    vp = VariationalPrinciple(A, alpha, T)
    return vp.master_equation_solution(spectral_correction)
EOF
echo "core.py implemented successfully!"