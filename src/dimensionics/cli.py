#!/usr/bin/env python3
"""
Command Line Interface for Dimensionics

Provides command-line tools for verifying the unified theory.
"""

import sys
import json
from dimensionics.bridges import (
    BridgeA_FractalLaplacian,
    BridgeB_VariationalWeights,
    BridgeC_NetworkNeuralIsomorphism,
)
from dimensionics.core import MasterEquation


def verify_all_bridges():
    """Verify all three final bridges"""
    print("=" * 70)
    print("DIMENSIONICS: Final 5% Bridge Verification")
    print("=" * 70)
    
    results = {}
    
    # Bridge A
    print("\n[Bridge A] Cantor Complexity ↔ Spectral Geometry")
    bridge_a = BridgeA_FractalLaplacian()
    results['bridge_a'] = bridge_a.derive_c_star()
    print(f"  C* (theoretical): {results['bridge_a']['C_star_theoretical']:.4f}")
    print(f"  C* (empirical):   {results['bridge_a']['C_star_empirical']:.4f}")
    print(f"  Status: {'✓ PASS' if bridge_a.verify() else '✗ FAIL'}")
    
    # Bridge B
    print("\n[Bridge B] Variational Principle for Unified Weights")
    bridge_b = BridgeB_VariationalWeights()
    results['bridge_b'] = bridge_b.derive_weights()
    print(f"  Weights (theoretical): {results['bridge_b']['weights_theoretical']}")
    print(f"  Weights (empirical):   {results['bridge_b']['weights_empirical']}")
    print(f"  Status: {'✓ PASS' if bridge_b.verify() else '✗ FAIL'}")
    
    # Bridge C
    print("\n[Bridge C] Network-Neural Isomorphism")
    bridge_c = BridgeC_NetworkNeuralIsomorphism()
    results['bridge_c'] = bridge_c.verify_isomorphism()
    print(f"  Is unitary: {results['bridge_c']['is_unitary']}")
    print(f"  Spectrum correlation: {results['bridge_c']['spectrum_correlation']:.6f}")
    print(f"  Status: {'✓ PASS' if bridge_c.verify() else '✗ FAIL'}")
    
    # Overall
    print("\n" + "=" * 70)
    all_pass = (
        bridge_a.verify() and 
        bridge_b.verify() and 
        bridge_c.verify()
    )
    if all_pass:
        print("✓ ALL BRIDGES VERIFIED - Dimensionics 100% Complete")
    else:
        print("⚠ Some bridges need refinement")
    print("=" * 70)
    
    return 0 if all_pass else 1


def demo():
    """Run a demonstration of Dimensionics"""
    print("=" * 70)
    print("DIMENSIONICS: Demonstration")
    print("=" * 70)
    
    # Master Equation demo
    print("\n[1] Master Equation")
    me = MasterEquation(alpha=0.5, beta=0.3)
    d_eq = me.solve_equilibrium(T=1.0)
    print(f"  Equilibrium dimension: d_eff = {d_eq:.4f}")
    print(f"  Convexity satisfied: {me.check_convexity()}")
    
    # Dimension flow
    print("\n[2] Dimension Flow")
    d_flow = me.solve_dimension_flow(d_initial=4.0, t_span=5.0)
    print(f"  Initial: d_s(0) = {d_flow[0]:.4f}")
    print(f"  Final:   d_s(5) = {d_flow[-1]:.4f}")
    print(f"  Flow: UV→IR = {d_flow[0]:.1f}→{d_flow[-1]:.1f}")
    
    print("\n" + "=" * 70)
    print("Demonstration complete!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        sys.exit(verify_all_bridges())
    else:
        sys.exit(demo())
