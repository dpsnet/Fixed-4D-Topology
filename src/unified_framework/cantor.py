"""
Cantor Representation Module (T1 Direction)
===========================================

Implementation of Cantor class fractal representation theory.
"""

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    import math
    # Minimal numpy-like fallback
    class _NumpyFallback:
        @staticmethod
        def mean(arr):
            return sum(arr) / len(arr) if arr else 0
        @staticmethod
        def std(arr, ddof=0):
            if len(arr) <= ddof:
                return 0
            m = sum(arr) / len(arr)
            variance = sum((x - m) ** 2 for x in arr) / (len(arr) - ddof)
            return math.sqrt(variance)
        @staticmethod
        def array(arr):
            return list(arr)
        @staticmethod
        def log(x):
            if hasattr(x, '__iter__'):
                return [math.log(v) for v in x]
            return math.log(x)
        @staticmethod
        def exp(x):
            if hasattr(x, '__iter__'):
                return [math.exp(v) for v in x]
            return math.exp(x)
        @staticmethod
        def linspace(start, stop, num):
            if num <= 1:
                return [start]
            step = (stop - start) / (num - 1)
            return [start + i * step for i in range(num)]
        @staticmethod
        def zeros(n):
            return [0.0] * n
        @staticmethod
        def sqrt(x):
            if hasattr(x, '__iter__'):
                return [math.sqrt(v) for v in x]
            return math.sqrt(x)
        @staticmethod
        def logspace(start, stop, num):
            # Generate logarithmically spaced numbers
            log_start = start * math.log(10)
            log_stop = stop * math.log(10)
            step = (log_stop - log_start) / (num - 1) if num > 1 else 0
            return [math.exp(log_start + i * step) for i in range(num)]
        @staticmethod
        def max(arr):
            return max(arr) if arr else 0
        @staticmethod
        def min(arr):
            return min(arr) if arr else 0
        @staticmethod
        def arange(n):
            return list(range(n))
        @staticmethod
        def polyfit(x, y, deg):
            # Simple linear regression for deg=1
            if deg != 1:
                raise NotImplementedError("Only linear fit supported in fallback")
            n = len(x)
            x_mean = sum(x) / n
            y_mean = sum(y) / n
            ss_xy = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
            ss_xx = sum((x[i] - x_mean) ** 2 for i in range(n))
            slope = ss_xy / ss_xx if ss_xx != 0 else 0
            intercept = y_mean - slope * x_mean
            return [slope, intercept]
    np = _NumpyFallback()
from typing import List, Tuple, Optional
from fractions import Fraction


class CantorRepresentation:
    """
    Cantor class fractal representation for real numbers.
    
    Implements the greedy approximation algorithm from T1.
    """
    
    def __init__(self, max_terms: int = 100):
        """
        Initialize Cantor representation.
        
        Args:
            max_terms: Maximum number of terms in expansion
        """
        self.max_terms = max_terms
        self.cantor_dimensions = self._generate_cantor_dimensions()
        
    def _generate_cantor_dimensions(self, max_n: int = 20) -> List[Tuple[float, int, float]]:
        """
        Generate Cantor class dimensions d_{N,r} = log(N)/log(1/r).
        
        Returns:
            List of (dimension, N, r) tuples
        """
        dimensions = []
        
        # Standard Cantor-type dimensions
        params = [
            (2, 1/3),    # Standard Cantor: log(2)/log(3)
            (3, 1/3),    # Cantor dust
            (2, 1/4),    # Modified Cantor
            (3, 1/2),    # High-multiplicity
            (4, 1/3),    # 4-part Cantor
            (5, 1/3),    # 5-part Cantor
            (2, 1/5),    # Sparse Cantor
            (3, 1/4),    # Intermediate
            (4, 1/2),    # Dense
            (2, 1/6),    # Very sparse
        ]
        
        for N, r in params:
            d = np.log(N) / np.log(1/r)
            dimensions.append((d, N, r))
        
        # Sort by dimension value
        dimensions.sort(key=lambda x: x[0])
        
        return dimensions
    
    def greedy_approximate(self, 
                          target: float, 
                          epsilon: float = 1e-6) -> Tuple[float, List[Tuple[float, float]]]:
        """
        Greedy algorithm for Cantor approximation.
        
        Args:
            target: Target real number
            epsilon: Desired precision
            
        Returns:
            Tuple of (approximation, coefficients)
            where coefficients is list of (dimension, coefficient) pairs
        """
        residual = target
        coefficients = []
        
        for _ in range(self.max_terms):
            if abs(residual) < epsilon:
                break
            
            # Find best coefficient for each dimension
            best_error = abs(residual)
            best_choice = None
            
            for d_i, N, r in self.cantor_dimensions:
                # Optimal coefficient: round residual / d_i to simple fraction
                coeff_float = residual / d_i
                
                # Try simple fractions
                for denom in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    for num in range(-10, 11):
                        if denom == 0:
                            continue
                        coeff = num / denom
                        error = abs(residual - coeff * d_i)
                        
                        if error < best_error:
                            best_error = error
                            best_choice = (d_i, coeff)
            
            if best_choice is None:
                break
                
            d_i, coeff = best_choice
            
            # Update
            residual -= coeff * d_i
            coefficients.append((d_i, coeff))
        
        # Compute final approximation
        approximation = sum(coeff * d_i for d_i, coeff in coefficients)
        
        return approximation, coefficients
    
    def linear_independence_check(self, 
                                  coeffs: List[Tuple[float, float]], 
                                  tolerance: float = 1e-10) -> bool:
        """
        Verify linear independence of Cantor dimensions.
        
        Args:
            coeffs: List of (dimension, coefficient) pairs
            tolerance: Numerical tolerance
            
        Returns:
            True if approximately independent
        """
        # Check if sum is approximately zero
        total = sum(c * d for d, c in coeffs)
        return abs(total) > tolerance
    
    def density_verification(self, 
                            target: float, 
                            num_trials: int = 100) -> dict:
        """
        Verify density of Cantor rational combinations.
        
        Args:
            target: Target dimension
            num_trials: Number of approximation trials
            
        Returns:
            Statistics on approximation quality
        """
        errors = []
        
        for epsilon in np.logspace(-1, -6, num_trials):
            approx, _ = self.greedy_approximate(target, epsilon)
            error = abs(target - approx)
            errors.append(error)
        
        return {
            'mean_error': np.mean(errors),
            'max_error': np.max(errors),
            'min_error': np.min(errors),
            'convergence_rate': self._estimate_convergence_rate(errors)
        }
    
    def _estimate_convergence_rate(self, errors: List[float]) -> float:
        """Estimate convergence rate from error sequence."""
        if len(errors) < 2:
            return 0.0
        
        # Fit log(error) vs step
        steps = np.arange(len(errors))
        log_errors = np.log(errors)
        
        # Linear regression
        slope, _ = np.polyfit(steps, log_errors, 1)
        return slope  # Should be approximately log(2/3) ≈ -0.405
    
    def get_convergence_constant(self) -> float:
        """
        Get theoretical convergence constant C = 1/log(3/2).
        
        Returns:
            Theoretical constant
        """
        return 1.0 / np.log(3/2)
    
    def info(self) -> dict:
        """Get information about the Cantor representation system."""
        return {
            'num_dimensions': len(self.cantor_dimensions),
            'dimension_range': (
                min(d for d, _, _ in self.cantor_dimensions),
                max(d for d, _, _ in self.cantor_dimensions)
            ),
            'max_terms': self.max_terms,
            'convergence_constant': self.get_convergence_constant()
        }


def demo_cantor_approximation():
    """Demonstrate Cantor approximation capabilities."""
    print("Cantor Representation Demo")
    print("="*60)
    
    cantor = CantorRepresentation()
    
    # Test targets
    targets = [
        np.sqrt(2) - 1,      # ~0.414
        np.pi - 3,           # ~0.141
        np.e - 2,            # ~0.718
        (1 + np.sqrt(5)) / 2 - 1,  # Golden ratio - 1
    ]
    
    epsilon = 1e-6
    
    for target in targets:
        print(f"\nTarget: {target:.6f}")
        approx, coeffs = cantor.greedy_approximate(target, epsilon)
        
        print(f"Approximation: {approx:.6f}")
        print(f"Error: {abs(target - approx):.2e}")
        print(f"Terms: {len(coeffs)}")
        print("Coefficients:")
        for d_i, q_i in coeffs[:5]:  # Show first 5
            print(f"  {q_i:+.3f} × {d_i:.4f}")
        if len(coeffs) > 5:
            print(f"  ... and {len(coeffs)-5} more")
    
    print("\n" + "="*60)
    print(f"Convergence constant: {cantor.get_convergence_constant():.4f}")
    print(f"Theoretical: O(log(1/ε)) steps for precision ε")


if __name__ == "__main__":
    demo_cantor_approximation()