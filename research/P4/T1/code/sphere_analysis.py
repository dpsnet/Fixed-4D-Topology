#!/usr/bin/env python3
"""
P4-T1: Sphere Analysis - d_s vs Characteristic Classes
"""

import numpy as np
from math import gamma

def sphere_euler_characteristic(n):
    """Euler characteristic of n-sphere: χ = 1 + (-1)^n"""
    return 1 + (-1)**n

def heat_kernel_trace_sphere(t, n, radius=1.0):
    """Heat kernel trace on n-sphere (simplified)"""
    # Volume of n-sphere
    vol_sn = 2 * np.pi**((n+1)/2) / gamma((n+1)/2) * radius**n
    return (4 * np.pi * t)**(-n/2) * vol_sn

def spectral_dimension_estimate(n):
    """Estimate spectral dimension for n-sphere"""
    # For smooth manifold, d_s = n
    return float(n)

def analyze_spheres():
    """Analyze spectral dimension for various spheres."""
    print("="*70)
    print("Sphere Analysis: d_s vs Topology")
    print("="*70)
    print()
    
    dimensions = [2, 3, 4, 5, 6]
    
    print(f"{'n':<5} {'χ(S^n)':<10} {'d_s':<10} {'p-class':<10} {'Notes':<20}")
    print("-"*70)
    
    for n in dimensions:
        chi = sphere_euler_characteristic(n)
        d_s = spectral_dimension_estimate(n)
        p_class = 1 if n % 4 == 0 else 0
        
        notes = []
        if chi == 2:
            notes.append("even")
        else:
            notes.append("odd")
        
        print(f"{n:<5} {chi:<10} {d_s:<10.1f} {p_class:<10} {', '.join(notes):<20}")
    
    print()
    print("="*70)
    print("Observations:")
    print("  - d_s = n for S^n")
    print("  - χ(S^n) = 2 (even n), 0 (odd n)")
    print("  - Need: d_s = f(χ, p-classes)")
    print("="*70)

if __name__ == "__main__":
    analyze_spheres()
