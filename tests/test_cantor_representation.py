"""
Tests for Cantor representation theory (T1).
"""

import numpy as np
import pytest
from fixed_4d_topology import CantorRepresentation


class TestCantorRepresentation:
    """Test suite for Cantor class fractal representation."""
    
    def test_initialization(self):
        """Test CantorRepresentation initialization."""
        rep = CantorRepresentation()
        assert len(rep.dimensions) > 0
        assert rep.C > 0
    
    def test_approximation_basic(self):
        """Test basic approximation functionality."""
        rep = CantorRepresentation()
        result = rep.approximate(0.5, epsilon=1e-4)
        
        assert result.error < 1e-4
        assert result.steps > 0
        assert result.steps <= rep.C * np.log(1e4) + 10
    
    def test_approximation_convergence(self):
        """Test convergence for various targets."""
        rep = CantorRepresentation()
        targets = [0.1, 0.5, 1.0, np.pi - 3, np.e - 2]
        
        for target in targets:
            result = rep.approximate(target, epsilon=1e-5)
            assert result.error < 1e-5, f"Failed for target {target}"
    
    def test_linear_independence(self):
        """Test linear independence verification."""
        rep = CantorRepresentation()
        is_independent = rep.verify_linear_independence()
        assert is_independent, "Dimensions should be linearly independent"
    
    def test_optimal_complexity(self):
        """Test optimal complexity bound."""
        rep = CantorRepresentation()
        bound = rep.compute_optimal_complexity(1e-6)
        assert bound > 0
        
        # Verify actual steps are close to bound
        result = rep.approximate(0.5, epsilon=1e-6)
        assert result.steps <= bound + 10
    
    def test_density_analysis(self):
        """Test density analysis."""
        rep = CantorRepresentation()
        stats = rep.analyze_density(n_samples=100)
        
        assert stats["success_rate"] > 0.9
        assert stats["mean_error"] < 1e-3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
