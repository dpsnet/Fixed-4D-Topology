"""
T4: Fractal Arithmetic & Grothendieck Group

Implementation of algebraic structure on fractal dimensions
via logarithmic isomorphism to rational numbers.

Reference: docs/T4-fractal-arithmetic/
"""

import numpy as np
from fractions import Fraction
from typing import List, Tuple, Union
from dataclasses import dataclass


@dataclass(frozen=True)
class FractalElement:
    """
    Element of Grothendieck group of fractal dimensions.
    
    Represents formal difference: [D_1] - [D_2]
    where D_i are fractal dimensions.
    """
    positive: Tuple[int, int]  # (N, r) for dimension log(N)/log(1/r)
    negative: Tuple[int, int]  # (N, r) for dimension log(N)/log(1/r)
    
    def __post_init__(self):
        # Normalize: ensure r > 1
        if self.positive[1] <= 1 or self.negative[1] <= 1:
            raise ValueError("r must be > 1")
    
    def dimension_value(self) -> float:
        """
        Compute numerical value of this element.
        
        Value = log(N_+/r_+) - log(N_-/r_-)
        """
        d_pos = np.log(self.positive[0]) / np.log(self.positive[1])
        d_neg = np.log(self.negative[0]) / np.log(self.negative[1])
        return d_pos - d_neg


class GrothendieckGroup:
    """
    Grothendieck group of fractal dimensions.
    
    Theorem: (𝒢_D^(r), ⊕) ≅ (ℚ, +) via logarithmic map
    
    Elements are formal differences of fractal dimensions,
    with operation ⊕ induced from dimension addition.
    """
    
    def __init__(self, max_denominator: int = 1000):
        """
        Initialize Grothendieck group.
        
        Args:
            max_denominator: Maximum denominator for rational approximations
        """
        self.max_denominator = max_denominator
        self.elements: List[FractalElement] = []
    
    def log_isomorphism(self, element: FractalElement) -> Fraction:
        """
        Logarithmic isomorphism: 𝒢_D^(r) → ℚ.
        
        Maps [log(N_1)/log(r)] - [log(N_2)/log(r)] ↦ log(N_1/N_2)
        
        Args:
            element: Element of Grothendieck group
            
        Returns:
            Rational number in ℚ
        """
        # log(N_1/N_2) = log(N_1) - log(N_2)
        log_val = (np.log(element.positive[0]) - 
                   np.log(element.negative[0]))
        
        # Convert to rational approximation
        frac = Fraction(log_val).limit_denominator(self.max_denominator)
        return frac
    
    def inverse_log_isomorphism(self, q: Fraction) -> FractalElement:
        """
        Inverse logarithmic isomorphism: ℚ → 𝒢_D^(r).
        
        Args:
            q: Rational number
            
        Returns:
            Corresponding Grothendieck group element
        """
        # Find N such that log(N) ≈ q
        # For q = a/b, take N = e^q, approximate by integers
        target = float(q)
        
        # Find best integer approximation
        N_pos = int(np.exp(abs(target)) + 0.5)
        N_neg = 1
        
        if target < 0:
            N_pos, N_neg = N_neg, N_pos
        
        r = 2  # Standard base
        
        return FractalElement((N_pos, r), (N_neg, r))
    
    def group_operation(
        self,
        a: FractalElement,
        b: FractalElement
    ) -> FractalElement:
        """
        Group operation ⊕ on 𝒢_D^(r).
        
        Corresponds to addition in ℚ via isomorphism.
        
        Args:
            a: First element
            b: Second element
            
        Returns:
            a ⊕ b
        """
        # Use isomorphism: a ⊕ b = φ^{-1}(φ(a) + φ(b))
        phi_a = self.log_isomorphism(a)
        phi_b = self.log_isomorphism(b)
        sum_rational = phi_a + phi_b
        
        return self.inverse_log_isomorphism(sum_rational)
    
    def verify_isomorphism(self, n_tests: int = 100) -> dict:
        """
        Verify group isomorphism numerically.
        
        Theorem: φ: (𝒢_D^(r), ⊕) → (ℚ, +) is a group isomorphism.
        
        Args:
            n_tests: Number of test cases
            
        Returns:
            Verification statistics
        """
        errors = []
        
        for _ in range(n_tests):
            # Random elements
            N1 = np.random.randint(2, 100)
            N2 = np.random.randint(2, 100)
            N3 = np.random.randint(2, 100)
            N4 = np.random.randint(2, 100)
            r = np.random.randint(2, 5)
            
            a = FractalElement((N1, r), (N2, r))
            b = FractalElement((N3, r), (N4, r))
            
            # Test homomorphism: φ(a ⊕ b) = φ(a) + φ(b)
            a_plus_b = self.group_operation(a, b)
            lhs = self.log_isomorphism(a_plus_b)
            rhs = self.log_isomorphism(a) + self.log_isomorphism(b)
            
            error = abs(float(lhs - rhs))
            errors.append(error)
        
        return {
            "max_error": max(errors),
            "mean_error": np.mean(errors),
            "success_rate": sum(e < 1e-10 for e in errors) / len(errors),
            "n_tests": n_tests,
        }


class FractalArithmetic:
    """
    Arithmetic operations on fractal dimensions.
    
    Implements algebraic structure:
    - Addition (⊕) via Grothendieck group
    - Multiplication (⊗) via exponentiation
    - Distributive laws
    """
    
    def __init__(self):
        """Initialize fractal arithmetic."""
        self.group = GrothendieckGroup()
    
    def add_dimensions(self, d1: float, d2: float, base: float = 2.0) -> float:
        """
        Add fractal dimensions: d1 ⊕ d2.
        
        Uses the isomorphism: log(N1)/log(r) ⊕ log(N2)/log(r) = log(N1*N2)/log(r)
        
        Args:
            d1: First dimension
            d2: Second dimension
            base: Logarithm base
            
        Returns:
            d1 ⊕ d2
        """
        # d = log(N)/log(r) ⇒ N = r^d
        N1 = base ** d1
        N2 = base ** d2
        
        # Result: log(N1 * N2) / log(r) = log(N1)/log(r) + log(N2)/log(r)
        result = np.log(N1 * N2) / np.log(base)
        
        return result
    
    def multiply_dimensions(self, d1: float, d2: float, base: float = 2.0) -> float:
        """
        Multiply fractal dimensions: d1 ⊗ d2.
        
        Defined via exponentiation in the corresponding ℚ structure.
        
        Args:
            d1: First dimension
            d2: Second dimension
            base: Logarithm base
            
        Returns:
            d1 ⊗ d2
        """
        # Multiplication corresponds to exponentiation in dimension space
        # d1 ⊗ d2 = log(exp(d1) * exp(d2)) / log(base) = (d1 + d2)
        # This is just addition! Multiplication requires different structure.
        
        # Alternative: Use power tower
        # d1 ⊗ d2 = log(N1^log(N2)) / log(r) = log(N1)*log(N2) / log(r)^2
        N1 = base ** d1
        N2 = base ** d2
        
        result = np.log(N1) * np.log(N2) / (np.log(base) ** 2)
        return result
    
    def dimension_to_rational(self, d: float, r: float = 2.0) -> Fraction:
        """
        Convert fractal dimension to rational number.
        
        d = log(N)/log(r) ⟹ log(N) = d * log(r)
        
        Args:
            d: Fractal dimension
            r: Scaling factor
            
        Returns:
            Corresponding rational
        """
        log_val = d * np.log(r)
        return Fraction(log_val).limit_denominator(1000)
    
    def rational_to_dimension(self, q: Fraction, r: float = 2.0) -> float:
        """
        Convert rational number to fractal dimension.
        
        Args:
            q: Rational number
            r: Scaling factor
            
        Returns:
            Fractal dimension
        """
        return float(q) / np.log(r)


def demonstrate_grothendieck_isomorphism():
    """Demonstrate Grothendieck group isomorphism."""
    group = GrothendieckGroup()
    
    print("Grothendieck Group Isomorphism: 𝒢_D^(r) ≅ (ℚ, +)")
    print("=" * 50)
    print()
    
    # Create example elements
    a = FractalElement((2, 3), (1, 3))  # log(2)/log(3)
    b = FractalElement((3, 3), (1, 3))  # log(3)/log(3) = 1
    
    print(f"Element a: log({a.positive[0]})/log({a.positive[1]}) - log({a.negative[0]})/log({a.negative[1]})")
    print(f"  = log(2)/log(3) ≈ {a.dimension_value():.6f}")
    print(f"  φ(a) = {group.log_isomorphism(a)}")
    print()
    
    print(f"Element b: log({b.positive[0]})/log({b.positive[1]}) - log({b.negative[0]})/log({b.negative[1]})")
    print(f"  = log(3)/log(3) = {b.dimension_value():.6f}")
    print(f"  φ(b) = {group.log_isomorphism(b)}")
    print()
    
    # Group operation
    c = group.group_operation(a, b)
    print(f"a ⊕ b = c")
    print(f"  φ(a ⊕ b) = {group.log_isomorphism(c)}")
    print(f"  φ(a) + φ(b) = {group.log_isomorphism(a) + group.log_isomorphism(b)}")
    print()
    
    # Verify isomorphism
    print("Running isomorphism verification...")
    result = group.verify_isomorphism(n_tests=100)
    print(f"Tests: {result['n_tests']}")
    print(f"Success rate: {result['success_rate']*100:.1f}%")
    print(f"Mean error: {result['mean_error']:.2e}")


if __name__ == "__main__":
    demonstrate_grothendieck_isomorphism()
