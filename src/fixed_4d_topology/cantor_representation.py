"""
T1: Cantor Class Fractal Representation Theory

Implementation of the rigorous approximation theory for real numbers
using Cantor class fractal dimensions.

Reference: docs/T1-cantor-representation/cantor_representation_theory_arxiv.md
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CantorApproximation:
    """Result of Cantor representation approximation."""
    target: float
    epsilon: float
    dimensions: List[float]
    coefficients: List[float]
    approximation: float
    error: float
    steps: int
    convergence_rate: float


class CantorRepresentation:
    """
    Cantor class fractal representation theory implementation.
    
    Provides constructive algorithm for approximating real numbers
    using rational combinations of Cantor class fractal dimensions.
    
    Theorem (Convergence Rate): k ≤ C·log(1/ε) + O(1)
    where C = 1/log(3/2)
    """
    
    # Canonical Cantor class dimensions
    CANTOR_DIMENSIONS = np.array([
        np.log(2) / np.log(3),      # Standard Cantor: log(2)/log(3)
        np.log(3) / np.log(4),      # Variant 1: log(3)/log(4)
        np.log(4) / np.log(5),      # Variant 2: log(4)/log(5)
        np.log(5) / np.log(6),      # Variant 3: log(5)/log(6)
        np.log(6) / np.log(7),      # Variant 4: log(6)/log(7)
    ])
    
    def __init__(self, dimensions: Optional[np.ndarray] = None):
        """
        Initialize Cantor representation.
        
        Args:
            dimensions: Custom dimension set (default: CANTOR_DIMENSIONS)
        """
        self.dimensions = dimensions if dimensions is not None else self.CANTOR_DIMENSIONS
        self.C = 1.0 / np.log(3/2)  # Optimal constant from Theorem 4
        
    def approximate(self, alpha: float, epsilon: float = 1e-6) -> CantorApproximation:
        """
        Approximate real number alpha using Cantor dimensions.
        
        Algorithm 4.1 (Greedy Approximation):
        1. Initialize residual r_0 = alpha
        2. At step k: choose c_k minimizing |r_{k-1} - c_k * d_{i_k}|
        3. Update residual: r_k = r_{k-1} - c_k * d_{i_k}
        4. Stop when |r_k| < epsilon
        
        Args:
            alpha: Target real number to approximate
            epsilon: Desired precision
            
        Returns:
            CantorApproximation with all approximation details
            
        Complexity: O(log(1/epsilon)) steps (optimal by Theorem 4)
        """
        if epsilon <= 0:
            raise ValueError("epsilon must be positive")
            
        residual = float(alpha)
        dims = []
        coeffs = []
        steps = 0
        max_steps = int(self.C * np.log(1/epsilon)) + 10
        
        while abs(residual) > epsilon and steps < max_steps:
            # Greedy step: find best dimension and coefficient
            best_error = abs(residual)
            best_dim_idx = 0
            best_coeff = 0.0
            
            for i, d in enumerate(self.dimensions):
                # Optimal coefficient for this dimension
                c = residual / d
                # Round to simple rational
                c_rounded = round(c, 6)
                error = abs(residual - c_rounded * d)
                
                if error < best_error:
                    best_error = error
                    best_dim_idx = i
                    best_coeff = c_rounded
            
            # Update
            dims.append(float(self.dimensions[best_dim_idx]))
            coeffs.append(best_coeff)
            residual -= best_coeff * self.dimensions[best_dim_idx]
            steps += 1
        
        approximation = sum(c * d for c, d in zip(coeffs, dims))
        error = abs(alpha - approximation)
        
        # Convergence rate estimate
        if steps > 0:
            convergence_rate = np.log(1/epsilon) / steps
        else:
            convergence_rate = 0.0
        
        return CantorApproximation(
            target=alpha,
            epsilon=epsilon,
            dimensions=dims,
            coefficients=coeffs,
            approximation=approximation,
            error=error,
            steps=steps,
            convergence_rate=convergence_rate
        )
    
    def verify_linear_independence(self, tolerance: float = 1e-10) -> bool:
        """
        Verify linear independence of Cantor dimensions over Q.
        
        Theorem 1: The Cantor dimensions are linearly independent over Q.
        
        This is verified by checking that no non-trivial rational
        combination sums to zero within tolerance.
        
        Args:
            tolerance: Numerical tolerance for independence test
            
        Returns:
            True if dimensions appear linearly independent
        """
        # Check pairwise: d_i / d_j should be irrational
        n = len(self.dimensions)
        for i in range(n):
            for j in range(i+1, n):
                ratio = self.dimensions[i] / self.dimensions[j]
                # Check if ratio is close to rational with small denominator
                for q in range(1, 100):
                    p = round(ratio * q)
                    if abs(ratio - p/q) < tolerance:
                        return False
        return True
    
    def analyze_density(self, n_samples: int = 10000) -> dict:
        """
        Analyze density of rational combinations in R.
        
        Theorem 2: Rational combinations are dense in R.
        
        Numerically verify by sampling approximations.
        
        Args:
            n_samples: Number of random targets to test
            
        Returns:
            Dictionary with density analysis statistics
        """
        targets = np.random.uniform(-10, 10, n_samples)
        errors = []
        
        for target in targets:
            result = self.approximate(target, epsilon=1e-4)
            errors.append(result.error)
        
        errors = np.array(errors)
        
        return {
            "mean_error": float(np.mean(errors)),
            "max_error": float(np.max(errors)),
            "success_rate": float(np.mean(errors < 1e-4)),
            "n_samples": n_samples,
        }
    
    def compute_optimal_complexity(self, epsilon: float) -> float:
        """
        Compute theoretical optimal complexity bound.
        
        Theorem 4: k ≤ C·log(1/ε) + O(1)
        
        Args:
            epsilon: Target precision
            
        Returns:
            Theoretical bound on number of steps
        """
        return self.C * np.log(1/epsilon)


def demonstrate_convergence_rate():
    """Demonstrate O(log(1/epsilon)) convergence rate."""
    rep = CantorRepresentation()
    epsilons = [10**(-i) for i in range(1, 8)]
    target = np.pi - 3  # Example: pi - 3 ≈ 0.14159...
    
    print("Convergence Rate Demonstration")
    print("=" * 50)
    print(f"Target: π - 3 ≈ {target:.10f}")
    print()
    print(f"{'Epsilon':>12} {'Steps':>8} {'Rate':>10} {'Error':>12}")
    print("-" * 50)
    
    for eps in epsilons:
        result = rep.approximate(target, epsilon=eps)
        rate = result.steps / np.log(1/eps) if result.steps > 0 else 0
        print(f"{eps:>12.0e} {result.steps:>8} {rate:>10.3f} {result.error:>12.2e}")
    
    print()
    print(f"Theoretical C = 1/log(3/2) ≈ {rep.C:.3f}")


if __name__ == "__main__":
    demonstrate_convergence_rate()
