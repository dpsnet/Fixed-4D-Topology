"""
Command-line interface for Fixed 4D Topology.

Provides verification and diagnostic tools.
"""

import argparse
import sys
from typing import Optional

from . import __version__
from .cantor_representation import CantorRepresentation
from .spectral_dimension import SpectralDimension
from .modular_correspondence import ModularCorrespondence
from .fractal_arithmetic import FractalArithmetic, GrothendieckGroup


def verify_command() -> int:
    """
    Run verification tests for all theory threads.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Verify Fixed 4D Topology installation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()
    
    print(f"Fixed 4D Topology v{__version__}")
    print("=" * 50)
    
    all_passed = True
    
    # T1: Cantor Representation
    print("\n[T1] Testing Cantor Representation...")
    try:
        rep = CantorRepresentation()
        result = rep.approximate(alpha=0.5, epsilon=1e-4)
        assert result.error < 1e-4
        if args.verbose:
            print(f"  Approximation: {result.approximation}")
            print(f"  Error: {result.error}")
            print(f"  Steps: {result.steps}")
        print("  ✓ T1 passed")
    except Exception as e:
        print(f"  ✗ T1 failed: {e}")
        all_passed = False
    
    # T2: Spectral Dimension
    print("\n[T2] Testing Spectral Dimension...")
    try:
        spec = SpectralDimension("sierpinski")
        d_s = spec.compute_spectral_dimension(t=1e-5)
        expected = 2 * 3.14159265359 * 0.217  # Approximate
        assert abs(d_s - 1.365) < 0.1
        if args.verbose:
            print(f"  d_s(10^-5) = {d_s:.6f}")
        print("  ✓ T2 passed")
    except Exception as e:
        print(f"  ✗ T2 failed: {e}")
        all_passed = False
    
    # T3: Modular Correspondence
    print("\n[T3] Testing Modular Correspondence...")
    try:
        corr = ModularCorrespondence()
        l_val = corr.ramanujan.compute_l_function("delta", s=6)
        assert abs(l_val.real - 0.037) < 0.01
        if args.verbose:
            print(f"  L(Δ, 6) = {l_val}")
        print("  ✓ T3 passed")
    except Exception as e:
        print(f"  ✗ T3 failed: {e}")
        all_passed = False
    
    # T4: Fractal Arithmetic
    print("\n[T4] Testing Fractal Arithmetic...")
    try:
        group = GrothendieckGroup()
        result = group.verify_isomorphism(n_tests=100)
        assert result["success_rate"] > 0.95
        if args.verbose:
            print(f"  Success rate: {result['success_rate']*100:.1f}%")
        print("  ✓ T4 passed")
    except Exception as e:
        print(f"  ✗ T4 failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


def main():
    """Main entry point."""
    sys.exit(verify_command())


if __name__ == "__main__":
    main()
