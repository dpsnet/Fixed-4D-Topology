#!/usr/bin/env python3
"""
SnapPy Installation Test Script
===============================
This script verifies that SnapPy is correctly installed and can perform
basic operations for studying hyperbolic 3-manifolds and Kleinian groups.

Author: System Installation
Date: 2026-02-11
"""

import sys
import warnings

# Suppress GUI-related warnings (tkinter not available in headless mode)
warnings.filterwarnings('ignore', message='.*tkinter.*', category=UserWarning)

def test_import():
    """Test that SnapPy can be imported."""
    print("=" * 60)
    print("Testing SnapPy Import")
    print("=" * 60)
    try:
        import snappy
        print(f"✓ SnapPy imported successfully")
        print(f"  Version: {snappy.__version__}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import SnapPy: {e}")
        return False

def test_manifold_creation():
    """Test creating basic manifolds."""
    print("\n" + "=" * 60)
    print("Testing Manifold Creation")
    print("=" * 60)
    try:
        import snappy
        
        # Create figure-eight knot complement
        M = snappy.Manifold('4_1')
        print(f"✓ Created manifold: {M.name()}")
        print(f"  Volume: {float(M.volume()):.6f}")
        
        # Create another manifold
        N = snappy.Manifold('m003')
        print(f"✓ Created manifold: {N.name()}")
        print(f"  Volume: {float(N.volume()):.6f}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create manifold: {e}")
        return False

def test_hyperbolic_structure():
    """Test hyperbolic structure computation."""
    print("\n" + "=" * 60)
    print("Testing Hyperbolic Structure")
    print("=" * 60)
    try:
        import snappy
        
        M = snappy.Manifold('4_1')
        
        # Check if manifold is orientable
        print(f"✓ Orientable: {M.is_orientable()}")
        
        # Get number of cusps
        print(f"✓ Number of cusps: {M.num_cusps()}")
        
        # Try to compute Chern-Simons invariant
        try:
            cs = M.chern_simons()
            print(f"✓ Chern-Simons invariant: {cs}")
        except Exception as e:
            print(f"  Chern-Simons not available: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Failed hyperbolic structure test: {e}")
        return False

def test_isometry_signature():
    """Test isometry signature computation."""
    print("\n" + "=" * 60)
    print("Testing Isometry Signature")
    print("=" * 60)
    try:
        import snappy
        
        M = snappy.Manifold('4_1')
        sig = M.isometry_signature()
        if sig:
            print(f"✓ Isometry signature: {sig[:50]}...")
        else:
            print("✓ Isometry signature: None (expected for non-triangulated)")
        
        return True
    except Exception as e:
        print(f"✗ Failed isometry signature test: {e}")
        return False

def test_dirichlet_domain():
    """Test Dirichlet domain computation."""
    print("\n" + "=" * 60)
    print("Testing Dirichlet Domain")
    print("=" * 60)
    try:
        import snappy
        
        M = snappy.Manifold('4_1')
        domain = M.dirichlet_domain()
        print(f"✓ Dirichlet domain computed")
        print(f"  Number of faces: {domain.num_faces()}")
        print(f"  Number of vertices: {domain.num_vertices()}")
        
        return True
    except Exception as e:
        print(f"✗ Failed Dirichlet domain test: {e}")
        return False

def test_census_access():
    """Test census manifold access."""
    print("\n" + "=" * 60)
    print("Testing Census Access")
    print("=" * 60)
    try:
        import snappy
        
        # Access OrientableCuspedCensus
        census = snappy.OrientableCuspedCensus
        print(f"✓ OrientableCuspedCensus loaded")
        
        # Count manifolds with volume < 1.0
        small_manifolds = [M for M in census if float(M.volume()) < 1.0][:5]
        print(f"✓ Found {len(small_manifolds)} manifolds with volume < 1.0 (showing first 5)")
        for M in small_manifolds:
            print(f"    {M.name()}: volume = {float(M.volume()):.6f}")
        
        return True
    except Exception as e:
        print(f"✗ Failed census access test: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SnapPy Installation Verification")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Import", test_import()))
    results.append(("Manifold Creation", test_manifold_creation()))
    results.append(("Hyperbolic Structure", test_hyperbolic_structure()))
    results.append(("Isometry Signature", test_isometry_signature()))
    results.append(("Dirichlet Domain", test_dirichlet_domain()))
    results.append(("Census Access", test_census_access()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! SnapPy is correctly installed.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
