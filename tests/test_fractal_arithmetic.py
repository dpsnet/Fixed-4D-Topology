"""
Tests for fractal arithmetic and Grothendieck group (T4).
"""

import numpy as np
import pytest
from fixed_4d_topology import FractalArithmetic, GrothendieckGroup, FractalElement


class TestGrothendieckGroup:
    """Test suite for Grothendieck group."""
    
    def test_initialization(self):
        """Test GrothendieckGroup initialization."""
        group = GrothendieckGroup()
        assert group.max_denominator > 0
    
    def test_log_isomorphism(self):
        """Test logarithmic isomorphism."""
        group = GrothendieckGroup()
        element = FractalElement((2, 3), (1, 3))
        
        q = group.log_isomorphism(element)
        assert q.numerator > 0
        assert q.denominator > 0
    
    def test_group_operation(self):
        """Test group operation."""
        group = GrothendieckGroup()
        a = FractalElement((2, 3), (1, 3))
        b = FractalElement((3, 3), (1, 3))
        
        c = group.group_operation(a, b)
        
        # Verify homomorphism
        phi_a = group.log_isomorphism(a)
        phi_b = group.log_isomorphism(b)
        phi_c = group.log_isomorphism(c)
        
        assert abs(float(phi_c - (phi_a + phi_b))) < 1e-10
    
    def test_isomorphism_verification(self):
        """Test isomorphism verification."""
        group = GrothendieckGroup()
        result = group.verify_isomorphism(n_tests=50)
        
        assert result["success_rate"] > 0.95
        assert result["mean_error"] < 1e-6


class TestFractalArithmetic:
    """Test suite for fractal arithmetic."""
    
    def test_add_dimensions(self):
        """Test dimension addition."""
        arith = FractalArithmetic()
        d1 = np.log(2) / np.log(3)
        d2 = np.log(3) / np.log(3)
        
        result = arith.add_dimensions(d1, d2, base=3.0)
        expected = np.log(6) / np.log(3)
        
        assert abs(result - expected) < 1e-10
    
    def test_dimension_to_rational(self):
        """Test dimension to rational conversion."""
        arith = FractalArithmetic()
        d = np.log(2) / np.log(3)
        
        q = arith.dimension_to_rational(d, r=3.0)
        assert q.numerator == 1  # log(2)
        assert q.denominator == 2  # log(3) approx


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
