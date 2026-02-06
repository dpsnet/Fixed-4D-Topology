"""
Example: Cantor Representation Theory (T1)

Demonstrates approximation of real numbers using Cantor class fractal dimensions.
"""

import numpy as np
from fixed_4d_topology import CantorRepresentation


def main():
    print("=" * 60)
    print("Cantor Representation Theory Demo")
    print("=" * 60)
    print()
    
    # Initialize
    rep = CantorRepresentation()
    
    print("Canonical Cantor Dimensions:")
    for i, d in enumerate(rep.CANTOR_DIMENSIONS):
        print(f"  d_{i+1} = {d:.6f}")
    print()
    
    # Example 1: Approximate pi - 3
    target = np.pi - 3
    print(f"Example 1: Approximating π - 3 ≈ {target:.10f}")
    print("-" * 40)
    
    for eps in [1e-3, 1e-5, 1e-7]:
        result = rep.approximate(target, epsilon=eps)
        print(f"ε = {eps:.0e}: error = {result.error:.2e}, steps = {result.steps}")
    print()
    
    # Example 2: Convergence rate verification
    print("Convergence Rate Verification")
    print("-" * 40)
    print(f"Theoretical C = 1/log(3/2) ≈ {rep.C:.3f}")
    print()
    print(f"{'Epsilon':>12} {'Steps':>8} {'C·log(1/ε)':>12} {'Ratio':>8}")
    print("-" * 50)
    
    for i in range(1, 8):
        eps = 10**(-i)
        result = rep.approximate(target, epsilon=eps)
        theoretical = rep.C * np.log(1/eps)
        ratio = result.steps / theoretical if theoretical > 0 else 0
        print(f"{eps:>12.0e} {result.steps:>8} {theoretical:>12.2f} {ratio:>8.2f}")
    print()
    
    # Example 3: Verify linear independence
    print("Linear Independence Check")
    print("-" * 40)
    is_independent = rep.verify_linear_independence()
    print(f"Dimensions are linearly independent: {'✓' if is_independent else '✗'}")
    print()
    
    print("Demo complete!")


if __name__ == "__main__":
    main()
