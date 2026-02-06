"""
Example: Fractal Arithmetic & Grothendieck Group (T4)

Demonstrates algebraic structure on fractal dimensions.
"""

import numpy as np
from fixed_4d_topology import FractalArithmetic, GrothendieckGroup, FractalElement


def main():
    print("=" * 60)
    print("Fractal Arithmetic & Grothendieck Group Demo")
    print("=" * 60)
    print()
    
    # Initialize
    arith = FractalArithmetic()
    group = GrothendieckGroup()
    
    print("Grothendieck Group Isomorphism: 𝒢_D^(r) ≅ (ℚ, +)")
    print("-" * 60)
    print()
    
    # Example 1: Element creation and isomorphism
    print("Example 1: Grothendieck Group Elements")
    print("-" * 40)
    
    elements = [
        FractalElement((2, 3), (1, 3)),  # log(2)/log(3)
        FractalElement((3, 3), (1, 3)),  # log(3)/log(3) = 1
        FractalElement((4, 3), (1, 3)),  # log(4)/log(3)
    ]
    
    for i, elem in enumerate(elements):
        q = group.log_isomorphism(elem)
        d_val = elem.dimension_value()
        print(f"Element {i+1}: [{elem.positive[0]}/{elem.negative[0]}]")
        print(f"  Dimension value: {d_val:.6f}")
        print(f"  φ(element) = {q} ≈ {float(q):.6f}")
        print()
    
    # Example 2: Group operation
    print("Example 2: Group Operation (Addition)")
    print("-" * 40)
    
    a = elements[0]  # log(2)/log(3)
    b = elements[1]  # 1
    c = group.group_operation(a, b)
    
    print(f"a = log(2)/log(3) ≈ {a.dimension_value():.6f}")
    print(f"b = 1")
    print(f"a ⊕ b = c ≈ {c.dimension_value():.6f}")
    print()
    print(f"φ(a) = {group.log_isomorphism(a)}")
    print(f"φ(b) = {group.log_isomorphism(b)}")
    print(f"φ(a ⊕ b) = {group.log_isomorphism(c)}")
    print(f"φ(a) + φ(b) = {group.log_isomorphism(a) + group.log_isomorphism(b)}")
    print()
    
    # Example 3: Fractal arithmetic
    print("Example 3: Fractal Dimension Arithmetic")
    print("-" * 40)
    
    d1 = np.log(2) / np.log(3)  # ~0.6309
    d2 = np.log(3) / np.log(3)  # 1.0
    
    d_sum = arith.add_dimensions(d1, d2, base=3.0)
    
    print(f"d1 = log(2)/log(3) ≈ {d1:.6f}")
    print(f"d2 = log(3)/log(3) = {d2:.6f}")
    print(f"d1 ⊕ d2 = {d_sum:.6f}")
    print(f"Expected: log(6)/log(3) = {np.log(6)/np.log(3):.6f}")
    print()
    
    # Example 4: Isomorphism verification
    print("Example 4: Isomorphism Verification")
    print("-" * 40)
    
    result = group.verify_isomorphism(n_tests=100)
    print(f"Tests run: {result['n_tests']}")
    print(f"Success rate: {result['success_rate']*100:.1f}%")
    print(f"Mean error: {result['mean_error']:.2e}")
    print(f"Max error: {result['max_error']:.2e}")
    print()
    
    print("=" * 60)
    print("Demo complete!")


if __name__ == "__main__":
    main()
