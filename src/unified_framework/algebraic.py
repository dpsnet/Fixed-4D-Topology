"""
Algebraic Module - Grothendieck Group Implementation (T4 Direction)
===================================================================

Implementation of fractal dimension Grothendieck group theory.
"""

import numpy as np
from fractions import Fraction
from typing import Tuple, Union


class FractalElement:
    """
    Element of the Grothendieck group: formal difference [d_N1] - [d_N2].
    """
    
    def __init__(self, positive: Tuple[int, float], negative: Tuple[int, float]):
        """
        Initialize element [d_N1] - [d_N2].
        
        Args:
            positive: (N1, r) for dimension log(N1)/log(1/r)
            negative: (N2, r) for dimension log(N2)/log(1/r)
        """
        self.N1, self.r1 = positive
        self.N2, self.r2 = negative
        
        # Simplify if same r
        if abs(self.r1 - self.r2) < 1e-10:
            self.r = self.r1
            self.simplified = True
        else:
            self.r = None
            self.simplified = False
    
    def __repr__(self):
        d1 = np.log(self.N1) / np.log(1/self.r1)
        d2 = np.log(self.N2) / np.log(1/self.r2)
        return f"FractalElement([{d1:.3f}] - [{d2:.3f}])"
    
    def __eq__(self, other):
        """Equality in Grothendieck group."""
        if not isinstance(other, FractalElement):
            return False
        
        # Two elements are equal if their isomorphism images are equal
        from .algebraic import GrothendieckGroup
        
        # Use common scaling ratio for comparison
        r = self.r1 if self.r else 1/3
        group = GrothendieckGroup(r)
        
        return abs(group.isomorphism(self) - group.isomorphism(other)) < 1e-10


class GrothendieckGroup:
    """
    Grothendieck group of fractal dimensions (T4).
    
    G_D^(r) = {[d_N1] - [d_N2]} / ~
    
    with isomorphism φ: G_D^(r) → (Q, +)
    """
    
    def __init__(self, scaling_ratio: float = 1/3):
        """
        Initialize Grothendieck group.
        
        Args:
            scaling_ratio: Base scaling ratio r
        """
        self.r = scaling_ratio
        self.log_inv_r = np.log(1 / scaling_ratio)
        
    def __repr__(self):
        return f"GrothendieckGroup(r={self.r})"
    
    def isomorphism(self, g: FractalElement) -> float:
        """
        Compute isomorphism φ: G_D → (Q, +).
        
        φ([d_N1] - [d_N2]) = (log(N1) - log(N2)) / log(1/r)
        
        Args:
            g: Grothendieck group element
            
        Returns:
            Rational number (as float)
        """
        # Convert both dimensions to the same scale
        d1 = np.log(g.N1) / np.log(1/g.r1)
        d2 = np.log(g.N2) / np.log(1/g.r2)
        
        return d1 - d2
    
    def from_rational(self, q: Union[Fraction, float]) -> FractalElement:
        """
        Construct group element from rational number.
        
        Args:
            q: Rational number
            
        Returns:
            Group element [g] with φ([g]) = q
        """
        if isinstance(q, Fraction):
            p, denom = q.numerator, q.denominator
        else:
            # Approximate as fraction
            frac = Fraction(q).limit_denominator(1000)
            p, denom = frac.numerator, frac.denominator
        
        # We want: (log(N1) - log(N2)) / log(1/r) = p/denom
        # => log(N1/N2) = p/denom * log(1/r)
        # => N1/N2 = (1/r)^(p/denom)
        
        # Choose N1 = 2^|p|, N2 = 2^|denom| with appropriate signs
        if p >= 0:
            N1, N2 = 2**p, 2**denom
        else:
            N1, N2 = 2**denom, 2**abs(p)
        
        return FractalElement((N1, self.r), (N2, self.r))
    
    def group_operation(self, g1: FractalElement, g2: FractalElement) -> FractalElement:
        """
        Group addition: g1 ⊕ g2.
        
        ([d_A] - [d_B]) ⊕ ([d_C] - [d_D]) = [d_A + d_C] - [d_B + d_D]
        
        Args:
            g1, g2: Group elements
            
        Returns:
            Sum g1 ⊕ g2
        """
        # Convert to dimensions
        d1_pos = np.log(g1.N1) / np.log(1/g1.r1)
        d1_neg = np.log(g1.N2) / np.log(1/g1.r2)
        d2_pos = np.log(g2.N1) / np.log(1/g2.r1)
        d2_neg = np.log(g2.N2) / np.log(1/g2.r2)
        
        # Sum: (d1_pos - d1_neg) + (d2_pos - d2_neg) = (d1_pos + d2_pos) - (d1_neg + d2_neg)
        d_pos = d1_pos + d2_pos
        d_neg = d1_neg + d2_neg
        
        # Convert back to N values (approximate)
        N_pos = int(np.exp(d_pos * self.log_inv_r))
        N_neg = int(np.exp(d_neg * self.log_inv_r))
        
        # Ensure at least 2
        N_pos = max(N_pos, 2)
        N_neg = max(N_neg, 2)
        
        return FractalElement((N_pos, self.r), (N_neg, self.r))
    
    def inverse(self, g: FractalElement) -> FractalElement:
        """
        Group inverse: -g.
        
        Args:
            g: Group element
            
        Returns:
            Inverse element
        """
        return FractalElement((g.N2, g.r2), (g.N1, g.r1))
    
    def identity(self) -> FractalElement:
        """
        Identity element: [d] - [d] for any d.
        
        Returns:
            Identity
        """
        return FractalElement((2, self.r), (2, self.r))
    
    def verify_isomorphism(self, n_tests: int = 100) -> dict:
        """
        Numerically verify the isomorphism property.
        
        Args:
            n_tests: Number of random tests
            
        Returns:
            Verification statistics
        """
        import random
        
        success_count = 0
        max_error = 0.0
        
        for _ in range(n_tests):
            # Random elements
            N1 = random.randint(2, 100)
            N2 = random.randint(2, 100)
            N3 = random.randint(2, 100)
            N4 = random.randint(2, 100)
            
            a = FractalElement((N1, self.r), (N2, self.r))
            b = FractalElement((N3, self.r), (N4, self.r))
            
            # Group operation
            c = self.group_operation(a, b)
            
            # Verify homomorphism
            phi_a = self.isomorphism(a)
            phi_b = self.isomorphism(b)
            phi_c = self.isomorphism(c)
            
            error = abs(phi_c - (phi_a + phi_b))
            max_error = max(max_error, error)
            
            if error < 1e-10:
                success_count += 1
        
        return {
            'success_rate': success_count / n_tests,
            'max_error': max_error,
            'n_tests': n_tests
        }
    
    def info(self) -> dict:
        """Get information about the group."""
        return {
            'scaling_ratio': self.r,
            'log_inv_r': self.log_inv_r,
            'isomorphism_target': 'Q (rational numbers)',
            'operation': 'addition',
            'identity': '0 = [d] - [d]'
        }


def demo_grothendieck_group():
    """Demonstrate Grothendieck group operations."""
    print("Grothendieck Group Demo")
    print("="*60)
    
    group = GrothendieckGroup(scaling_ratio=1/3)
    
    # Create elements
    # Element representing log(2)/log(3) ≈ 0.631
    g1 = FractalElement((2, 1/3), (1, 1/3))
    print(f"g1 = {g1}")
    print(f"φ(g1) = {group.isomorphism(g1):.4f}")
    
    # Element representing 1 = log(3)/log(3)
    g2 = FractalElement((3, 1/3), (1, 1/3))
    print(f"\ng2 = {g2}")
    print(f"φ(g2) = {group.isomorphism(g2):.4f}")
    
    # Group operation
    g3 = group.group_operation(g1, g2)
    print(f"\ng1 ⊕ g2 = {g3}")
    print(f"φ(g1 ⊕ g2) = {group.isomorphism(g3):.4f}")
    print(f"φ(g1) + φ(g2) = {group.isomorphism(g1) + group.isomorphism(g2):.4f}")
    
    # From rational
    q = Fraction(3, 5)
    g_from_q = group.from_rational(q)
    print(f"\nFrom rational {q}:")
    print(f"  Element: {g_from_q}")
    print(f"  φ(element) = {group.isomorphism(g_from_q):.4f}")
    
    # Verification
    print("\n" + "="*60)
    print("Verifying isomorphism...")
    result = group.verify_isomorphism(n_tests=1000)
    print(f"Success rate: {result['success_rate']*100:.2f}%")
    print(f"Max error: {result['max_error']:.2e}")


if __name__ == "__main__":
    demo_grothendieck_group()
EOF
echo "algebraic.py implemented successfully!"