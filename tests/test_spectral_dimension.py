"""
Tests for spectral dimension evolution (T2).
"""

import numpy as np
import pytest
from fixed_4d_topology import SpectralDimension


class TestSpectralDimension:
    """Test suite for spectral dimension PDE."""
    
    def test_initialization(self):
        """Test SpectralDimension initialization."""
        spec = SpectralDimension("sierpinski")
        assert spec.fractal_type == "sierpinski"
        assert "d_s_exact" in spec.fractal_info
    
    def test_sierpinski_dimension(self):
        """Test Sierpinski gasket spectral dimension."""
        spec = SpectralDimension("sierpinski")
        expected = 2 * np.log(3) / np.log(5)
        
        d_s = spec.compute_spectral_dimension(t=1e-5)
        assert abs(d_s - expected) < 0.01
    
    def test_evolution(self):
        """Test spectral dimension evolution."""
        spec = SpectralDimension("sierpinski")
        result = spec.evolve(t_span=(1e-5, 1.0), n_points=100)
        
        assert result.convergence_achieved
        assert len(result.t_values) == 100
        assert len(result.d_s_values) == 100
    
    def test_pde_verification(self):
        """Test PDE consistency."""
        spec = SpectralDimension("sierpinski")
        stats = spec.verify_pde()
        
        assert stats["max_error"] < 1.0
        assert stats["mean_error"] < 0.1
    
    def test_different_fractals(self):
        """Test different fractal types."""
        for fractal_type in ["sierpinski", "cantor_dust"]:
            spec = SpectralDimension(fractal_type)
            d_s = spec.compute_spectral_dimension(t=1e-5)
            assert 0 < d_s < 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
