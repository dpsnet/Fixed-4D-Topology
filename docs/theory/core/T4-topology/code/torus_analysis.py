#!/usr/bin/env python3
"""
P4-T1: Torus Analysis - d_s vs Characteristic Classes
Execution: 2026-02-10 08:32 UTC+8

Analyze spectral dimension for n-tori and relate to topology.
"""

import numpy as np

def torus_euler_characteristic(n):
    """
    Euler characteristic of n-torus T^n = (S^1)^n:
    χ(T^n) = 0 for n > 0
    """
    return 0 if n > 0 else 1

def torus_pontryagin_classes(n):
    """
    Pontryagin classes for torus:
    T^n is flat, so all p-classes vanish.
    """
    return [0] * (n // 4 + 1)

def spectral_dimension_torus(n):
    """
    Spectral dimension of n-torus.
    For flat torus, d_s = n (topological dimension)
    """
    return float(n)

def analyze_tori():
    """Analyze spectral dimension for various tori."""
    print("="*70)
    print("Torus Analysis: d_s vs Topology")
    print("="*70)
    print()
    print("Key property: T^n is flat → all curvature invariants vanish")
    print()
    
    dimensions = [2, 3, 4, 5, 6]
    
    print(f"{'n':<5} {'χ(T^n)':<10} {'d_s':<10} {'p-classes':<15} {'Notes':<25}")
    print("-"*70)
    
    for n in dimensions:
        chi = torus_euler_characteristic(n)
        d_s = spectral_dimension_torus(n)
        p_classes = torus_pontryagin_classes(n)
        
        notes = ["flat", "p=0"]
        
        print(f"{n:<5} {chi:<10} {d_s:<10.1f} {str(p_classes):<15} {', '.join(notes):<25}")
    
    print()
    print("="*70)
    print("Key Observations:")
    print("  - χ(T^n) = 0 for all n > 0")
    print("  - All Pontryagin classes vanish (flat manifold)")
    print("  - Yet d_s = n varies")
    print()
    print("  ⇒ d_s cannot depend only on χ or p-classes!")
    print("  ⇒ Need more refined topological invariant")
    print("="*70)

def compare_manifolds():
    """Compare spheres and tori with same dimension."""
    print("\n" + "="*70)
    print("Comparison: S^n vs T^n")
    print("="*70)
    print()
    
    print(f"{'n':<5} {'Manifold':<12} {'χ':<10} {'d_s':<10} {'Difference':<20}")
    print("-"*70)
    
    for n in [2, 3, 4]:
        # Sphere
        chi_s = 1 + (-1)**n
        d_s_s = float(n)
        print(f"{n:<5} {'S^'+str(n):<12} {chi_s:<10} {d_s_s:<10.1f} {'curved':<20}")
        
        # Torus
        chi_t = 0
        d_s_t = float(n)
        print(f"{n:<5} {'T^'+str(n):<12} {chi_t:<10} {d_s_t:<10.1f} {'flat':<20}")
        print()
    
    print("="*70)
    print("Conclusion:")
    print("  Same d_s, different χ → χ alone doesn't determine d_s")
    print("  Need: d_s = f(metric, topology)")
    print("="*70)

if __name__ == "__main__":
    analyze_tori()
    compare_manifolds()
